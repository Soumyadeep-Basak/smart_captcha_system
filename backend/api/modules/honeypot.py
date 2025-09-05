"""
Enhanced Honeypot Module for Advanced Bot Detection

This module implements a sophisticated 3-layer honeypot system:
1. Hidden CSS field - Only bots can see and fill this field
2. Fake submit button - Invisible duplicate button that only bots click
3. JS-based optional field - Bots without JS execution will fill this

Author: Bot Detection System
Version: 2.0
"""

from datetime import datetime
import json
import re

class HoneypotModule:
    """Enhanced honeypot detection with multiple trap mechanisms"""
    
    def __init__(self):
        self.module_name = 'enhanced_honeypot'
        self.version = '2.0'
        
        # Honeypot weights for scoring (total should equal 1.0)
        self.honeypot_weights = {
            'hidden_field': 0.4,     # Strongest indicator - only bots should see this
            'fake_submit': 0.3,      # Strong indicator - invisible to humans
            'optional_field': 0.3    # Moderate indicator - JS-based detection
        }
        
        # Thresholds
        self.suspicious_threshold = 0.3  # Lower threshold for honeypot-based detection
        self.high_threat_threshold = 0.6
        
        print(f"🍯 Enhanced Honeypot Module v{self.version} initialized")
        print(f"🎯 Honeypot mechanisms: {list(self.honeypot_weights.keys())}")
    
    def analyze(self, events, metadata=None):
        """
        Perform enhanced honeypot analysis with 3-layer detection
        
        Args:
            events: List of user interaction events
            metadata: Additional request metadata
            
        Returns:
            Enhanced analysis result with honeypot details
        """
        try:
            if metadata is None:
                metadata = {}
            
            print(f"🔍 Starting enhanced honeypot analysis...")
            print(f"📊 Events received: {len(events)}")
            
            # Primary: Analyze honeypot triggers
            honeypot_results = self._analyze_honeypots(events, metadata)
            honeypot_score = honeypot_results['total_score']
            
            # Secondary: Traditional behavioral analysis (lower weight)
            timing_score, timing_indicators = self._analyze_timing(events)
            movement_score, movement_indicators = self._analyze_movement(events)
            metadata_score, metadata_indicators = self._analyze_metadata(metadata)
            
            # Combine scores with honeypot priority
            behavioral_score = (timing_score + movement_score + metadata_score) / 10.0  # Normalize
            total_score = (honeypot_score * 0.8) + (behavioral_score * 0.2)  # Prioritize honeypots
            
            # Collect all indicators
            threat_indicators = honeypot_results['indicators'] + timing_indicators + movement_indicators + metadata_indicators
            
            # Determine threat level based on total score
            if total_score >= 0.8:
                threat_level = 'critical'
            elif total_score >= 0.6:
                threat_level = 'high'
            elif total_score >= 0.3:
                threat_level = 'medium'
            else:
                threat_level = 'low'
            
            is_bot = total_score >= self.suspicious_threshold
            
            result = self._create_enhanced_analysis_result(
                total_score, threat_level, threat_indicators, is_bot, honeypot_results
            )
            
            print(f"🍯 Honeypot Analysis Complete:")
            print(f"   • Honeypot Score: {honeypot_score:.3f}")
            print(f"   • Total Score: {total_score:.3f}")
            print(f"   • Threat Level: {threat_level}")
            print(f"   • Bot Detected: {is_bot}")
            print(f"   • Honeypots Triggered: {honeypot_results['honeypots_triggered']}/3")
            
            return result
            
        except Exception as e:
            print(f"❌ Enhanced honeypot analysis error: {e}")
            return self._create_error_result(str(e))
    
    def _analyze_honeypots(self, events, metadata):
        """
        Analyze the 3 honeypot mechanisms for bot detection
        
        Returns detailed honeypot analysis with individual scores
        """
        indicators = []
        total_score = 0.0
        
        # Initialize detailed results for each honeypot
        detailed_results = {
            'hidden_field': {'triggered': False, 'score': 0.0, 'details': ''},
            'fake_submit': {'triggered': False, 'score': 0.0, 'details': ''},
            'optional_field': {'triggered': False, 'score': 0.0, 'details': ''}
        }
        
        # 1. Hidden CSS Field Detection (Weight: 0.4)
        hidden_field_value = metadata.get('hidden_honeypot_field', '')
        if hidden_field_value and hidden_field_value.strip():
            detailed_results['hidden_field'] = {
                'triggered': True,
                'score': 1.0,
                'details': f'Hidden field filled with: {hidden_field_value[:50]}...'
            }
            total_score += self.honeypot_weights['hidden_field']
            indicators.append('hidden_field_filled')
            print("🎯 HONEYPOT TRIGGERED: Hidden CSS field was filled")
        
        # 2. Fake Submit Button Detection (Weight: 0.3)
        fake_submit_clicked = metadata.get('fake_submit_clicked', False)
        if fake_submit_clicked:
            detailed_results['fake_submit'] = {
                'triggered': True,
                'score': 1.0,
                'details': 'Invisible fake submit button was clicked'
            }
            total_score += self.honeypot_weights['fake_submit']
            indicators.append('fake_submit_clicked')
            print("🎯 HONEYPOT TRIGGERED: Fake submit button clicked")
        
        # 3. JS-based Optional Field Detection (Weight: 0.3)
        js_field_value = metadata.get('js_optional_field', '')
        js_enabled = metadata.get('js_enabled', True)
        
        # If JS is disabled and field is filled, it's likely a bot
        if not js_enabled and js_field_value and js_field_value.strip():
            detailed_results['optional_field'] = {
                'triggered': True,
                'score': 1.0,
                'details': f'JS field filled without JS: {js_field_value[:50]}...'
            }
            total_score += self.honeypot_weights['optional_field']
            indicators.append('js_field_no_js')
            print("🎯 HONEYPOT TRIGGERED: JS field filled without JavaScript")
        
        # Additional behavioral indicators that support honeypot findings
        if len(events) == 0:
            indicators.append('no_user_interaction')
            total_score += 0.1  # Bonus for no interaction with honeypots triggered
        
        return {
            'total_score': min(total_score, 1.0),
            'indicators': indicators,
            'detailed_results': detailed_results,
            'honeypots_triggered': len([r for r in detailed_results.values() if r['triggered']]),
            'analysis_summary': {
                'hidden_field_triggered': detailed_results['hidden_field']['triggered'],
                'fake_submit_triggered': detailed_results['fake_submit']['triggered'],
                'optional_field_triggered': detailed_results['optional_field']['triggered'],
                'total_honeypot_score': total_score,
                'threat_assessment': 'HIGH' if total_score >= 0.6 else 'MEDIUM' if total_score >= 0.3 else 'LOW'
            }
        }
    
    def _analyze_timing(self, events):
        """Analyze timing patterns for bot indicators"""
        if len(events) < 3:
            return 0.2, ['insufficient_timing_data']
        
        indicators = []
        score = 0.0
        
        # Calculate time differences
        time_diffs = []
        for i in range(1, len(events)):
            diff = events[i].get('timestamp', 0) - events[i-1].get('timestamp', 0)
            time_diffs.append(diff)
        
        if time_diffs:
            avg_time = sum(time_diffs) / len(time_diffs)
            
            # Very fast interactions (< 50ms average)
            if avg_time < 50:
                score += 0.3
                indicators.append('rapid_interactions')
            
            # Very regular timing (low variance)
            if len(set(time_diffs)) < len(time_diffs) * 0.3:
                score += 0.2
                indicators.append('regular_timing')
        
        return score, indicators
    
    def _analyze_movement(self, events):
        """Analyze movement patterns for bot indicators"""
        movement_events = [e for e in events if e.get('event_name') == 'mousemove']
        
        if len(movement_events) < 5:
            return 0.3, ['minimal_movement']
        
        indicators = []
        score = 0.0
        
        # Check for perfect straight lines
        positions = [(e.get('x_position', 0), e.get('y_position', 0)) for e in movement_events]
        
        # Simple linearity check
        if len(positions) > 3:
            # Check if all points are roughly on a straight line
            x_coords = [p[0] for p in positions]
            y_coords = [p[1] for p in positions]
            
            if len(set(x_coords)) <= 2 or len(set(y_coords)) <= 2:
                score += 0.4
                indicators.append('linear_movement')
        
        return score, indicators
    
    def _analyze_metadata(self, metadata):
        """Analyze metadata for suspicious patterns"""
        indicators = []
        score = 0.0
        
        # Check user agent
        user_agent = metadata.get('user_agent', '').lower()
        if any(bot_indicator in user_agent for bot_indicator in ['bot', 'crawler', 'spider', 'automated']):
            score += 0.5
            indicators.append('bot_user_agent')
        
        return score, indicators
    
    def _create_enhanced_analysis_result(self, total_score, threat_level, threat_indicators, is_bot, honeypot_results):
        """Create enhanced standardized analysis result with honeypot details"""
        return {
            'analysis': {
                'total_score': total_score,
                'honeypot_score': honeypot_results['total_score'],
                'threat_level': threat_level,
                'threat_indicators': threat_indicators,
                'total_indicators': len(threat_indicators),
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            },
            'honeypot_verdict': {
                'is_bot': is_bot,
                'confidence': min(0.9, 0.5 + (total_score * 0.4)),
                'recommendation': 'block' if threat_level in ['critical', 'high'] else ('monitor' if threat_level == 'medium' else 'allow'),
                'bot_probability': total_score
            },
            'honeypot_results': honeypot_results,
            'honeypot_summary': {
                'total_honeypots': 3,
                'triggered_honeypots': honeypot_results['honeypots_triggered'],
                'honeypot_score': honeypot_results['total_score'],
                'detection_method': 'multi_layer_honeypot',
                'honeypot_types_triggered': [
                    trap_type for trap_type, details in honeypot_results['detailed_results'].items() 
                    if details['triggered']
                ]
            },
            'module_info': {
                'module': 'enhanced_honeypot',
                'version': self.version,
                'analysis_method': 'behavioral_honeypot_hybrid',
                'honeypot_types': ['hidden_css_field', 'fake_submit_button', 'js_optional_field'],
                'features_analyzed': ['timing_patterns', 'movement_patterns', 'metadata_analysis', 'honeypot_triggers'],
                'weights': self.honeypot_weights
            }
        }
    
    def _create_error_result(self, error_message):
        """Create error result for failed analysis"""
        return {
            'analysis': {
                'total_score': 0.5,
                'honeypot_score': 0.0,
                'threat_level': 'medium',
                'threat_indicators': ['analysis_error'],
                'error': error_message,
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            },
            'honeypot_verdict': {
                'is_bot': True,
                'confidence': 0.3,
                'recommendation': 'monitor',
                'bot_probability': 0.5
            },
            'honeypot_results': {
                'total_score': 0.0,
                'indicators': ['analysis_error'],
                'detailed_results': {},
                'honeypots_triggered': 0
            },
            'module_info': {
                'module': 'enhanced_honeypot',
                'version': self.version,
                'status': 'error'
            }
        }
    
    def get_info(self):
        """Get enhanced module information"""
        return {
            'module': 'enhanced_honeypot',
            'version': self.version,
            'honeypot_types': ['hidden_css_field', 'fake_submit_button', 'js_optional_field'],
            'threat_levels': ['low', 'medium', 'high', 'critical'],
            'analysis_features': ['timing_patterns', 'movement_patterns', 'metadata_analysis'],
            'honeypot_weights': self.honeypot_weights,
            'suspicious_threshold': self.suspicious_threshold,
            'description': '3-layer honeypot system for advanced bot detection'
        }
    
    def get_honeypot_fields(self):
        """Get honeypot field configurations for frontend integration"""
        return {
            'hidden_field': {
                'name': 'website_url',  # Misleading name
                'type': 'text',
                'css_class': 'honeypot-hidden',
                'style': 'position: absolute; left: -9999px; visibility: hidden;',
                'label': 'Website URL (leave blank)',
                'required': False
            },
            'fake_submit': {
                'name': 'fake_submit_btn',
                'type': 'submit',
                'css_class': 'honeypot-fake-submit',
                'style': 'position: absolute; left: -9999px; visibility: hidden;',
                'value': 'Submit Form'
            },
            'js_optional': {
                'name': 'optional_info',
                'type': 'text',
                'css_class': 'honeypot-js-field',
                'label': 'Additional Info (Optional)',
                'placeholder': 'This field should remain empty',
                'data_js_only': 'true'
            }
        }
