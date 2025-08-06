# Unified Bot Detection API - Single Endpoint with Modular Functions
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import json
import os
from pathlib import Path
import logging

# Import our modular functions
from modules.ml_model import MLModelModule
from modules.honeypot import HoneypotModule
from modules.fingerprinting import FingerprintingModule

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize modules
print("🚀 Initializing Bot Detection API with Modular Architecture")
ml_module = MLModelModule()
honeypot_module = HoneypotModule()
fingerprinting_module = FingerprintingModule()

# Setup logging directory
BASE_DIR = Path(__file__).parent.parent
LOGS_DIR = BASE_DIR / 'logs' / 'predictions'
LOGS_DIR.mkdir(parents=True, exist_ok=True)
PREDICTIONS_FILE = LOGS_DIR / 'api_predictions.json'

def save_prediction(data):
    """Save prediction to JSON file"""
    try:
        if PREDICTIONS_FILE.exists():
            with open(PREDICTIONS_FILE, 'r') as f:
                predictions = json.load(f)
        else:
            predictions = []
        
        predictions.append(data)
        
        # Keep only last 1000 predictions to prevent file from getting too large
        if len(predictions) > 1000:
            predictions = predictions[-1000:]
        
        with open(PREDICTIONS_FILE, 'w') as f:
            json.dump(predictions, f, indent=2)
        
        logger.info(f"💾 Prediction saved to {PREDICTIONS_FILE}")
    except Exception as e:
        logger.error(f"❌ Error saving prediction: {e}")

@app.route('/health')
def health():
    """Health check for the unified API"""
    module_status = {
        'ml_model': ml_module.get_info(),
        'honeypot': honeypot_module.get_info(),
        'fingerprinting': fingerprinting_module.get_info()
    }
    
    return jsonify({
        'status': 'healthy',
        'service': 'unified_bot_detection_api',
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'architecture': 'modular_single_api',
        'modules': module_status
    })

@app.route('/predict', methods=['POST'])
def predict():
    """Main prediction endpoint - uses all modules and returns frontend-compatible response"""
    try:
        data = request.json
        logger.info(f"📥 Incoming prediction request from {request.remote_addr}")
        
        # Validate input data
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Extract required fields
        if 'mouseMoveCount' not in data or 'keyPressCount' not in data or 'events' not in data:
            return jsonify({"error": "mouseMoveCount, keyPressCount, and events are required"}), 400
        
        mouse_move_count = data.get('mouseMoveCount')
        key_press_count = data.get('keyPressCount')
        events = data.get('events', [])
        
        # Extract honeypot data from frontend
        honeypot_data = data.get('honeypot_data', {})
        
        # Extract enhanced fingerprinting data
        browser_fingerprint = data.get('browserFingerprint', {})
        fingerprint_risk = data.get('fingerprintRisk', {})
        enhanced_metadata = data.get('metadata', {})
        
        # Prepare metadata (combine traditional, enhanced, and honeypot data)
        metadata = {
            'ip_address': request.remote_addr,
            'user_agent': request.headers.get('User-Agent'),
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }
        
        # Add enhanced metadata if available
        metadata.update(enhanced_metadata)
        
        # Add honeypot-specific metadata
        if honeypot_data:
            metadata.update({
                'hidden_honeypot_field': honeypot_data.get('hidden_honeypot_field', ''),
                'fake_submit_clicked': honeypot_data.get('fake_submit_clicked', False),
                'js_optional_field': honeypot_data.get('js_optional_field', ''),
                'js_enabled': honeypot_data.get('js_enabled', True),
                'honeypot_triggers': honeypot_data.get('honeypot_triggers', {})
            })
        
        current_timestamp = datetime.utcnow().isoformat() + 'Z'
        
        # Run all modules with enhanced data
        logger.info("🔄 Running all detection modules with enhanced fingerprinting...")
        
        # 1. ML Model Analysis
        ml_result = ml_module.predict(events)
        
        # 2. Enhanced Honeypot Analysis (3-layer detection)
        honeypot_result = honeypot_module.analyze(events, metadata)
        
        # 3. Enhanced Fingerprinting Analysis
        fingerprint_result = fingerprinting_module.analyze_fingerprint(metadata, browser_fingerprint)
        
        # Combine results for final decision
        final_decision = combine_module_results(ml_result, honeypot_result, fingerprint_result)
        
        # Create FRONTEND-COMPATIBLE response (matches original format)
        response = {
            # Original format that frontend expects
            'ip_address': metadata['ip_address'],
            'user_agent': metadata['user_agent'],
            'current_timestamp': current_timestamp,
            'mouseMoveCount': mouse_move_count,
            'keyPressCount': key_press_count,
            'prediction': [{
                'bot': final_decision['is_bot'],
                'reconstruction_error': ml_result.get('reconstruction_error', 0.5),
                'confidence': final_decision['confidence'],
                'raw_error': ml_result.get('raw_error', 0)
            }],
            
            # Enhanced data for detailed analysis
            'enhanced_analysis': {
                'final_verdict': final_decision,
                'ml_analysis': {
                    'bot_detected': ml_result.get('bot', False),
                    'reconstruction_error': ml_result.get('reconstruction_error', 0),
                    'confidence': ml_result.get('confidence', 0.5),
                    'method': ml_result.get('method', 'unknown'),
                    'decision_logic': ml_result.get('decision_logic', ''),
                    'raw_error': ml_result.get('raw_error', 0),
                    'threshold': ml_result.get('threshold_used', 300)
                },
                'honeypot_analysis': {
                    'threat_detected': honeypot_result['honeypot_verdict']['is_bot'],
                    'threat_level': honeypot_result['analysis']['threat_level'],
                    'honeypot_score': honeypot_result['analysis'].get('honeypot_score', honeypot_result['analysis'].get('total_score', 0)),
                    'threat_indicators': honeypot_result['analysis']['threat_indicators'],
                    'confidence': honeypot_result['honeypot_verdict']['confidence'],
                    'honeypot_summary': honeypot_result.get('honeypot_summary', {}),
                    'honeypot_details': honeypot_result.get('honeypot_results', {}),
                    'detection_method': 'enhanced_3_layer_honeypot'
                },
                'fingerprint_analysis': {
                    'risk_level': fingerprint_result['analysis']['risk_level'],
                    'risk_score': fingerprint_result['analysis'].get('risk_score', 0),
                    'is_suspicious': fingerprint_result['verdict']['is_suspicious'],
                    'is_bot_likely': fingerprint_result['analysis'].get('is_bot_likely', False),
                    'risk_indicators': fingerprint_result['analysis']['risk_indicators'],
                    'total_indicators': fingerprint_result['analysis'].get('total_indicators', 0),
                    'device_hash': fingerprint_result['fingerprint'].get('device_hash', 'unknown'),
                    'confidence': fingerprint_result['verdict']['confidence'],
                    'bot_probability': fingerprint_result['verdict'].get('bot_probability', 0),
                    'feature_analysis': {
                        'webdriver_detected': browser_fingerprint.get('webdriver_detected', False),
                        'plugins_count': browser_fingerprint.get('plugins_count', 0),
                        'mime_types_count': browser_fingerprint.get('mime_types_count', 0),
                        'screen_suspicious': browser_fingerprint.get('suspicious_screen', False),
                        'browser_capabilities': {
                            'webgl': browser_fingerprint.get('webgl_supported', False),
                            'canvas': browser_fingerprint.get('canvas_supported', False),
                            'audio_context': browser_fingerprint.get('audio_context_supported', False)
                        }
                    }
                }
            },
            
            # API metadata
            'api_metadata': {
                'architecture': 'modular_single_api',
                'modules_used': ['ml_model', 'honeypot', 'fingerprinting'],
                'processing_timestamp': current_timestamp,
                'version': '3.0'
            }
        }
        
        # Enhanced logging with fingerprinting and honeypot details
        logger.info(f"📊 Final Prediction Summary:")
        logger.info(f"   🤖 Bot Decision: {final_decision['is_bot']}")
        logger.info(f"   📊 Combined Confidence: {final_decision['confidence']:.3f}")
        logger.info(f"   🧠 ML: {ml_result.get('bot', False)} (conf: {ml_result.get('confidence', 0):.3f})")
        logger.info(f"   🍯 Honeypot: {honeypot_result['honeypot_verdict']['is_bot']} (threat: {honeypot_result['analysis']['threat_level']}, triggers: {honeypot_result.get('honeypot_summary', {}).get('triggered_honeypots', 0)}/3)")
        logger.info(f"   👆 Fingerprint: {fingerprint_result['verdict']['is_suspicious']} (risk: {fingerprint_result['analysis']['risk_level']})")
        logger.info(f"   🔍 Enhanced Features: WebDriver={browser_fingerprint.get('webdriver_detected', False)}, Plugins={browser_fingerprint.get('plugins_count', 0)}, MIME={browser_fingerprint.get('mime_types_count', 0)}")
        
        # Log honeypot trigger details
        honeypot_triggers = honeypot_result.get('honeypot_results', {}).get('detailed_results', {})
        if honeypot_triggers:
            logger.info(f"   🎯 Honeypot Triggers:")
            for trap_type, details in honeypot_triggers.items():
                if details.get('triggered', False):
                    logger.info(f"     • {trap_type}: {details.get('details', 'Triggered')}")
        
        # Save detailed prediction log with enhanced data
        prediction_log = {
            'timestamp': current_timestamp,
            'client_info': metadata,
            'input_summary': {
                'mouseMoveCount': mouse_move_count,
                'keyPressCount': key_press_count,
                'events_count': len(events)
            },
            'enhanced_fingerprint': {
                'browser_fingerprint': browser_fingerprint,
                'fingerprint_risk_assessment': fingerprint_risk,
                'feature_summary': {
                    'webdriver_detected': browser_fingerprint.get('webdriver_detected', False),
                    'plugins_count': browser_fingerprint.get('plugins_count', 0),
                    'mime_types_count': browser_fingerprint.get('mime_types_count', 0),
                    'suspicious_screen': browser_fingerprint.get('suspicious_screen', False),
                    'suspicious_ua_patterns': browser_fingerprint.get('suspicious_ua_patterns', [])
                }
            },
            'module_results': {
                'ml_model': ml_result,
                'honeypot': honeypot_result,
                'fingerprinting': fingerprint_result
            },
            'final_decision': final_decision,
            'frontend_response': response['prediction'][0]  # Just the main prediction part
        }
        save_prediction(prediction_log)
        
        logger.info("✅ Unified prediction completed successfully")
        return jsonify(response)
    
    except Exception as e:
        logger.error(f"❌ API error: {e}")
        # Return frontend-compatible error response
        return jsonify({
            'ip_address': request.remote_addr,
            'user_agent': request.headers.get('User-Agent'),
            'current_timestamp': datetime.utcnow().isoformat() + 'Z',
            'mouseMoveCount': data.get('mouseMoveCount', 0) if data else 0,
            'keyPressCount': data.get('keyPressCount', 0) if data else 0,
            'prediction': [{
                'bot': True,  # Default to bot on error
                'reconstruction_error': 0.9,
                'confidence': 0.8,
                'raw_error': 500
            }],
            'error': f'API processing error: {str(e)}',
            'api_metadata': {
                'architecture': 'modular_single_api',
                'error_fallback': True
            }
        }), 500

def combine_module_results(ml_result, honeypot_result, fingerprint_result):
    """Combine results from all modules into final decision"""
    try:
        # Extract individual decisions
        ml_bot = ml_result.get('bot', False)
        ml_confidence = ml_result.get('confidence', 0.5)
        
        honeypot_bot = honeypot_result['honeypot_verdict']['is_bot']
        honeypot_confidence = honeypot_result['honeypot_verdict']['confidence']
        
        fingerprint_suspicious = fingerprint_result['verdict']['is_suspicious']
        fingerprint_bot_likely = fingerprint_result['analysis'].get('is_bot_likely', False)
        fingerprint_confidence = fingerprint_result['verdict']['confidence']
        fingerprint_risk_score = fingerprint_result['analysis'].get('risk_score', 0)
        
        # Enhanced weighted decision making with honeypot priority
        # Honeypot detection is most reliable (45%), ML model (35%), fingerprinting (20%)
        # Honeypots get highest weight because they detect definitive bot behavior
        honeypot_weight = 0.45  # Increased from 0.15 - honeypots are most reliable
        ml_weight = 0.35        # Reduced from 0.50 - ML can have false positives
        fingerprint_weight = 0.20  # Reduced from 0.35 - supporting evidence
        
        # Calculate weighted bot probability
        bot_probability = (
            (ml_bot * ml_confidence * ml_weight) +
            (fingerprint_bot_likely * fingerprint_risk_score * fingerprint_weight) +
            (honeypot_bot * honeypot_confidence * honeypot_weight)
        )
        
        # Honeypot trigger bonus - if multiple honeypots triggered, increase probability
        honeypot_summary = honeypot_result.get('honeypot_summary', {})
        triggered_honeypots = honeypot_summary.get('triggered_honeypots', 0)
        
        if triggered_honeypots > 0:
            # Each triggered honeypot adds a bonus
            honeypot_bonus = triggered_honeypots * 0.15  # 15% per triggered honeypot
            bot_probability += honeypot_bonus
            logger.info(f"🍯 Honeypot bonus applied: +{honeypot_bonus:.3f} for {triggered_honeypots} triggers")
        
        # Cap probability at 1.0
        bot_probability = min(bot_probability, 1.0)
        
        # Calculate combined confidence
        combined_confidence = (
            (ml_confidence * ml_weight) +
            (fingerprint_confidence * fingerprint_weight) +
            (honeypot_confidence * honeypot_weight)
        )
        
        # Enhanced decision threshold with fingerprinting consideration
        decision_threshold = 0.4
        
        # Special case: If multiple honeypots triggered, immediate bot detection
        if triggered_honeypots >= 2:
            decision_threshold = 0.1  # Almost guaranteed bot
            logger.info(f"🚨 Multiple honeypots triggered ({triggered_honeypots}/3) - using ultra-sensitive threshold")
        elif triggered_honeypots == 1:
            decision_threshold = 0.25  # Very likely bot
            logger.info(f"🚨 Single honeypot triggered - using sensitive threshold")
        
        # Special case: If fingerprinting detects webdriver or very high risk, lower threshold
        high_risk_indicators = fingerprint_result['analysis'].get('risk_indicators', [])
        if 'webdriver_detected' in high_risk_indicators:
            decision_threshold = min(decision_threshold, 0.2)  # Take minimum of current threshold
            logger.info("🚨 WebDriver detected - using sensitive threshold")
        elif fingerprint_risk_score > 0.8:
            decision_threshold = min(decision_threshold, 0.3)  # Take minimum of current threshold
            logger.info("🚨 High fingerprint risk - using sensitive threshold")
        
        is_bot = bot_probability > decision_threshold
        
        # Determine overall risk level
        if bot_probability > 0.7:
            risk_level = 'high'
        elif bot_probability > 0.4:
            risk_level = 'medium'
        else:
            risk_level = 'low'
        
        return {
            'is_bot': is_bot,
            'confidence': float(combined_confidence),
            'bot_probability': float(bot_probability),
            'risk_level': risk_level,
            'recommendation': 'block' if is_bot else 'allow',
            'decision_threshold': decision_threshold,
            'contributing_factors': {
                'ml_model': {'bot': ml_bot, 'confidence': ml_confidence, 'weight': ml_weight},
                'fingerprinting': {
                    'bot_likely': fingerprint_bot_likely, 
                    'risk_score': fingerprint_risk_score,
                    'confidence': fingerprint_confidence, 
                    'weight': fingerprint_weight,
                    'high_risk_indicators': len([i for i in high_risk_indicators if i in ['webdriver_detected', 'no_plugins', 'no_mime_types']])
                },
                'honeypot': {'bot': honeypot_bot, 'confidence': honeypot_confidence, 'weight': honeypot_weight}
            },
            'decision_logic': f"weighted_probability({bot_probability:.3f}) > adaptive_threshold({decision_threshold}) = {is_bot}"
        }
        
    except Exception as e:
        logger.error(f"❌ Error combining module results: {e}")
        return {
            'is_bot': True,
            'confidence': 0.8,
            'bot_probability': 0.9,
            'risk_level': 'high',
            'recommendation': 'block',
            'decision_logic': f'combination_error: {str(e)}'
        }

@app.route('/analyze/detailed', methods=['POST'])
def detailed_analysis():
    """Detailed analysis endpoint with full module breakdown"""
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        events = data.get('events', [])
        browser_fingerprint = data.get('browserFingerprint', {})
        enhanced_metadata = data.get('metadata', {})
        
        metadata = {
            'ip_address': request.remote_addr,
            'user_agent': request.headers.get('User-Agent'),
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }
        metadata.update(enhanced_metadata)
        
        # Run all modules with enhanced data
        ml_result = ml_module.predict(events)
        honeypot_result = honeypot_module.analyze_behavior(events, metadata)
        fingerprint_result = fingerprinting_module.analyze_fingerprint(metadata, browser_fingerprint)
        final_decision = combine_module_results(ml_result, honeypot_result, fingerprint_result)
        
        return jsonify({
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'input_analysis': {
                'events_count': len(events),
                'metadata': metadata,
                'browser_fingerprint_features': len(browser_fingerprint),
                'enhanced_features': {
                    'webdriver_detected': browser_fingerprint.get('webdriver_detected', False),
                    'plugins_count': browser_fingerprint.get('plugins_count', 0),
                    'mime_types_count': browser_fingerprint.get('mime_types_count', 0),
                    'suspicious_patterns': browser_fingerprint.get('suspicious_ua_patterns', [])
                }
            },
            'module_results': {
                'ml_model': ml_result,
                'honeypot': honeypot_result,
                'enhanced_fingerprinting': fingerprint_result
            },
            'combined_analysis': final_decision,
            'api_info': {
                'architecture': 'modular_single_api_enhanced',
                'version': '3.1',
                'fingerprinting_features': 'rule_based_enhanced'
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/predictions', methods=['GET'])
def get_predictions():
    """Get stored predictions transformed for admin page"""
    try:
        if PREDICTIONS_FILE.exists():
            with open(PREDICTIONS_FILE, 'r') as f:
                raw_predictions = json.load(f)
            
            # Transform data to match admin page expectations
            transformed_predictions = []
            for pred in raw_predictions:
                try:
                    # Extract ML model results
                    ml_result = pred.get('module_results', {}).get('ml_model', {})
                    fingerprinting_result = pred.get('module_results', {}).get('fingerprinting', {})
                    
                    # Extract fingerprinting data
                    browser_features = None
                    fingerprint_risk = None
                    
                    if fingerprinting_result:
                        analysis = fingerprinting_result.get('analysis', {})
                        browser_features = {
                            'webdriver': analysis.get('webdriver_detected', False),
                            'plugins': analysis.get('plugins_count', 0),
                            'mimeTypes': analysis.get('mime_types_count', 0),
                            'screenSize': f"{analysis.get('screen_width', 0)}x{analysis.get('screen_height', 0)}",
                            'touchPoints': analysis.get('max_touch_points', 0),
                            'suspiciousPatterns': analysis.get('suspicious_ua_patterns', [])
                        }
                        
                        fingerprint_risk = {
                            'riskLevel': analysis.get('risk_level', 'unknown'),
                            'riskScore': analysis.get('risk_score', 0),
                            'isBot': analysis.get('is_bot', False),
                            'riskFactors': analysis.get('risk_factors', [])
                        }
                    
                    # Extract honeypot results
                    honeypot_result = pred.get('module_results', {}).get('honeypot', {})
                    honeypot_analysis = None
                    
                    if honeypot_result:
                        honeypot_analysis = {
                            'threat_detected': honeypot_result.get('honeypot_verdict', {}).get('is_bot', False),
                            'threat_level': honeypot_result.get('analysis', {}).get('threat_level', 'low'),
                            'honeypot_score': honeypot_result.get('analysis', {}).get('honeypot_score', 0),
                            'confidence': honeypot_result.get('honeypot_verdict', {}).get('confidence', 0.5),
                            'honeypot_summary': honeypot_result.get('honeypot_summary', {}),
                            'honeypot_details': honeypot_result.get('honeypot_results', {}),
                            'detection_method': 'enhanced_3_layer_honeypot'
                        }
                    
                    # Extract final verdict
                    final_verdict = pred.get('final_decision', {})
                    
                    transformed_entry = {
                        'ipAddress': pred.get('client_info', {}).get('ip_address', 'Unknown'),
                        'userAgent': pred.get('client_info', {}).get('user_agent', 'Unknown'),
                        'timestamp': pred.get('timestamp', pred.get('client_info', {}).get('timestamp', '')),
                        'mouseMoveCount': pred.get('input_summary', {}).get('mouseMoveCount', 0),
                        'keyPressCount': pred.get('input_summary', {}).get('keyPressCount', 0),
                        'isBot': final_verdict.get('is_bot', ml_result.get('bot', False)),
                        'prediction': [{
                            'bot': final_verdict.get('is_bot', ml_result.get('bot', False)),
                            'reconstruction_error': ml_result.get('reconstruction_error', 0)
                        }],
                        # Add enhanced analysis for admin panel
                        'enhanced_analysis': {
                            'final_verdict': final_verdict,
                            'honeypot_analysis': honeypot_analysis,
                            'ml_analysis': {
                                'bot_detected': ml_result.get('bot', False),
                                'reconstruction_error': ml_result.get('reconstruction_error', 0),
                                'confidence': ml_result.get('confidence', 0.5)
                            }
                        },
                        'browserFeatures': browser_features,
                        'fingerprintRisk': fingerprint_risk
                    }
                    
                    transformed_predictions.append(transformed_entry)
                except Exception as e:
                    logger.warning(f"Error transforming prediction: {e}")
                    continue
            
            return jsonify(transformed_predictions[-50:][::-1])  # Last 50 predictions, newest first
        else:
            return jsonify([])
    except Exception as e:
        logger.error(f"Error getting predictions: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/modules/info')
def modules_info():
    """Get information about all modules"""
    return jsonify({
        'api': 'unified_bot_detection',
        'architecture': 'modular_single_api',
        'modules': {
            'ml_model': ml_module.get_info(),
            'honeypot': honeypot_module.get_info(),
            'fingerprinting': fingerprinting_module.get_info()
        }
    })

if __name__ == '__main__':
    print("🚀 Starting Unified Bot Detection API...")
    print("📋 Architecture: Modular Single API")
    print("🧩 Modules: ML Model, Honeypot, Fingerprinting")
    print("🔗 Main endpoints:")
    print("   POST /predict - Main prediction endpoint (frontend compatible)")
    print("   POST /analyze/detailed - Detailed analysis")
    print("   GET  /health - Health check")
    print("   GET  /modules/info - Module information")
    print("   GET  /predictions - Recent predictions")
    app.run(debug=True, host='0.0.0.0', port=5000)
