# Fingerprinting Service - Enhanced Browser & Environment Analysis
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import json
import hashlib
import os
from pathlib import Path
import sys

app = Flask(__name__)
CORS(app)

# Import our enhanced fingerprinting module
sys.path.append(str(Path(__file__).parent.parent.parent / 'api' / 'modules'))
from fingerprinting import FingerprintingAnalyzer

# Path configuration
BASE_DIR = Path(__file__).parent.parent.parent
LOGS_DIR = BASE_DIR / 'logs' / 'fingerprinting'
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# Initialize enhanced analyzer
fingerprint_analyzer = FingerprintingAnalyzer()

@app.route('/health') 
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'fingerprinting',
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'version': '2.0.0-enhanced'
    })

@app.route('/analyze', methods=['POST'])
def analyze():
    """Enhanced fingerprint analysis for bot detection"""
    try:
        data = request.json
        print(f"👆 Enhanced fingerprinting analysis started")
        
        # Extract request information
        client_ip = request.remote_addr
        user_agent = request.headers.get('User-Agent', '')
        headers = dict(request.headers)
        
        # Extract browser fingerprint data from request
        browser_fingerprint = data.get('browserFingerprint', {})
        fingerprint_risk = data.get('fingerprintRisk', {})
        
        # If metadata provided, use it
        if data and 'metadata' in data:
            metadata = data['metadata']
            user_agent = metadata.get('user_agent', user_agent)
        
        # Perform enhanced fingerprint analysis
        analysis_result = fingerprint_analyzer.analyze_fingerprint(
            browser_fingerprint, 
            client_ip, 
            user_agent
        )
        
        # Calculate enhanced patterns
        analysis_patterns = {
            'automationDetected': analysis_result.get('automation_detected', False),
            'zeroFeaturesDetected': analysis_result.get('zero_features_detected', False),
            'zeroFeaturesList': analysis_result.get('zero_features_list', []),
            'canvasSignature': analysis_result.get('canvas_signature'),
            'canvasDuplicate': analysis_result.get('canvas_duplicate', False),
            'timingAnalysis': analysis_result.get('timing_analysis', {}),
            'behavioralConsistency': analysis_result.get('behavioral_consistency', {})
        }
        
        # Prepare enhanced browser features for admin display
        enhanced_browser_features = {
            **browser_fingerprint,
            'automationSignatures': analysis_result.get('automation_signatures', []),
            'suspiciousPatterns': analysis_result.get('suspicious_patterns', []),
            'canvasSupported': browser_fingerprint.get('canvas_supported', True),
            'webglSupported': browser_fingerprint.get('webgl_supported', True),
            'webglVendor': browser_fingerprint.get('webgl_vendor', ''),
            'webglRenderer': browser_fingerprint.get('webgl_renderer', ''),
            'fonts': browser_fingerprint.get('fonts_detected', 0)
        }
        
        result = {
            'service': 'fingerprinting',
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'analysis': analysis_result,
            'analysisPatterns': analysis_patterns,
            'browserFeatures': enhanced_browser_features,
            'fingerprintRisk': fingerprint_risk,
            'client_info': {
                'ip_address': client_ip,
                'user_agent': user_agent,
                'headers_analyzed': len(headers)
            },
            'risk_score': analysis_result.get('risk_score', 0.5),
            'prediction': 'bot' if analysis_result.get('risk_score', 0.5) > 0.7 else 'human',
            'confidence': analysis_result.get('confidence', 0.8)
        }
        
        # Log the enhanced analysis
        log_file = LOGS_DIR / 'enhanced_analysis.json'
        try:
            if log_file.exists():
                with open(log_file, 'r') as f:
                    existing_logs = json.load(f)
            else:
                existing_logs = []
            
            existing_logs.append(result)
            
            # Keep only last 500 entries
            if len(existing_logs) > 500:
                existing_logs = existing_logs[-500:]
            
            with open(log_file, 'w') as f:
                json.dump(existing_logs, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not log enhanced analysis: {e}")
        
        status_emoji = "🚨" if result['prediction'] == 'bot' else "✅"
        risk_percentage = f"{result['risk_score'] * 100:.1f}%"
        print(f"{status_emoji} Enhanced analysis complete - Risk: {risk_percentage}")
        
        return jsonify(result)
    
    except Exception as e:
        print(f"❌ Enhanced fingerprinting error: {e}")
        return jsonify({
            'error': str(e),
            'service': 'fingerprinting',
            'analysis': {},
            'analysisPatterns': {},
            'browserFeatures': {},
            'risk_score': 1.0,
            'prediction': 'bot'
        }), 500
        return jsonify({
            'error': str(e),
            'service': 'fingerprinting'
        }), 500

@app.route('/fingerprints', methods=['GET'])
def get_fingerprints():
    """Get fingerprint analysis history"""
    try:
        log_file = LOGS_DIR / 'fingerprint_analysis.json'
        
        if not log_file.exists():
            return jsonify({
                'service': 'fingerprinting',
                'total': 0,
                'fingerprints': []
            })
        
        with open(log_file, 'r') as f:
            logs = json.load(f)
        
        return jsonify({
            'service': 'fingerprinting',
            'total': len(logs),
            'fingerprints': logs[-20:]  # Return last 20
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/stats', methods=['GET'])
def get_stats():
    """Get fingerprinting statistics"""
    try:
        log_file = LOGS_DIR / 'fingerprint_analysis.json'
        
        if not log_file.exists():
            return jsonify({
                'service': 'fingerprinting',
                'stats': {'total': 0, 'suspicious': 0, 'clean': 0}
            })
        
        with open(log_file, 'r') as f:
            logs = json.load(f)
        
        total = len(logs)
        suspicious = sum(1 for log in logs if log.get('analysis', {}).get('is_suspicious', False))
        clean = total - suspicious
        
        return jsonify({
            'service': 'fingerprinting',
            'stats': {
                'total': total,
                'suspicious': suspicious,
                'clean': clean,
                'suspicious_percentage': (suspicious / total * 100) if total > 0 else 0
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Fingerprinting Service...")
    print("👆 Browser & Environment Analysis Active")
    print(f"📁 Logs directory: {LOGS_DIR}")
    app.run(debug=True, host='0.0.0.0', port=5003)
