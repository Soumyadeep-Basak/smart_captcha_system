# Bot Detection Service - Behavioral Analysis
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import json
import numpy as np
from pathlib import Path

app = Flask(__name__)
CORS(app)

# Path configuration
BASE_DIR = Path(__file__).parent.parent.parent
LOGS_DIR = BASE_DIR / 'logs' / 'bot_detection'
LOGS_DIR.mkdir(parents=True, exist_ok=True)

class BehaviorAnalyzer:
    """Analyze behavioral patterns for bot detection"""
    
    def __init__(self):
        self.human_patterns = {
            'mouse_speed_range': (0.1, 2.0),
            'click_intervals': (0.2, 3.0),
            'typing_speed_range': (0.05, 0.5),
            'pause_patterns': True
        }
    
    def analyze_mouse_patterns(self, events):
        """Analyze mouse movement patterns"""
        try:
            mouse_events = [e for e in events if 'x_position' in e and 'y_position' in e]
            
            if len(mouse_events) < 2:
                return {'suspicious': True, 'reason': 'insufficient_mouse_data'}
            
            # Calculate movement characteristics
            speeds = []
            for i in range(1, len(mouse_events)):
                prev = mouse_events[i-1]
                curr = mouse_events[i]
                
                time_diff = (curr['timestamp'] - prev['timestamp']) / 1000.0  # Convert to seconds
                if time_diff > 0:
                    distance = np.sqrt((curr['x_position'] - prev['x_position'])**2 + 
                                     (curr['y_position'] - prev['y_position'])**2)
                    speed = distance / time_diff
                    speeds.append(speed)
            
            if not speeds:
                return {'suspicious': True, 'reason': 'no_mouse_movement'}
            
            avg_speed = np.mean(speeds)
            speed_variance = np.var(speeds)
            
            # Check for bot-like patterns
            suspicious_indicators = []
            
            # Too consistent speed (bots often have uniform movement)
            if speed_variance < 10:
                suspicious_indicators.append('uniform_speed')
            
            # Extremely high speed
            if avg_speed > 1000:
                suspicious_indicators.append('inhuman_speed')
            
            # Perfect straight lines
            straight_movements = sum(1 for i in range(2, len(mouse_events)) 
                                   if self._is_straight_line(mouse_events[i-2:i+1]))
            
            if straight_movements > len(mouse_events) * 0.8:
                suspicious_indicators.append('too_many_straight_lines')
            
            return {
                'suspicious': len(suspicious_indicators) > 0,
                'indicators': suspicious_indicators,
                'metrics': {
                    'avg_speed': float(avg_speed),
                    'speed_variance': float(speed_variance),
                    'total_movements': len(speeds)
                }
            }
            
        except Exception as e:
            return {'error': str(e), 'suspicious': True}
    
    def _is_straight_line(self, points):
        """Check if 3 points form a straight line"""
        if len(points) != 3:
            return False
        
        p1, p2, p3 = points
        # Calculate cross product to check collinearity
        cross_product = ((p2['x_position'] - p1['x_position']) * (p3['y_position'] - p1['y_position']) - 
                        (p3['x_position'] - p1['x_position']) * (p2['y_position'] - p1['y_position']))
        
        return abs(cross_product) < 5  # Small tolerance for floating point errors
    
    def analyze_timing_patterns(self, events):
        """Analyze timing patterns for bot detection"""
        try:
            if len(events) < 2:
                return {'suspicious': True, 'reason': 'insufficient_timing_data'}
            
            timestamps = [e['timestamp'] for e in events]
            intervals = [timestamps[i] - timestamps[i-1] for i in range(1, len(timestamps))]
            
            if not intervals:
                return {'suspicious': True, 'reason': 'no_intervals'}
            
            avg_interval = np.mean(intervals)
            interval_variance = np.var(intervals)
            
            suspicious_indicators = []
            
            # Too regular intervals (bots often have precise timing)
            if interval_variance < 100:  # Very low variance in milliseconds
                suspicious_indicators.append('regular_intervals')
            
            # Extremely fast interactions
            fast_intervals = sum(1 for interval in intervals if interval < 50)  # Less than 50ms
            if fast_intervals > len(intervals) * 0.3:
                suspicious_indicators.append('superhuman_speed')
            
            return {
                'suspicious': len(suspicious_indicators) > 0,
                'indicators': suspicious_indicators,
                'metrics': {
                    'avg_interval': float(avg_interval),
                    'interval_variance': float(interval_variance),
                    'fast_interactions': fast_intervals
                }
            }
            
        except Exception as e:
            return {'error': str(e), 'suspicious': True}

# Initialize analyzer
behavior_analyzer = BehaviorAnalyzer()

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy', 
        'service': 'bot_detection',
        'analyzer': 'ready',
        'version': '1.0'
    })

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze behavioral patterns for bot detection"""
    try:
        data = request.json
        print(f"📊 Bot detection analysis started")
        
        if not data or 'events' not in data:
            return jsonify({'error': 'Events data required'}), 400
        
        events = data['events']
        metadata = data.get('metadata', {})
        
        # Perform behavioral analysis
        mouse_analysis = behavior_analyzer.analyze_mouse_patterns(events)
        timing_analysis = behavior_analyzer.analyze_timing_patterns(events)
        
        # Combine results
        all_indicators = []
        if mouse_analysis.get('suspicious'):
            all_indicators.extend(mouse_analysis.get('indicators', []))
        if timing_analysis.get('suspicious'):
            all_indicators.extend(timing_analysis.get('indicators', []))
        
        # Calculate overall suspicion score
        suspicion_score = len(all_indicators) / 6.0  # Normalize to 0-1
        suspicion_score = min(suspicion_score, 1.0)
        
        # Determine final classification
        is_bot_behavior = suspicion_score > 0.3
        
        result = {
            'service': 'bot_detection',
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'analysis': {
                'is_bot_behavior': is_bot_behavior,
                'suspicion_score': float(suspicion_score),
                'indicators': all_indicators,
                'confidence': min(suspicion_score * 2, 1.0)  # Confidence based on score
            },
            'detailed_analysis': {
                'mouse_patterns': mouse_analysis,
                'timing_patterns': timing_analysis
            },
            'metadata': {
                'events_analyzed': len(events),
                'analysis_method': 'behavioral_patterns'
            }
        }
        
        # Save analysis for future reference
        analysis_file = LOGS_DIR / 'behavior_analysis.json'
        try:
            if analysis_file.exists():
                with open(analysis_file, 'r') as f:
                    existing_data = json.load(f)
            else:
                existing_data = []
            
            existing_data.append(result)
            
            with open(analysis_file, 'w') as f:
                json.dump(existing_data, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save analysis: {e}")
        
        print(f"✅ Bot detection analysis complete: {'BOT' if is_bot_behavior else 'HUMAN'}")
        return jsonify(result)
    
    except Exception as e:
        print(f"❌ Bot detection error: {e}")
        return jsonify({
            'error': str(e),
            'service': 'bot_detection'
        }), 500

@app.route('/patterns', methods=['GET'])
def get_patterns():
    """Get analyzed behavior patterns"""
    try:
        analysis_file = LOGS_DIR / 'behavior_analysis.json'
        
        if analysis_file.exists():
            with open(analysis_file, 'r') as f:
                data = json.load(f)
            
            return jsonify({
                'service': 'bot_detection',
                'total_analyses': len(data),
                'patterns': data[-10:]  # Return last 10 analyses
            })
        else:
            return jsonify({
                'service': 'bot_detection',
                'total_analyses': 0,
                'patterns': []
            })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/stats', methods=['GET'])
def get_stats():
    """Get detection statistics"""
    try:
        analysis_file = LOGS_DIR / 'behavior_analysis.json'
        
        if not analysis_file.exists():
            return jsonify({
                'service': 'bot_detection',
                'stats': {'total': 0, 'bots': 0, 'humans': 0}
            })
        
        with open(analysis_file, 'r') as f:
            data = json.load(f)
        
        total = len(data)
        bots = sum(1 for item in data if item.get('analysis', {}).get('is_bot_behavior', False))
        humans = total - bots
        
        return jsonify({
            'service': 'bot_detection',
            'stats': {
                'total': total,
                'bots': bots,
                'humans': humans,
                'bot_percentage': (bots / total * 100) if total > 0 else 0
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Bot Detection Service...")
    print(f"📁 Logs directory: {LOGS_DIR}")
    app.run(debug=True, host='0.0.0.0', port=5001)
