# Honeypot Service - Advanced Bot Detection and Honeypot Analysis
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
LOGS_DIR = BASE_DIR / 'logs' / 'honeypot'
LOGS_DIR.mkdir(parents=True, exist_ok=True)

class HoneypotAnalyzer:
    """Advanced honeypot analysis for sophisticated bot detection"""
    
    def __init__(self):
        self.suspicious_patterns = {
            'mouse_speed_threshold': 1000,
            'click_interval_threshold': 0.05,
            'straight_line_threshold': 0.8,
            'variance_threshold': 10
        }
    
    def analyze_behavioral_patterns(self, events):
        """Comprehensive behavioral analysis"""
        try:
            if len(events) < 3:
                return {
                    'is_suspicious': True,
                    'reason': 'insufficient_data',
                    'threat_level': 'medium',
                    'honeypot_score': 0.7
                }
            
            # Extract mouse events
            mouse_events = [e for e in events if 'x_position' in e and 'y_position' in e]
            
            if len(mouse_events) < 2:
                return {
                    'is_suspicious': True,
                    'reason': 'no_mouse_interaction',
                    'threat_level': 'high',
                    'honeypot_score': 0.9
                }
            
            # Analyze multiple threat vectors
            threat_indicators = []
            
            # 1. Speed Analysis
            speed_analysis = self._analyze_speed_patterns(mouse_events)
            if speed_analysis['suspicious']:
                threat_indicators.extend(speed_analysis['indicators'])
            
            # 2. Timing Analysis
            timing_analysis = self._analyze_timing_patterns(events)
            if timing_analysis['suspicious']:
                threat_indicators.extend(timing_analysis['indicators'])
            
            # 3. Movement Pattern Analysis
            movement_analysis = self._analyze_movement_patterns(mouse_events)
            if movement_analysis['suspicious']:
                threat_indicators.extend(movement_analysis['indicators'])
            
            # 4. Honeypot-specific triggers
            honeypot_triggers = self._check_honeypot_triggers(events)
            if honeypot_triggers['triggered']:
                threat_indicators.extend(honeypot_triggers['triggers'])
            
            # Calculate overall threat assessment
            total_indicators = len(threat_indicators)
            honeypot_score = min(total_indicators / 10.0, 1.0)  # Changed: More indicators needed for higher score
            
            # Determine threat level (Changed: Default to low, higher thresholds)
            if honeypot_score >= 0.7:  # Changed from 0.8
                threat_level = 'critical'
            elif honeypot_score >= 0.5:  # Changed from 0.5
                threat_level = 'high'
            elif honeypot_score >= 0.3:  # Changed from 0.3
                threat_level = 'medium'
            else:
                threat_level = 'low'  # Default to low
            
            return {
                'is_suspicious': honeypot_score > 0.4,  # Changed threshold from 0.3 to 0.4
                'threat_level': threat_level,
                'honeypot_score': float(honeypot_score),
                'threat_indicators': threat_indicators,
                'detailed_analysis': {
                    'speed': speed_analysis,
                    'timing': timing_analysis,
                    'movement': movement_analysis,
                    'honeypot_triggers': honeypot_triggers
                },
                'confidence': min(honeypot_score * 1.5, 1.0)
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'is_suspicious': True,
                'threat_level': 'unknown',
                'honeypot_score': 1.0
            }
    
    def _analyze_speed_patterns(self, mouse_events):
        """Analyze mouse speed patterns for bot detection"""
        try:
            speeds = []
            for i in range(1, len(mouse_events)):
                prev = mouse_events[i-1]
                curr = mouse_events[i]
                
                time_diff = (curr['timestamp'] - prev['timestamp']) / 1000.0
                if time_diff > 0:
                    distance = np.sqrt((curr['x_position'] - prev['x_position'])**2 + 
                                     (curr['y_position'] - prev['y_position'])**2)
                    speed = distance / time_diff
                    speeds.append(speed)
            
            if not speeds:
                return {'suspicious': True, 'indicators': ['no_movement'], 'metrics': {}}
            
            avg_speed = np.mean(speeds)
            speed_variance = np.var(speeds)
            max_speed = np.max(speeds)
            
            indicators = []
            
            # Bot-like speed patterns
            if speed_variance < self.suspicious_patterns['variance_threshold']:
                indicators.append('uniform_speed')
            
            if max_speed > self.suspicious_patterns['mouse_speed_threshold']:
                indicators.append('superhuman_speed')
            
            if avg_speed > 500:  # Very fast average
                indicators.append('suspicious_avg_speed')
            
            return {
                'suspicious': len(indicators) > 0,
                'indicators': indicators,
                'metrics': {
                    'avg_speed': float(avg_speed),
                    'max_speed': float(max_speed),
                    'speed_variance': float(speed_variance)
                }
            }
        except:
            return {'suspicious': True, 'indicators': ['speed_analysis_error'], 'metrics': {}}
    
    def _analyze_timing_patterns(self, events):
        """Analyze timing patterns for automation detection"""
        try:
            timestamps = [e['timestamp'] for e in events]
            intervals = [timestamps[i] - timestamps[i-1] for i in range(1, len(timestamps))]
            
            if not intervals:
                return {'suspicious': True, 'indicators': ['no_intervals'], 'metrics': {}}
            
            avg_interval = np.mean(intervals)
            interval_variance = np.var(intervals)
            
            indicators = []
            
            # Too regular intervals (automation)
            if interval_variance < 100:
                indicators.append('robotic_timing')
            
            # Suspiciously fast interactions
            fast_count = sum(1 for i in intervals if i < 50)
            if fast_count > len(intervals) * 0.4:
                indicators.append('inhuman_reaction_time')
            
            # Perfect intervals (script-like)
            if len(set(intervals)) < len(intervals) * 0.3:
                indicators.append('repetitive_intervals')
            
            return {
                'suspicious': len(indicators) > 0,
                'indicators': indicators,
                'metrics': {
                    'avg_interval': float(avg_interval),
                    'interval_variance': float(interval_variance),
                    'fast_interactions': fast_count
                }
            }
        except:
            return {'suspicious': True, 'indicators': ['timing_analysis_error'], 'metrics': {}}
    
    def _analyze_movement_patterns(self, mouse_events):
        """Analyze movement patterns for non-human behavior"""
        try:
            if len(mouse_events) < 3:
                return {'suspicious': True, 'indicators': ['insufficient_movement'], 'metrics': {}}
            
            indicators = []
            
            # Check for straight lines
            straight_lines = 0
            for i in range(2, len(mouse_events)):
                if self._is_perfect_line(mouse_events[i-2:i+1]):
                    straight_lines += 1
            
            straight_ratio = straight_lines / max(len(mouse_events) - 2, 1)
            if straight_ratio > self.suspicious_patterns['straight_line_threshold']:
                indicators.append('too_many_straight_lines')
            
            # Check for teleportation (instant jumps)
            teleports = 0
            for i in range(1, len(mouse_events)):
                prev = mouse_events[i-1]
                curr = mouse_events[i]
                distance = np.sqrt((curr['x_position'] - prev['x_position'])**2 + 
                                 (curr['y_position'] - prev['y_position'])**2)
                time_diff = (curr['timestamp'] - prev['timestamp']) / 1000.0
                
                if distance > 200 and time_diff < 0.1:  # Large jump in short time
                    teleports += 1
            
            if teleports > len(mouse_events) * 0.2:
                indicators.append('mouse_teleportation')
            
            return {
                'suspicious': len(indicators) > 0,
                'indicators': indicators,
                'metrics': {
                    'straight_line_ratio': float(straight_ratio),
                    'teleportation_events': teleports
                }
            }
        except:
            return {'suspicious': True, 'indicators': ['movement_analysis_error'], 'metrics': {}}
    
    def _check_honeypot_triggers(self, events):
        """Check for honeypot-specific trigger conditions"""
        try:
            triggers = []
            
            # Check for interaction with invisible elements (honeypot trap)
            invisible_interactions = sum(1 for e in events if e.get('element_visible', True) == False)
            if invisible_interactions > 0:
                triggers.append('invisible_element_interaction')
            
            # Check for form filling without focus events
            form_fills = sum(1 for e in events if e.get('event_name') == 'input')
            focus_events = sum(1 for e in events if e.get('event_name') == 'focus')
            
            if form_fills > 0 and focus_events == 0:
                triggers.append('form_filling_without_focus')
            
            # Check for rapid-fire submissions
            submit_events = [e for e in events if e.get('event_name') == 'submit']
            if len(submit_events) > 1:
                submit_intervals = [submit_events[i]['timestamp'] - submit_events[i-1]['timestamp'] 
                                  for i in range(1, len(submit_events))]
                if any(interval < 1000 for interval in submit_intervals):  # Less than 1 second
                    triggers.append('rapid_submissions')
            
            return {
                'triggered': len(triggers) > 0,
                'triggers': triggers,
                'metrics': {
                    'invisible_interactions': invisible_interactions,
                    'form_fills': form_fills,
                    'focus_events': focus_events
                }
            }
        except:
            return {'triggered': True, 'triggers': ['honeypot_check_error'], 'metrics': {}}
    
    def _is_perfect_line(self, points):
        """Check if points form a perfectly straight line (bot behavior)"""
        if len(points) != 3:
            return False
        
        p1, p2, p3 = points
        cross_product = ((p2['x_position'] - p1['x_position']) * (p3['y_position'] - p1['y_position']) - 
                        (p3['x_position'] - p1['x_position']) * (p2['y_position'] - p1['y_position']))
        
        return abs(cross_product) < 1  # Very tight tolerance for perfect lines

# Initialize analyzer
honeypot_analyzer = HoneypotAnalyzer()

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy', 
        'service': 'honeypot',
        'analyzer': 'active',
        'version': '2.0',
        'capabilities': ['behavioral_analysis', 'threat_detection', 'honeypot_triggers']
    })

@app.route('/analyze', methods=['POST'])
def analyze():
    """Advanced honeypot analysis for bot detection"""
    try:
        data = request.json
        print(f"🍯 Honeypot analysis started")
        
        if not data or 'events' not in data:
            return jsonify({'error': 'Events data required for honeypot analysis'}), 400
        
        events = data['events']
        metadata = data.get('metadata', {})
        
        # Perform comprehensive honeypot analysis
        analysis_result = honeypot_analyzer.analyze_behavioral_patterns(events)
        
        # Enhance with metadata
        client_ip = metadata.get('ip_address', 'unknown')
        user_agent = metadata.get('user_agent', 'unknown')
        
        result = {
            'service': 'honeypot',
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'analysis': analysis_result,
            'client_info': {
                'ip_address': client_ip,
                'user_agent': user_agent,
                'events_analyzed': len(events)
            },
            'honeypot_verdict': {
                'is_bot': analysis_result.get('is_suspicious', True),
                'threat_level': analysis_result.get('threat_level', 'unknown'),
                'confidence': analysis_result.get('confidence', 0.5),
                'recommended_action': 'block' if analysis_result.get('honeypot_score', 0) > 0.7 else 'monitor'
            }
        }
        
        # Log the analysis
        log_file = LOGS_DIR / 'honeypot_analysis.json'
        try:
            if log_file.exists():
                with open(log_file, 'r') as f:
                    existing_logs = json.load(f)
            else:
                existing_logs = []
            
            existing_logs.append(result)
            
            # Keep only last 1000 entries
            if len(existing_logs) > 1000:
                existing_logs = existing_logs[-1000:]
            
            with open(log_file, 'w') as f:
                json.dump(existing_logs, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not log honeypot analysis: {e}")
        
        threat_emoji = "🚨" if analysis_result.get('threat_level') == 'critical' else "⚠️" if analysis_result.get('is_suspicious') else "✅"
        print(f"{threat_emoji} Honeypot analysis complete: {analysis_result.get('threat_level', 'unknown').upper()}")
        
        return jsonify(result)
    
    except Exception as e:
        print(f"❌ Honeypot analysis error: {e}")
        return jsonify({
            'error': str(e),
            'service': 'honeypot'
        }), 500

@app.route('/threats', methods=['GET'])
def get_threats():
    """Get detected threats and statistics"""
    try:
        log_file = LOGS_DIR / 'honeypot_analysis.json'
        
        if not log_file.exists():
            return jsonify({
                'service': 'honeypot',
                'total_analyses': 0,
                'threats': [],
                'statistics': {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
            })
        
        with open(log_file, 'r') as f:
            logs = json.load(f)
        
        # Get recent threats
        recent_threats = [log for log in logs if log.get('analysis', {}).get('is_suspicious', False)][-20:]
        
        # Calculate statistics
        threat_levels = [log.get('analysis', {}).get('threat_level', 'unknown') for log in logs]
        stats = {
            'critical': threat_levels.count('critical'),
            'high': threat_levels.count('high'),
            'medium': threat_levels.count('medium'),
            'low': threat_levels.count('low')
        }
        
        return jsonify({
            'service': 'honeypot',
            'total_analyses': len(logs),
            'threats': recent_threats,
            'statistics': stats,
            'threat_percentage': (len(recent_threats) / len(logs) * 100) if logs else 0
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Honeypot Service...")
    print("🍯 Advanced Bot Detection & Threat Analysis Active")
    print(f"📁 Logs directory: {LOGS_DIR}")
    app.run(debug=True, host='0.0.0.0', port=5001)
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
