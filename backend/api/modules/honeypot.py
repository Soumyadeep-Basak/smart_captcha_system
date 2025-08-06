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
            'hidden_field': 0.25,     # CSS hidden field detection
            'fake_submit': 0.25,      # Invisible submit button
            'optional_field': 0.2,    # JS-based detection
            'focus_order': 0.15,      # Focus order violation
            'offscreen_mouse': 0.15   # Offscreen mouse decoy
        }
        
        # STRICT RULE: Any single honeypot trigger = bot detected
        self.strict_mode = True
        self.any_trigger_threshold = 0.1  # If any honeypot triggers, immediate bot detection
        
        # Thresholds
        self.suspicious_threshold = 0.3  # Lower threshold for honeypot-based detection
        self.high_threat_threshold = 0.6
        
        print(f"🍯 Enhanced Honeypot Module v{self.version} initialized")
        print(f"🎯 Honeypot mechanisms: {list(self.honeypot_weights.keys())}")
        print(f"🚨 Strict mode: {'ENABLED' if self.strict_mode else 'DISABLED'} - Any trigger = Bot")
    
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
            'optional_field': {'triggered': False, 'score': 0.0, 'details': ''},
            'focus_order': {'triggered': False, 'score': 0.0, 'details': ''},
            'offscreen_mouse': {'triggered': False, 'score': 0.0, 'details': ''}
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
        
        # 3. JS-based Optional Field Detection (Weight: 0.2)
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
        
        # 4. Focus Order Honeypot Detection (Weight: 0.15) - HUMAN-FRIENDLY
        focus_trail = metadata.get('focus_trail', [])
        expected_order = metadata.get('expected_focus_order', [])
        
        if len(focus_trail) >= 6 and len(expected_order) > 0:  # Increased from 3 to 6 - need more data
            # Check for EXTREME unnatural patterns that only bots would exhibit
            extreme_violations = 0
            rapid_back_and_forth = 0
            
            # Look for patterns that humans would never do
            for i in range(2, len(focus_trail)):  # Need at least 3 events
                current_field = focus_trail[i]
                previous_field = focus_trail[i-1]
                before_previous = focus_trail[i-2]
                
                if all(f in expected_order for f in [current_field, previous_field, before_previous]):
                    # Pattern: A -> B -> A (rapid back-and-forth) - very suspicious
                    if current_field == before_previous and current_field != previous_field:
                        rapid_back_and_forth += 1
                    
                    # Only flag MASSIVE jumps (like first field to last field repeatedly)
                    current_index = expected_order.index(current_field)
                    previous_index = expected_order.index(previous_field)
                    jump_size = abs(current_index - previous_index)
                    
                    if jump_size >= 4:  # Only extreme jumps
                        extreme_violations += 1
            
            # Only trigger for patterns that are clearly non-human
            if rapid_back_and_forth >= 3 or extreme_violations >= 4:
                detailed_results['focus_order'] = {
                    'triggered': True,
                    'score': 1.0,
                    'details': f'Extreme bot-like focus: {" -> ".join(focus_trail[-6:])} (rapid: {rapid_back_and_forth}, extreme: {extreme_violations})'
                }
                total_score += self.honeypot_weights['focus_order']
                indicators.append('extreme_bot_focus_pattern')
                print(f"🎯 HONEYPOT TRIGGERED: Extreme bot-like focus patterns (rapid: {rapid_back_and_forth}, extreme: {extreme_violations})")
            else:
                print(f"🟢 Focus order acceptable for human: {len(focus_trail)} events, normal behavior")
        
        # 5. Offscreen Mouse Decoy Detection (Weight: 0.15)
        offscreen_triggered = metadata.get('offscreen_mouse_triggered', False)
        if offscreen_triggered:
            detailed_results['offscreen_mouse'] = {
                'triggered': True,
                'score': 1.0,
                'details': 'Mouse entered offscreen decoy element'
            }
            total_score += self.honeypot_weights['offscreen_mouse']
            indicators.append('offscreen_mouse_decoy')
            print("🎯 HONEYPOT TRIGGERED: Offscreen mouse decoy touched")
        
        # STRICT MODE: Only for PRIMARY honeypots that humans should NEVER trigger
        primary_honeypots_triggered = [
            r for trap_type, r in detailed_results.items() 
            if r['triggered'] and trap_type in ['hidden_field', 'fake_submit', 'optional_field']
        ]
        secondary_honeypots_triggered = [
            r for trap_type, r in detailed_results.items() 
            if r['triggered'] and trap_type in ['focus_order', 'offscreen_mouse']
        ]
        
        total_honeypots_triggered = len(primary_honeypots_triggered) + len(secondary_honeypots_triggered)
        
        # STRICT MODE: Only apply to primary honeypots (hidden field, fake submit, JS field)
        if self.strict_mode and len(primary_honeypots_triggered) > 0:
            total_score = 1.0  # Maximum score for any primary trigger
            indicators.append('strict_primary_honeypot_enforcement')
            print(f"🚨 STRICT MODE: {len(primary_honeypots_triggered)} PRIMARY honeypot(s) triggered - IMMEDIATE BOT DETECTION")
        elif len(secondary_honeypots_triggered) > 0:
            # Secondary honeypots add suspicion but don't guarantee bot detection
            secondary_bonus = len(secondary_honeypots_triggered) * 0.3
            total_score += secondary_bonus
            print(f"⚠️ Secondary honeypots triggered: {len(secondary_honeypots_triggered)} (bonus: +{secondary_bonus:.2f})")
        else:
            print(f"🟢 No honeypots triggered - normal human behavior")
        
        # Additional behavioral indicators that support honeypot findings
        if len(events) == 0:
            indicators.append('no_user_interaction')
            total_score += 0.1  # Bonus for no interaction with honeypots triggered
        
        return {
            'total_score': min(total_score, 1.0),
            'indicators': indicators,
            'detailed_results': detailed_results,
            'honeypots_triggered': total_honeypots_triggered,
            'primary_honeypots_triggered': len(primary_honeypots_triggered),
            'secondary_honeypots_triggered': len(secondary_honeypots_triggered),
            'analysis_summary': {
                'hidden_field_triggered': detailed_results['hidden_field']['triggered'],
                'fake_submit_triggered': detailed_results['fake_submit']['triggered'],
                'optional_field_triggered': detailed_results['optional_field']['triggered'],
                'focus_order_triggered': detailed_results['focus_order']['triggered'],
                'offscreen_mouse_triggered': detailed_results['offscreen_mouse']['triggered'],
                'total_honeypot_score': total_score,
                'threat_assessment': 'HIGH' if total_score >= 0.6 else 'MEDIUM' if total_score >= 0.3 else 'LOW',
                'strict_mode_applied': len(primary_honeypots_triggered) > 0
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
                'total_honeypots': 5,
                'triggered_honeypots': honeypot_results['honeypots_triggered'],
                'honeypot_score': honeypot_results['total_score'],
                'detection_method': 'multi_layer_honeypot_strict',
                'honeypot_types_triggered': [
                    trap_type for trap_type, details in honeypot_results['detailed_results'].items() 
                    if details['triggered']
                ],
                'strict_mode_enabled': self.strict_mode
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
            'honeypot_types': ['hidden_css_field', 'fake_submit_button', 'js_optional_field', 'focus_order_tracking', 'offscreen_mouse_decoy'],
            'threat_levels': ['low', 'medium', 'high', 'critical'],
            'analysis_features': ['timing_patterns', 'movement_patterns', 'metadata_analysis'],
            'honeypot_weights': self.honeypot_weights,
            'suspicious_threshold': self.suspicious_threshold,
            'strict_mode': self.strict_mode,
            'total_honeypots': 5,
            'description': '5-layer honeypot system with strict enforcement - any trigger = bot detection'
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
