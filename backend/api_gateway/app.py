# API Gateway - Main Entry Point with Service Routing
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
from datetime import datetime
import logging

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Service endpoints
SERVICES = {
    'ml_model': 'http://localhost:5002',
    'honeypot': 'http://localhost:5001', 
    'fingerprinting': 'http://localhost:5003'
}

def call_service(service_name, endpoint, method='GET', data=None, timeout=30):
    """Call a microservice with error handling"""
    try:
        service_url = SERVICES.get(service_name)
        if not service_url:
            raise ValueError(f"Unknown service: {service_name}")
        
        url = f"{service_url}{endpoint}"
        logger.info(f"🔗 Calling {service_name}: {method} {url}")
        
        if method == 'POST':
            response = requests.post(url, json=data, timeout=timeout)
        else:
            response = requests.get(url, timeout=timeout)
        
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.Timeout:
        logger.error(f"⏰ Timeout calling {service_name}")
        return {'error': f'Service {service_name} timeout', 'service': service_name}
    except requests.exceptions.ConnectionError:
        logger.error(f"🔌 Connection error to {service_name}")
        return {'error': f'Service {service_name} unavailable', 'service': service_name}
    except Exception as e:
        logger.error(f"❌ Error calling {service_name}: {e}")
        return {'error': str(e), 'service': service_name}

@app.route('/health')
def health():
    """Health check for API Gateway and all services"""
    gateway_status = {
        'status': 'healthy',
        'service': 'api_gateway',
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }
    
    # Check all service health
    services_health = {}
    for service_name in SERVICES:
        health_response = call_service(service_name, '/health', timeout=5)
        services_health[service_name] = health_response
    
    return jsonify({
        'gateway': gateway_status,
        'services': services_health
    })

@app.route('/predict', methods=['POST'])
def predict():
    """Main prediction endpoint - integrates all services"""
    try:
        data = request.json
        logger.info(f"📥 Incoming prediction request from {request.remote_addr}")
        
        # Validate input data
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Add gateway metadata
        gateway_info = {
            'gateway_timestamp': datetime.utcnow().isoformat() + 'Z',
            'client_ip': request.remote_addr,
            'user_agent': request.headers.get('User-Agent'),
            'content_type': request.headers.get('Content-Type')
        }
        
        # Initialize results container
        all_results = {}
        
        # 1. Get ML Model Prediction (Primary)
        logger.info("🧠 Calling ML Model Service...")
        ml_response = call_service('ml_model', '/predict', method='POST', data=data)
        all_results['ml_model'] = ml_response
        
        # 2. Get Honeypot Analysis (Enhanced Security)
        logger.info("🍯 Calling Honeypot Service...")
        honeypot_data = {
            'events': data.get('events', []),
            'metadata': {
                'ip_address': request.remote_addr,
                'user_agent': request.headers.get('User-Agent')
            }
        }
        honeypot_response = call_service('honeypot', '/analyze', method='POST', data=honeypot_data)
        all_results['honeypot'] = honeypot_response
        
        # 3. Get Enhanced Fingerprinting Analysis
        logger.info("👆 Calling Enhanced Fingerprinting Service...")
        fingerprint_data = {
            'browserFingerprint': data.get('browserFingerprint', {}),
            'fingerprintRisk': data.get('fingerprintRisk', {}),
            'metadata': {
                'ip_address': request.remote_addr,
                'user_agent': request.headers.get('User-Agent')
            }
        }
        fingerprint_response = call_service('fingerprinting', '/analyze', method='POST', data=fingerprint_data)
        all_results['fingerprinting'] = fingerprint_response
        
        # 4. Combine Results into Final Prediction
        final_prediction = _combine_service_results(all_results, gateway_info)
        
        # Debug logging
        logger.info(f"🔍 Final response structure: {list(final_prediction.keys())}")
        logger.info(f"🔍 Prediction array length: {len(final_prediction.get('prediction', []))}")
        
        logger.info("✅ Integrated prediction completed successfully")
        return jsonify(final_prediction)
    
    except Exception as e:
        logger.error(f"❌ Gateway error: {e}")
        return jsonify({
            'error': 'Gateway processing error',
            'details': str(e),
            'gateway': {
                'timestamp': datetime.utcnow().isoformat() + 'Z',
                'service': 'api_gateway'
            }
        }), 500

def _combine_service_results(all_results, gateway_info):
    """Combine results from all services into final prediction"""
    try:
        # Extract ML prediction (primary)
        ml_result = all_results.get('ml_model', {})
        ml_prediction = ml_result.get('prediction', {})
        
        # Extract Honeypot analysis
        honeypot_result = all_results.get('honeypot', {})
        honeypot_analysis = honeypot_result.get('analysis', {})
        honeypot_verdict = honeypot_result.get('honeypot_verdict', {})
        
        # Extract Enhanced Fingerprinting analysis
        fingerprint_result = all_results.get('fingerprinting', {})
        fingerprint_analysis = fingerprint_result.get('analysis', {})
        fingerprint_patterns = fingerprint_result.get('analysisPatterns', {})
        fingerprint_features = fingerprint_result.get('browserFeatures', {})
        fingerprint_risk = fingerprint_result.get('fingerprintRisk', {})
        
        # Combine bot detection logic
        ml_bot_detected = ml_prediction.get('bot', False)
        honeypot_bot_detected = honeypot_verdict.get('is_bot', False)
        fingerprint_bot_detected = fingerprint_result.get('prediction') == 'bot'
        
        # Final decision logic - if any service detects bot with high confidence
        final_bot_prediction = (ml_bot_detected or 
                              honeypot_bot_detected or 
                              fingerprint_bot_detected)
        
        # Calculate combined confidence and risk score
        ml_confidence = ml_prediction.get('confidence', 0.5)
        honeypot_confidence = honeypot_verdict.get('confidence', 0.5)
        fingerprint_confidence = fingerprint_result.get('confidence', 0.5)
        combined_confidence = (ml_confidence + honeypot_confidence + fingerprint_confidence) / 3
        
        # Use highest risk score from all services
        ml_risk = ml_prediction.get('reconstruction_error', 0.5)
        fingerprint_risk_score = fingerprint_result.get('risk_score', 0.5)
        combined_risk_score = max(ml_risk, fingerprint_risk_score)
        
        # Determine risk level
        honeypot_threat = honeypot_analysis.get('threat_level', 'low')
        if (honeypot_threat in ['critical', 'high'] or 
            final_bot_prediction or 
            combined_risk_score > 0.7):
            risk_level = 'high'
        elif honeypot_threat == 'medium' or combined_risk_score > 0.5:
            risk_level = 'medium'
        else:
            risk_level = 'low'
        
        # Create BACKWARD COMPATIBLE response for frontend
        frontend_compatible_response = {
            # Original format that frontend expects
            'ip_address': gateway_info.get('client_ip', '127.0.0.1'),
            'user_agent': gateway_info.get('user_agent', 'Unknown'),
            'current_timestamp': gateway_info.get('gateway_timestamp', datetime.utcnow().isoformat() + 'Z'),
            'mouseMoveCount': ml_result.get('metadata', {}).get('mouseMoveCount', 0),
            'keyPressCount': ml_result.get('metadata', {}).get('keyPressCount', 0),
            'prediction': [{
                'bot': final_bot_prediction,
                'reconstruction_error': ml_prediction.get('reconstruction_error', combined_risk_score),
                'confidence': combined_confidence,
                'raw_error': ml_prediction.get('raw_error', 0)
            }],
            # Enhanced fingerprinting data for admin display
            'analysisPatterns': fingerprint_patterns,
            'browserFeatures': fingerprint_features,
            'fingerprintRisk': fingerprint_risk,
            'risk_score': combined_risk_score,
            # Enhanced data for advanced use
            'enhanced_prediction': {
                'is_bot': final_bot_prediction,
                'confidence': float(combined_confidence),
                'risk_level': risk_level,
                'risk_score': combined_risk_score,
                'recommendation': 'block' if final_bot_prediction else 'allow'
            },
            'service_results': {
                'ml_model': {
                    'bot_detected': ml_bot_detected,
                    'reconstruction_error': ml_prediction.get('reconstruction_error', 0),
                    'confidence': ml_confidence,
                    'status': 'success' if 'error' not in ml_result else 'failed'
                },
                'honeypot': {
                    'threat_detected': honeypot_bot_detected,
                    'threat_level': honeypot_threat,
                    'honeypot_score': honeypot_analysis.get('honeypot_score', 0),
                    'threat_indicators': honeypot_analysis.get('threat_indicators', []),
                    'status': 'success' if 'error' not in honeypot_result else 'failed'
                },
                'fingerprinting': {
                    'bot_detected': fingerprint_bot_detected,
                    'risk_score': fingerprint_risk_score,
                    'automation_detected': fingerprint_patterns.get('automationDetected', False),
                    'zero_features_detected': fingerprint_patterns.get('zeroFeaturesDetected', False),
                    'canvas_duplicate': fingerprint_patterns.get('canvasDuplicate', False),
                    'confidence': fingerprint_confidence,
                    'status': 'success' if 'error' not in fingerprint_result else 'failed'
                }
            },
            'gateway_metadata': {
                'processing_timestamp': datetime.utcnow().isoformat() + 'Z',
                'services_used': ['ml_model', 'honeypot', 'fingerprinting'],
                'version': '2.0'
            }
        }
        
        return frontend_compatible_response
    
    except Exception as e:
        logger.error(f"❌ Error combining service results: {e}")
        # Return backward compatible error response
        return {
            'ip_address': gateway_info.get('client_ip', '127.0.0.1'),
            'user_agent': gateway_info.get('user_agent', 'Unknown'),
            'current_timestamp': datetime.utcnow().isoformat() + 'Z',
            'mouseMoveCount': 0,
            'keyPressCount': 0,
            'prediction': [{
                'bot': True,  # Default to bot if error
                'reconstruction_error': 0.8,
                'confidence': 0.8
            }],
            'error': f'Error combining results: {str(e)}',
            'service_results': all_results
        }

@app.route('/predict/enhanced', methods=['POST'])
def predict_enhanced():
    """Enhanced prediction using multiple services (future feature)"""
    try:
        data = request.json
        logger.info(f"📥 Enhanced prediction request from {request.remote_addr}")
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # For now, just route to ML service
        # In future, can combine multiple services
        ml_response = call_service('ml_model', '/predict', method='POST', data=data)
        
        # Future: Add fingerprinting service
        # fingerprint_response = call_service('fingerprinting', '/analyze', method='POST', data=data)
        
        # Future: Add bot detection service  
        # detection_response = call_service('bot_detection', '/analyze', method='POST', data=data)
        
        response = {
            'gateway': {
                'timestamp': datetime.utcnow().isoformat() + 'Z',
                'service': 'api_gateway',
                'mode': 'enhanced'
            },
            'services': {
                'ml_model': ml_response,
                # 'fingerprinting': fingerprint_response,
                # 'bot_detection': detection_response
            },
            'final_prediction': ml_response.get('prediction', {})
        }
        
        return jsonify(response)
    
    except Exception as e:
        logger.error(f"❌ Enhanced prediction error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/services')
def list_services():
    """List all available services and their status"""
    service_status = {}
    
    for service_name in SERVICES:
        health_check = call_service(service_name, '/health', timeout=3)
        service_status[service_name] = {
            'url': SERVICES[service_name],
            'status': 'online' if 'status' in health_check else 'offline',
            'health': health_check
        }
    
    return jsonify({
        'gateway': 'api_gateway',
        'total_services': len(SERVICES),
        'services': service_status
    })

@app.route('/predictions', methods=['GET'])
def get_all_predictions():
    """Get predictions from all services"""
    try:
        all_predictions = {}
        
        # Get ML predictions
        ml_predictions = call_service('ml_model', '/predictions')
        if 'error' not in ml_predictions:
            all_predictions['ml_model'] = ml_predictions
        
        # Future: Add other service predictions
        # bot_predictions = call_service('bot_detection', '/predictions')
        # fingerprint_data = call_service('fingerprinting', '/data')
        
        return jsonify({
            'gateway': {
                'timestamp': datetime.utcnow().isoformat() + 'Z',
                'service': 'api_gateway'
            },
            'predictions': all_predictions
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/model/info')
def model_info():
    """Get ML model information through gateway"""
    try:
        ml_info = call_service('ml_model', '/model/info')
        
        return jsonify({
            'gateway': {
                'service': 'api_gateway',
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            },
            'ml_model_info': ml_info
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting API Gateway...")
    print("📡 Available Services:")
    for name, url in SERVICES.items():
        print(f"   {name}: {url}")
    print("🔗 Main endpoints:")
    print("   POST /predict - Main prediction endpoint")
    print("   GET  /health  - Health check all services")
    print("   GET  /services - List all services")
    app.run(debug=True, host='0.0.0.0', port=5000)
