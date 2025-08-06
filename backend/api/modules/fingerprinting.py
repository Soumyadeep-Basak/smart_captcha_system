# Fingerprinting Module - Enhanced Browser Analysis with Rule-Based Detection
from datetime import datetime
import hashlib
import json

class FingerprintingModule:
    def __init__(self):
        print("👆 Initializing Enhanced Fingerprinting Module")
        # Rule-based thresholds for bot detection (Lowered for less aggressive detection)
        self.thresholds = {
            'plugins_min': 0,       # Minimum plugins for human (lowered)
            'mime_types_min': 0,    # Minimum mime types for human (lowered)
            'screen_min_width': 400,   # Minimum screen width (lowered)
            'screen_min_height': 300,  # Minimum screen height (lowered)
            'ua_min_length': 20,    # Minimum user agent length (lowered)
            'hardware_concurrency_min': 0,  # Minimum CPU cores (lowered)
            'canvas_min_length': 20,    # Minimum canvas fingerprint length (lowered)
            'webgl_min_length': 10,     # Minimum WebGL fingerprint length (lowered)
        }
        
        # Suspicious patterns for detection
        self.suspicious_patterns = [
            'headless', 'phantom', 'selenium', 'webdriver', 'puppeteer',
            'chrome-headless', 'chromeless', 'bot', 'crawler', 'spider',
            'automation', 'script', 'test'
        ]
        
        # Known bad canvas/WebGL fingerprints (signatures commonly used by bots)
        self.known_bad_canvas_hashes = {
            # Common headless Chrome canvas signatures
            '6a3f5e2c4b8d7a1f',  # Common headless signature
            'e4b8c6d2a5f7e9c1',  # Another headless pattern
            'ffffffffffffffff',  # All-white canvas (common in bots)
            '0000000000000000',  # All-black canvas (common in bots)
            'abcdef1234567890',  # Generic test signature
            '1234567890abcdef',  # Another test pattern
            # Add more as discovered
        }
        
        self.known_bad_webgl_signatures = {
            'mesa',  # Common in headless environments
            'vmware',  # Virtual machine signatures
            'virtual',  # Virtual GPU signatures
            'software',  # Software rendering
            'null',  # Null renderer
        }
        
        # Track canvas signatures for duplicate detection
        self.canvas_signature_tracker = {}  # {canvas_hash: [ip_addresses]}
        self.webgl_signature_tracker = {}   # {webgl_signature: [ip_addresses]}
        
        # Timing analysis thresholds
        self.timing_thresholds = {
            'canvas_render_time_max': 1000,  # Max ms for canvas rendering
            'webgl_render_time_max': 2000,   # Max ms for WebGL rendering
            'plugin_enum_time_max': 500,     # Max ms for plugin enumeration
        }
    
    def analyze_fingerprint(self, metadata=None, browser_fingerprint=None):
        """Enhanced fingerprint analysis with rule-based bot detection"""
        try:
            print("👆 Enhanced Fingerprinting: Analyzing browser features")
            
            if not metadata:
                metadata = {}
            if not browser_fingerprint:
                browser_fingerprint = {}
            
            # Combine traditional and enhanced analysis
            fingerprint_data = {}
            risk_indicators = []
            risk_score = 0.0
            
            # 🔥 VERY HIGH PRIORITY CHECKS
            
            # 1. WebDriver Detection (Most reliable bot indicator)
            webdriver_detected = browser_fingerprint.get('webdriver_detected', False)
            if webdriver_detected:
                risk_score += 0.9
                risk_indicators.append('webdriver_detected')
                print("🚨 CRITICAL: WebDriver detected!")
            
            # 2. Zero Feature Detection (Strong headless indicator)
            plugins_count = browser_fingerprint.get('plugins_count', 0)
            mime_types_count = browser_fingerprint.get('mime_types_count', 0)
            fonts_count = browser_fingerprint.get('fonts_count', 0)
            
            # If ALL major features are zero = strong bot indicator
            zero_features = []
            if plugins_count == 0:
                zero_features.append('plugins')
            if mime_types_count == 0:
                zero_features.append('mime_types')
            if fonts_count == 0:
                zero_features.append('fonts')
            
            # Critical: If 2+ major features are zero, likely headless
            if len(zero_features) >= 2:
                risk_score += 0.85
                risk_indicators.append(f'headless_pattern_{len(zero_features)}_zero_features')
                print(f"🚨 CRITICAL: Headless pattern detected - {len(zero_features)} features are zero: {zero_features}")
            elif len(zero_features) == 1:
                risk_score += 0.4
                risk_indicators.append(f'single_zero_feature_{zero_features[0]}')
                print(f"🚨 WARNING: Zero {zero_features[0]} detected")
            
            # 3. Enhanced Automation Detection
            automation_indicators = self._detect_automation_patterns(browser_fingerprint)
            risk_score += automation_indicators['risk_score']
            risk_indicators.extend(automation_indicators['indicators'])
            fingerprint_data['automation_analysis'] = automation_indicators
            
            # ✅ HIGH PRIORITY CHECKS
            
            # 4. User Agent Analysis (Enhanced)
            user_agent = browser_fingerprint.get('user_agent', metadata.get('user_agent', ''))
            ua_analysis = self._analyze_enhanced_user_agent(user_agent, browser_fingerprint)
            fingerprint_data['user_agent_analysis'] = ua_analysis
            risk_score += ua_analysis['risk_score']
            risk_indicators.extend(ua_analysis['indicators'])
            
            # ⚠️ MEDIUM PRIORITY CHECKS
            
            # 5. Screen Properties Analysis
            screen_analysis = self._analyze_screen_properties(browser_fingerprint)
            fingerprint_data['screen_analysis'] = screen_analysis
            risk_score += screen_analysis['risk_score']
            risk_indicators.extend(screen_analysis['indicators'])
            
            # 6. Touch Support Analysis
            touch_analysis = self._analyze_touch_support(browser_fingerprint)
            fingerprint_data['touch_analysis'] = touch_analysis
            risk_score += touch_analysis['risk_score']
            risk_indicators.extend(touch_analysis['indicators'])
            
            # 7. Browser Capabilities Analysis
            capabilities_analysis = self._analyze_browser_capabilities(browser_fingerprint)
            fingerprint_data['capabilities_analysis'] = capabilities_analysis
            risk_score += capabilities_analysis['risk_score']
            risk_indicators.extend(capabilities_analysis['indicators'])
            
            # 8. Hardware Analysis
            hardware_analysis = self._analyze_hardware_info(browser_fingerprint)
            fingerprint_data['hardware_analysis'] = hardware_analysis
            risk_score += hardware_analysis['risk_score']
            risk_indicators.extend(hardware_analysis['indicators'])
            
            # 9. Font Enumeration Analysis
            font_analysis = self._analyze_font_enumeration(browser_fingerprint)
            fingerprint_data['font_analysis'] = font_analysis
            risk_score += font_analysis['risk_score']
            risk_indicators.extend(font_analysis['indicators'])
            
            # 10. Behavioral Consistency Analysis
            consistency_analysis = self._analyze_behavioral_consistency(browser_fingerprint)
            fingerprint_data['consistency_analysis'] = consistency_analysis
            risk_score += consistency_analysis['risk_score']
            risk_indicators.extend(consistency_analysis['indicators'])
            
            # 11. Advanced Pattern Detection
            pattern_analysis = self._analyze_advanced_patterns(browser_fingerprint, metadata)
            fingerprint_data['pattern_analysis'] = pattern_analysis
            risk_score += pattern_analysis['risk_score']
            risk_indicators.extend(pattern_analysis['indicators'])
            
            # Traditional IP analysis
            ip_address = metadata.get('ip_address', '')
            ip_analysis = self._analyze_ip(ip_address)
            fingerprint_data['ip_analysis'] = ip_analysis
            risk_score += ip_analysis['risk_score']
            risk_indicators.extend(ip_analysis['indicators'])
            
            # Generate enhanced device fingerprint hash
            fingerprint_hash = self._generate_enhanced_fingerprint_hash(metadata, browser_fingerprint)
            fingerprint_data['device_hash'] = fingerprint_hash
            
            # Store raw fingerprint data for analysis
            fingerprint_data['raw_fingerprint'] = browser_fingerprint
            fingerprint_data['feature_counts'] = {
                'plugins': plugins_count,
                'mime_types': mime_types_count,
                'screen_width': browser_fingerprint.get('screen_width', 0),
                'screen_height': browser_fingerprint.get('screen_height', 0),
                'touch_points': browser_fingerprint.get('max_touch_points', 0),
                'hardware_concurrency': browser_fingerprint.get('hardware_concurrency', 0)
            }
            
            # Apply risk score limits and determine final risk level
            final_risk_score = min(risk_score, 1.0)
            
            if final_risk_score >= 0.8:
                risk_level = 'high'
            elif final_risk_score >= 0.5:
                risk_level = 'medium'
            elif final_risk_score >= 0.3:
                risk_level = 'low'
            else:
                risk_level = 'minimal'
            
            # Bot decision based on risk score
            is_bot_likely = final_risk_score >= 0.6
            
            result = self._create_enhanced_fingerprint_result(
                fingerprint_data, risk_level, risk_indicators, final_risk_score, is_bot_likely
            )
            
            print(f"👆 Enhanced Fingerprint Analysis Complete:")
            print(f"   Risk Level: {risk_level.upper()}")
            print(f"   Risk Score: {final_risk_score:.3f}")
            print(f"   Bot Likely: {is_bot_likely}")
            print(f"   Risk Indicators: {len(risk_indicators)}")
            print(f"   Key Features: Plugins={plugins_count}, MIME={mime_types_count}, WebDriver={webdriver_detected}")
            
            return result
            
        except Exception as e:
            print(f"❌ Enhanced fingerprinting analysis error: {e}")
            return self._create_enhanced_fingerprint_result({}, 'medium', ['analysis_error'], 0.5, True)
    
    def _analyze_enhanced_user_agent(self, user_agent, browser_fingerprint):
        """Enhanced user agent analysis with additional browser fingerprint data"""
        indicators = []
        risk_score = 0.0
        
        if not user_agent:
            return {
                'risk_score': 0.7,
                'indicators': ['missing_user_agent'],
                'browser': 'unknown',
                'os': 'unknown',
                'is_mobile': False,
                'suspicious_patterns': []
            }
        
        ua_lower = user_agent.lower()
        
        # Check for suspicious patterns from browser fingerprint
        suspicious_patterns = browser_fingerprint.get('suspicious_ua_patterns', [])
        if suspicious_patterns:
            risk_score += 0.8
            indicators.append(f'suspicious_patterns_{len(suspicious_patterns)}')
            print(f"🚨 Suspicious UA patterns detected: {suspicious_patterns}")
        
        # Original bot detection logic
        for pattern in self.suspicious_patterns:
            if pattern in ua_lower:
                risk_score += 0.8
                indicators.append(f'bot_keyword_{pattern}')
                break
        
        # Check user agent length
        ua_length = browser_fingerprint.get('user_agent_length', len(user_agent))
        if ua_length < self.thresholds['ua_min_length']:
            risk_score += 0.6
            indicators.append('short_user_agent')
            print(f"🚨 Short user agent detected: {ua_length} chars")
        
        # Basic structure checks
        if 'mozilla' not in ua_lower:
            risk_score += 0.3
            indicators.append('no_mozilla')
        
        # Extract browser and OS info
        browser = 'unknown'
        os = 'unknown'
        is_mobile = False
        
        if 'chrome' in ua_lower:
            browser = 'chrome'
        elif 'firefox' in ua_lower:
            browser = 'firefox'
        elif 'safari' in ua_lower and 'chrome' not in ua_lower:
            browser = 'safari'
        elif 'edge' in ua_lower:
            browser = 'edge'
        
        if 'windows' in ua_lower:
            os = 'windows'
        elif 'mac' in ua_lower:
            os = 'macos'
        elif 'linux' in ua_lower:
            os = 'linux'
        elif 'android' in ua_lower:
            os = 'android'
            is_mobile = True
        elif 'ios' in ua_lower:
            os = 'ios'
            is_mobile = True
        
        return {
            'risk_score': min(risk_score, 1.0),
            'indicators': indicators,
            'browser': browser,
            'os': os,
            'is_mobile': is_mobile,
            'raw_user_agent': user_agent,
            'suspicious_patterns': suspicious_patterns,
            'user_agent_length': ua_length
        }
    
    def _analyze_screen_properties(self, browser_fingerprint):
        """Analyze screen properties for bot indicators"""
        indicators = []
        risk_score = 0.0
        
        screen_width = browser_fingerprint.get('screen_width', 0)
        screen_height = browser_fingerprint.get('screen_height', 0)
        color_depth = browser_fingerprint.get('screen_color_depth', 0)
        suspicious_screen = browser_fingerprint.get('suspicious_screen', False)
        
        # Check for suspicious screen configurations
        if suspicious_screen or screen_width == 0 or screen_height == 0:
            risk_score += 0.7
            indicators.append('invalid_screen_size')
            print(f"🚨 Suspicious screen size: {screen_width}x{screen_height}")
        
        # Check for unrealistic screen sizes
        if screen_width == screen_height and screen_width > 0:
            risk_score += 0.5
            indicators.append('square_screen')
        
        if (screen_width < self.thresholds['screen_min_width'] or 
            screen_height < self.thresholds['screen_min_height']) and screen_width > 0:
            risk_score += 0.4
            indicators.append('small_screen')
        
        # Check for missing color depth
        if color_depth == 0:
            risk_score += 0.3
            indicators.append('no_color_depth')
        
        return {
            'risk_score': min(risk_score, 1.0),
            'indicators': indicators,
            'screen_width': screen_width,
            'screen_height': screen_height,
            'color_depth': color_depth,
            'is_suspicious': suspicious_screen
        }
    
    def _analyze_touch_support(self, browser_fingerprint):
        """Analyze touch support for mobile emulation detection"""
        indicators = []
        risk_score = 0.0
        
        max_touch_points = browser_fingerprint.get('max_touch_points', 0)
        touch_support = browser_fingerprint.get('touch_support', False)
        
        # Check for inconsistent touch configurations
        if touch_support and max_touch_points == 0:
            risk_score += 0.3
            indicators.append('inconsistent_touch_config')
        
        # Very high touch points can indicate emulation
        if max_touch_points > 10:
            risk_score += 0.4
            indicators.append('excessive_touch_points')
        
        return {
            'risk_score': min(risk_score, 1.0),
            'indicators': indicators,
            'max_touch_points': max_touch_points,
            'touch_support': touch_support
        }
    
    def _analyze_browser_capabilities(self, browser_fingerprint):
        """Enhanced browser API capabilities analysis with signature detection"""
        indicators = []
        risk_score = 0.0
        
        # Critical capabilities that are often missing in bots
        webgl_supported = browser_fingerprint.get('webgl_supported', False)
        canvas_supported = browser_fingerprint.get('canvas_supported', False)
        audio_context_supported = browser_fingerprint.get('audio_context_supported', False)
        
        # Check for missing WebGL (common in headless browsers)
        if not webgl_supported:
            risk_score += 0.5
            indicators.append('no_webgl')
            print("🚨 WebGL not supported - possible headless browser")
        
        # Check for missing Canvas
        if not canvas_supported:
            risk_score += 0.4
            indicators.append('no_canvas')
        
        # Enhanced Canvas Fingerprint Analysis
        canvas_fingerprint = browser_fingerprint.get('canvas_fingerprint', '')
        canvas_analysis = self._analyze_canvas_signature(canvas_fingerprint, browser_fingerprint.get('ip_address', ''))
        risk_score += canvas_analysis['risk_score']
        indicators.extend(canvas_analysis['indicators'])
        
        # Enhanced WebGL Analysis
        webgl_vendor = browser_fingerprint.get('webgl_vendor', '').lower()
        webgl_renderer = browser_fingerprint.get('webgl_renderer', '').lower()
        webgl_analysis = self._analyze_webgl_signature(webgl_vendor, webgl_renderer, browser_fingerprint.get('ip_address', ''))
        risk_score += webgl_analysis['risk_score']
        indicators.extend(webgl_analysis['indicators'])
        
        # Check for missing Audio Context
        if not audio_context_supported:
            risk_score += 0.3
            indicators.append('no_audio_context')
        
        # Audio fingerprint analysis
        audio_sample_rate = browser_fingerprint.get('audio_sample_rate', 0)
        if audio_sample_rate == 0:
            risk_score += 0.3
            indicators.append('no_audio_sample_rate')
        elif audio_sample_rate in [44100, 48000]:  # Too common/predictable
            pass  # Normal rates
        else:
            # Unusual sample rates might indicate emulation
            risk_score += 0.1
            indicators.append('unusual_audio_sample_rate')
        
        # Check for missing storage APIs
        local_storage = browser_fingerprint.get('local_storage_supported', False)
        session_storage = browser_fingerprint.get('session_storage_supported', False)
        
        if not local_storage:
            risk_score += 0.2
            indicators.append('no_local_storage')
        
        if not session_storage:
            risk_score += 0.2
            indicators.append('no_session_storage')
        
        # Timing analysis for capability enumeration
        timing_analysis = self._analyze_capability_timing(browser_fingerprint)
        risk_score += timing_analysis['risk_score']
        indicators.extend(timing_analysis['indicators'])
        
        return {
            'risk_score': min(risk_score, 1.0),
            'indicators': indicators,
            'webgl_supported': webgl_supported,
            'canvas_supported': canvas_supported,
            'audio_context_supported': audio_context_supported,
            'canvas_analysis': canvas_analysis,
            'webgl_analysis': webgl_analysis,
            'timing_analysis': timing_analysis,
            'storage_support': {
                'local_storage': local_storage,
                'session_storage': session_storage
            }
        }
    
    def _analyze_hardware_info(self, browser_fingerprint):
        """Analyze hardware information for bot detection"""
        indicators = []
        risk_score = 0.0
        
        hardware_concurrency = browser_fingerprint.get('hardware_concurrency', 0)
        device_memory = browser_fingerprint.get('device_memory', 0)
        
        # Check for missing hardware info
        if hardware_concurrency == 0:
            risk_score += 0.4
            indicators.append('no_hardware_concurrency')
            print("🚨 No hardware concurrency info - possible bot")
        elif hardware_concurrency < self.thresholds['hardware_concurrency_min']:
            risk_score += 0.2
            indicators.append('low_hardware_concurrency')
        
        # Check for unusual hardware specs
        if hardware_concurrency > 32:  # Unusually high
            risk_score += 0.3
            indicators.append('excessive_cpu_cores')
        
        return {
            'risk_score': min(risk_score, 1.0),
            'indicators': indicators,
            'hardware_concurrency': hardware_concurrency,
            'device_memory': device_memory
        }
    
    def _analyze_canvas_signature(self, canvas_fingerprint, ip_address):
        """Analyze canvas fingerprint for bot patterns and duplicates"""
        indicators = []
        risk_score = 0.0
        
        if not canvas_fingerprint:
            risk_score += 0.4
            indicators.append('missing_canvas_fingerprint')
            return {
                'risk_score': risk_score,
                'indicators': indicators,
                'is_known_bad': False,
                'is_duplicate': False,
                'canvas_hash': ''
            }
        
        # Check canvas fingerprint length (too short indicates possible spoofing)
        if len(canvas_fingerprint) < self.thresholds['canvas_min_length']:
            risk_score += 0.5
            indicators.append('short_canvas_fingerprint')
            print(f"🚨 Suspicious canvas fingerprint length: {len(canvas_fingerprint)}")
        
        # Check against known bad canvas hashes
        canvas_hash = canvas_fingerprint[:16]  # Use first 16 chars as hash
        if canvas_hash in self.known_bad_canvas_hashes:
            risk_score += 0.8
            indicators.append('known_bad_canvas_hash')
            print(f"🚨 CRITICAL: Known bad canvas signature detected: {canvas_hash}")
        
        # Track canvas signatures for duplicate detection across IPs
        is_duplicate = False
        if canvas_hash in self.canvas_signature_tracker:
            existing_ips = self.canvas_signature_tracker[canvas_hash]
            if ip_address not in existing_ips:
                existing_ips.append(ip_address)
                if len(existing_ips) > 3:  # Same canvas across 3+ IPs is suspicious
                    risk_score += 0.7
                    indicators.append(f'canvas_duplicate_across_{len(existing_ips)}_ips')
                    print(f"🚨 Canvas signature reused across {len(existing_ips)} IPs")
                    is_duplicate = True
        else:
            self.canvas_signature_tracker[canvas_hash] = [ip_address]
        
        # Check for patterns indicating automation
        if canvas_fingerprint == canvas_fingerprint.upper():
            risk_score += 0.3
            indicators.append('canvas_all_uppercase')
        
        if canvas_fingerprint == canvas_fingerprint.lower():
            risk_score += 0.3
            indicators.append('canvas_all_lowercase')
        
        # Check for repeating patterns (common in automated generation)
        if len(set(canvas_fingerprint)) < len(canvas_fingerprint) * 0.5:
            risk_score += 0.4
            indicators.append('canvas_low_entropy')
        
        return {
            'risk_score': min(risk_score, 1.0),
            'indicators': indicators,
            'is_known_bad': canvas_hash in self.known_bad_canvas_hashes,
            'is_duplicate': is_duplicate,
            'canvas_hash': canvas_hash,
            'canvas_length': len(canvas_fingerprint)
        }
    
    def _analyze_webgl_signature(self, webgl_vendor, webgl_renderer, ip_address):
        """Analyze WebGL vendor/renderer signatures for bot detection"""
        indicators = []
        risk_score = 0.0
        
        # Check for known bad WebGL signatures
        for bad_signature in self.known_bad_webgl_signatures:
            if bad_signature in webgl_vendor or bad_signature in webgl_renderer:
                risk_score += 0.7
                indicators.append(f'webgl_bad_signature_{bad_signature}')
                print(f"🚨 Suspicious WebGL signature: {webgl_vendor}/{webgl_renderer}")
                break
        
        # Check for missing WebGL info
        if not webgl_vendor and not webgl_renderer:
            risk_score += 0.6
            indicators.append('missing_webgl_info')
        elif len(webgl_vendor) < 3 or len(webgl_renderer) < 3:
            risk_score += 0.4
            indicators.append('short_webgl_info')
        
        # Track WebGL signatures for duplicate detection
        webgl_signature = f"{webgl_vendor}|{webgl_renderer}"
        if webgl_signature in self.webgl_signature_tracker:
            existing_ips = self.webgl_signature_tracker[webgl_signature]
            if ip_address not in existing_ips:
                existing_ips.append(ip_address)
                if len(existing_ips) > 5:  # Same WebGL across 5+ IPs is suspicious
                    risk_score += 0.5
                    indicators.append(f'webgl_duplicate_across_{len(existing_ips)}_ips')
        else:
            self.webgl_signature_tracker[webgl_signature] = [ip_address]
        
        # Check for generic/default signatures
        generic_patterns = ['generic', 'default', 'unknown', 'null']
        for pattern in generic_patterns:
            if pattern in webgl_vendor.lower() or pattern in webgl_renderer.lower():
                risk_score += 0.3
                indicators.append(f'webgl_generic_{pattern}')
                break
        
        return {
            'risk_score': min(risk_score, 1.0),
            'indicators': indicators,
            'webgl_vendor': webgl_vendor,
            'webgl_renderer': webgl_renderer,
            'webgl_signature': webgl_signature
        }
    
    def _analyze_capability_timing(self, browser_fingerprint):
        """Analyze timing of capability enumeration for bot detection"""
        indicators = []
        risk_score = 0.0
        
        # Check canvas rendering time
        canvas_render_time = browser_fingerprint.get('canvas_render_time', 0)
        if canvas_render_time > self.timing_thresholds['canvas_render_time_max']:
            risk_score += 0.3
            indicators.append('slow_canvas_rendering')
        elif canvas_render_time > 0 and canvas_render_time < 10:
            # Too fast might indicate pre-computed values
            risk_score += 0.2
            indicators.append('suspiciously_fast_canvas')
        
        # Check WebGL rendering time
        webgl_render_time = browser_fingerprint.get('webgl_render_time', 0)
        if webgl_render_time > self.timing_thresholds['webgl_render_time_max']:
            risk_score += 0.3
            indicators.append('slow_webgl_rendering')
        elif webgl_render_time > 0 and webgl_render_time < 5:
            risk_score += 0.2
            indicators.append('suspiciously_fast_webgl')
        
        # Check plugin enumeration time
        plugin_enum_time = browser_fingerprint.get('plugin_enum_time', 0)
        if plugin_enum_time > self.timing_thresholds['plugin_enum_time_max']:
            risk_score += 0.2
            indicators.append('slow_plugin_enumeration')
        elif plugin_enum_time > 0 and plugin_enum_time < 1:
            risk_score += 0.1
            indicators.append('fast_plugin_enumeration')
        
        # Check for perfect timing (indicates possible caching/pre-computation)
        timings = [canvas_render_time, webgl_render_time, plugin_enum_time]
        if len(set(timings)) == 1 and timings[0] > 0:
            risk_score += 0.4
            indicators.append('identical_timing_values')
            print("🚨 Identical timing values detected - possible bot")
        
        return {
            'risk_score': min(risk_score, 1.0),
            'indicators': indicators,
            'canvas_render_time': canvas_render_time,
            'webgl_render_time': webgl_render_time,
            'plugin_enum_time': plugin_enum_time
        }
    
    def _analyze_font_enumeration(self, browser_fingerprint):
        """Analyze font enumeration patterns for bot detection"""
        indicators = []
        risk_score = 0.0
        
        fonts_count = browser_fingerprint.get('fonts_count', 0)
        fonts_list = browser_fingerprint.get('fonts_list', [])
        font_enum_time = browser_fingerprint.get('font_enum_time', 0)
        
        # Check for missing fonts (common in headless environments)
        if fonts_count == 0:
            risk_score += 0.6
            indicators.append('no_fonts_detected')
            print("🚨 No fonts detected - likely headless browser")
        elif fonts_count < 10:
            risk_score += 0.4
            indicators.append('very_few_fonts')
            print(f"🚨 Very few fonts detected: {fonts_count}")
        elif fonts_count < 30:
            risk_score += 0.2
            indicators.append('few_fonts')
        
        # Check for default/generic font lists (common in bots)
        if fonts_list:
            default_fonts = ['arial', 'times', 'courier', 'helvetica']
            detected_defaults = sum(1 for font in fonts_list if any(df in font.lower() for df in default_fonts))
            
            if len(fonts_list) > 0 and detected_defaults == len(fonts_list):
                risk_score += 0.5
                indicators.append('only_default_fonts')
                print("🚨 Only default fonts detected")
        
        # Check font enumeration timing
        if font_enum_time > 1000:  # More than 1 second is suspicious
            risk_score += 0.3
            indicators.append('slow_font_enumeration')
        elif font_enum_time > 0 and font_enum_time < 10:
            risk_score += 0.2
            indicators.append('suspiciously_fast_font_enum')
        
        return {
            'risk_score': min(risk_score, 1.0),
            'indicators': indicators,
            'fonts_count': fonts_count,
            'font_enum_time': font_enum_time
        }
    
    def _analyze_behavioral_consistency(self, browser_fingerprint):
        """Analyze consistency between different browser features"""
        indicators = []
        risk_score = 0.0
        
        # Check OS consistency between user agent and platform
        ua_os = browser_fingerprint.get('ua_os', '').lower()
        platform = browser_fingerprint.get('platform', '').lower()
        
        if ua_os and platform:
            os_consistent = False
            if 'windows' in ua_os and 'win' in platform:
                os_consistent = True
            elif 'mac' in ua_os and 'mac' in platform:
                os_consistent = True
            elif 'linux' in ua_os and 'linux' in platform:
                os_consistent = True
            
            if not os_consistent:
                risk_score += 0.5
                indicators.append('os_platform_mismatch')
                print(f"🚨 OS mismatch: UA={ua_os}, Platform={platform}")
        
        # Check mobile consistency
        is_mobile_ua = browser_fingerprint.get('is_mobile_ua', False)
        has_touch = browser_fingerprint.get('max_touch_points', 0) > 0
        screen_width = browser_fingerprint.get('screen_width', 0)
        
        if is_mobile_ua and not has_touch:
            risk_score += 0.4
            indicators.append('mobile_ua_no_touch')
        elif not is_mobile_ua and has_touch and screen_width > 1024:
            risk_score += 0.3
            indicators.append('desktop_ua_with_touch')
        
        # Check hardware consistency
        hardware_concurrency = browser_fingerprint.get('hardware_concurrency', 0)
        device_memory = browser_fingerprint.get('device_memory', 0)
        
        if hardware_concurrency > 16 and device_memory < 4:
            risk_score += 0.3
            indicators.append('high_cpu_low_memory')
        elif hardware_concurrency == 1 and device_memory > 8:
            risk_score += 0.3
            indicators.append('low_cpu_high_memory')
        
        # Check WebGL consistency with hardware
        webgl_vendor = browser_fingerprint.get('webgl_vendor', '').lower()
        if ('nvidia' in webgl_vendor or 'amd' in webgl_vendor) and hardware_concurrency < 2:
            risk_score += 0.2
            indicators.append('high_end_gpu_low_cpu')
        
        return {
            'risk_score': min(risk_score, 1.0),
            'indicators': indicators,
            'os_consistent': ua_os and platform,
            'mobile_consistent': True  # Simplified for now
        }
    
    def _analyze_advanced_patterns(self, browser_fingerprint, metadata):
        """Analyze advanced bot patterns and anomalies"""
        indicators = []
        risk_score = 0.0
        
        # Check for automation-specific timing patterns
        all_timings = [
            browser_fingerprint.get('canvas_render_time', 0),
            browser_fingerprint.get('webgl_render_time', 0),
            browser_fingerprint.get('plugin_enum_time', 0),
            browser_fingerprint.get('font_enum_time', 0)
        ]
        
        # Remove zero values for analysis
        valid_timings = [t for t in all_timings if t > 0]
        
        if len(valid_timings) >= 3:
            # Check for suspiciously similar timings
            timing_variance = max(valid_timings) - min(valid_timings)
            if timing_variance < 5:  # All timings within 5ms
                risk_score += 0.4
                indicators.append('uniform_timing_pattern')
                print("🚨 Suspiciously uniform timing pattern detected")
        
        # Check for feature enumeration order anomalies
        feature_order = browser_fingerprint.get('feature_enum_order', [])
        if feature_order:
            # Most humans enumerate in a somewhat random order
            # Bots often enumerate in alphabetical or fixed order
            if feature_order == sorted(feature_order):
                risk_score += 0.3
                indicators.append('alphabetical_feature_order')
        
        # Check for timestamp anomalies
        fingerprint_timestamp = browser_fingerprint.get('timestamp', 0)
        current_timestamp = int(datetime.now().timestamp() * 1000)
        
        if fingerprint_timestamp > 0:
            time_diff = abs(current_timestamp - fingerprint_timestamp)
            if time_diff > 300000:  # More than 5 minutes
                risk_score += 0.2
                indicators.append('old_fingerprint_timestamp')
            elif time_diff < 100:  # Less than 100ms (too precise)
                risk_score += 0.1
                indicators.append('precise_timestamp')
        
        # Check for batch submission patterns (multiple similar fingerprints)
        ip_address = metadata.get('ip_address', '')
        fingerprint_hash = browser_fingerprint.get('hash', '')
        
        if hasattr(self, 'recent_submissions'):
            if ip_address in self.recent_submissions:
                submission_count = len(self.recent_submissions[ip_address])
                if submission_count > 10:  # More than 10 submissions from same IP
                    risk_score += 0.5
                    indicators.append(f'high_submission_rate_{submission_count}')
        else:
            self.recent_submissions = {}
        
        # Initialize tracking if needed
        if ip_address not in self.recent_submissions:
            self.recent_submissions[ip_address] = []
        self.recent_submissions[ip_address].append(fingerprint_hash)
        
        # Keep only recent submissions (last 100 per IP)
        if len(self.recent_submissions[ip_address]) > 100:
            self.recent_submissions[ip_address] = self.recent_submissions[ip_address][-100:]
        
        return {
            'risk_score': min(risk_score, 1.0),
            'indicators': indicators,
            'timing_analysis': {
                'valid_timings_count': len(valid_timings),
                'timing_variance': timing_variance if len(valid_timings) >= 2 else 0
            }
        }
    
    def _detect_automation_patterns(self, browser_fingerprint):
        """Advanced automation pattern detection"""
        indicators = []
        risk_score = 0.0
        
        # Check for common automation signatures
        automation_signatures = [
            'navigator.webdriver',
            'window.cdc_',  # Chrome DevTools Protocol
            '_phantom',
            '_selenium',
            'callPhantom',
            'callSelenium',
            '__webdriver_script_fn',
            '__webdriver_evaluate',
            '__webdriver_unwrapped',
            '__fxdriver_unwrapped',
            '__driver_evaluate',
            '__webdriver_script_func',
            '__webdriver_script_function'
        ]
        
        detected_signatures = browser_fingerprint.get('automation_signatures', [])
        for sig in detected_signatures:
            if sig.lower() in [s.lower() for s in automation_signatures]:
                risk_score += 0.7
                indicators.append(f'automation_signature_{sig.lower()}')
                print(f"🚨 Automation signature detected: {sig}")
        
        # Check for missing window properties (common in headless)
        missing_properties = browser_fingerprint.get('missing_window_properties', [])
        critical_missing = ['outerHeight', 'outerWidth', 'screenY', 'screenX']
        missing_critical = [prop for prop in missing_properties if prop in critical_missing]
        
        if len(missing_critical) >= 2:
            risk_score += 0.6
            indicators.append(f'missing_critical_properties_{len(missing_critical)}')
            print(f"🚨 Missing critical window properties: {missing_critical}")
        
        # Check for phantom/headless specific patterns
        phantom_indicators = browser_fingerprint.get('phantom_indicators', [])
        if phantom_indicators:
            risk_score += 0.8
            indicators.append(f'phantom_detected_{len(phantom_indicators)}')
            print(f"🚨 Phantom/headless indicators: {phantom_indicators}")
        
        # Check for selenium-specific patterns
        selenium_indicators = browser_fingerprint.get('selenium_indicators', [])
        if selenium_indicators:
            risk_score += 0.8
            indicators.append(f'selenium_detected_{len(selenium_indicators)}')
            print(f"🚨 Selenium indicators: {selenium_indicators}")
        
        # Check for chrome headless patterns
        chrome_headless = browser_fingerprint.get('chrome_headless_detected', False)
        if chrome_headless:
            risk_score += 0.9
            indicators.append('chrome_headless_confirmed')
            print("🚨 Chrome headless mode confirmed")
        
        # Check for notification permission patterns (bots often have undefined)
        notification_permission = browser_fingerprint.get('notification_permission', '')
        if notification_permission == 'undefined' or not notification_permission:
            risk_score += 0.3
            indicators.append('undefined_notification_permission')
        
        # Check for missing iframe support
        iframe_support = browser_fingerprint.get('iframe_support', True)
        if not iframe_support:
            risk_score += 0.4
            indicators.append('no_iframe_support')
        
        # Check for suspicious navigator properties
        navigator_props = browser_fingerprint.get('navigator_properties', {})
        if navigator_props:
            # Check for missing or suspicious language
            languages = navigator_props.get('languages', [])
            if not languages or len(languages) == 0:
                risk_score += 0.4
                indicators.append('no_navigator_languages')
            
            # Check for missing connection info
            connection = navigator_props.get('connection', {})
            if not connection:
                risk_score += 0.2
                indicators.append('no_connection_info')
        
        return {
            'risk_score': min(risk_score, 1.0),
            'indicators': indicators,
            'detected_signatures': detected_signatures,
            'missing_properties': missing_properties,
            'automation_patterns': len(indicators)
        }
    def _analyze_user_agent(self, user_agent):
        """Legacy user agent analysis method for backward compatibility"""
        indicators = []
        risk_score = 0.0
        
        if not user_agent:
            return {
                'risk_score': 0.7,
                'indicators': ['missing_user_agent'],
                'browser': 'unknown',
                'os': 'unknown',
                'is_mobile': False
            }
        
        ua_lower = user_agent.lower()
        
        # Bot detection keywords
        bot_keywords = [
            'bot', 'crawler', 'spider', 'scraper', 'automated', 'headless',
            'phantom', 'selenium', 'webdriver', 'puppeteer'
        ]
        
        for keyword in bot_keywords:
            if keyword in ua_lower:
                risk_score += 0.8
                indicators.append(f'bot_keyword_{keyword}')
                break
        
        # Suspicious patterns
        if 'mozilla' not in ua_lower:
            risk_score += 0.3
            indicators.append('no_mozilla')
        
        if len(user_agent) < 50:
            risk_score += 0.2
            indicators.append('short_user_agent')
        
        # Extract browser and OS info
        browser = 'unknown'
        os = 'unknown'
        is_mobile = False
        
        if 'chrome' in ua_lower:
            browser = 'chrome'
        elif 'firefox' in ua_lower:
            browser = 'firefox'
        elif 'safari' in ua_lower and 'chrome' not in ua_lower:
            browser = 'safari'
        elif 'edge' in ua_lower:
            browser = 'edge'
        
        if 'windows' in ua_lower:
            os = 'windows'
        elif 'mac' in ua_lower:
            os = 'macos'
        elif 'linux' in ua_lower:
            os = 'linux'
        elif 'android' in ua_lower:
            os = 'android'
            is_mobile = True
        elif 'ios' in ua_lower:
            os = 'ios'
            is_mobile = True
        
        return {
            'risk_score': min(risk_score, 1.0),
            'indicators': indicators,
            'browser': browser,
            'os': os,
            'is_mobile': is_mobile,
            'raw_user_agent': user_agent
        }
        os = 'unknown'
        is_mobile = False
        
        if 'chrome' in ua_lower:
            browser = 'chrome'
        elif 'firefox' in ua_lower:
            browser = 'firefox'
        elif 'safari' in ua_lower and 'chrome' not in ua_lower:
            browser = 'safari'
        elif 'edge' in ua_lower:
            browser = 'edge'
        
        if 'windows' in ua_lower:
            os = 'windows'
        elif 'mac' in ua_lower:
            os = 'macos'
        elif 'linux' in ua_lower:
            os = 'linux'
        elif 'android' in ua_lower:
            os = 'android'
            is_mobile = True
        elif 'ios' in ua_lower:
            os = 'ios'
            is_mobile = True
        
        return {
            'risk_score': min(risk_score, 1.0),
            'indicators': indicators,
            'browser': browser,
            'os': os,
            'is_mobile': is_mobile,
            'raw_user_agent': user_agent
        }
    
    def _analyze_ip(self, ip_address):
        """Analyze IP address for bot indicators"""
        indicators = []
        risk_score = 0.0
        
        if not ip_address:
            return {
                'risk_score': 0.3,
                'indicators': ['missing_ip'],
                'type': 'unknown'
            }
        
        ip_type = 'public'
        
        # Local/loopback addresses
        if ip_address in ['127.0.0.1', '::1', 'localhost']:
            risk_score += 0.1  # Low risk for development
            indicators.append('localhost')
            ip_type = 'localhost'
        
        # Private IP ranges
        elif (ip_address.startswith('192.168.') or 
              ip_address.startswith('10.') or 
              ip_address.startswith('172.')):
            risk_score += 0.05
            indicators.append('private_ip')
            ip_type = 'private'
        
        # Known bot/cloud provider patterns (simplified)
        cloud_patterns = ['amazonaws', 'googlecloud', 'azure', 'digitalocean']
        # Note: This would need actual IP range checking in production
        
        return {
            'risk_score': min(risk_score, 1.0),
            'indicators': indicators,
            'type': ip_type,
            'raw_ip': ip_address
        }
    
    def _generate_enhanced_fingerprint_hash(self, metadata, browser_fingerprint):
        """Generate enhanced device fingerprint hash using multiple data sources"""
        try:
            # Combine traditional metadata with enhanced browser fingerprint
            fingerprint_elements = [
                metadata.get('user_agent', ''),
                metadata.get('ip_address', ''),
                str(browser_fingerprint.get('plugins_count', 0)),
                str(browser_fingerprint.get('mime_types_count', 0)),
                str(browser_fingerprint.get('screen_width', 0)),
                str(browser_fingerprint.get('screen_height', 0)),
                str(browser_fingerprint.get('screen_color_depth', 0)),
                str(browser_fingerprint.get('max_touch_points', 0)),
                str(browser_fingerprint.get('hardware_concurrency', 0)),
                browser_fingerprint.get('platform', ''),
                browser_fingerprint.get('language', ''),
                browser_fingerprint.get('timezone', ''),
                browser_fingerprint.get('webgl_vendor', ''),
                browser_fingerprint.get('webgl_renderer', ''),
                browser_fingerprint.get('canvas_fingerprint', ''),
                str(browser_fingerprint.get('audio_sample_rate', 0)),
                str(browser_fingerprint.get('device_memory', 0)),
                str(browser_fingerprint.get('webdriver_detected', False)),
            ]
            
            fingerprint_string = '|'.join(str(elem) for elem in fingerprint_elements)
            
            # Generate SHA256 hash
            hash_object = hashlib.sha256(fingerprint_string.encode())
            return hash_object.hexdigest()[:16]  # First 16 characters
            
        except Exception as e:
            print(f"❌ Enhanced fingerprint hash generation error: {e}")
            return 'unknown'
    
    def _generate_fingerprint_hash(self, metadata):
        """Legacy fingerprint hash generation for backward compatibility"""
        try:
            # Combine various metadata elements
            fingerprint_elements = [
                metadata.get('user_agent', ''),
                metadata.get('ip_address', ''),
                # In a real implementation, you'd include:
                # - Screen resolution
                # - Timezone
                # - Language settings
                # - Available fonts
                # - Hardware specs
                # - etc.
            ]
            
            fingerprint_string = '|'.join(str(elem) for elem in fingerprint_elements)
            
            # Generate SHA256 hash
            hash_object = hashlib.sha256(fingerprint_string.encode())
            return hash_object.hexdigest()[:16]  # First 16 characters
            
        except Exception as e:
            print(f"❌ Fingerprint hash generation error: {e}")
            return 'unknown'
    
    def _create_enhanced_fingerprint_result(self, fingerprint_data, risk_level, risk_indicators, risk_score, is_bot_likely):
        """Create enhanced standardized fingerprint result"""
        return {
            'fingerprint': fingerprint_data,
            'analysis': {
                'risk_level': risk_level,
                'risk_score': risk_score,
                'risk_indicators': risk_indicators,
                'is_bot_likely': is_bot_likely,
                'total_indicators': len(risk_indicators),
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            },
            'verdict': {
                'is_suspicious': risk_level in ['medium', 'high'],
                'recommendation': 'block' if risk_level == 'high' else ('monitor' if risk_level == 'medium' else 'allow'),
                'confidence': min(0.9, 0.3 + (risk_score * 0.6)),  # Scale confidence with risk
                'bot_probability': risk_score
            },
            'module_info': {
                'module': 'enhanced_fingerprinting',
                'analysis_method': 'rule_based_heuristics',
                'features_analyzed': [
                    'webdriver_detection', 'plugins_count', 'mime_types_count',
                    'user_agent_patterns', 'screen_properties', 'touch_support',
                    'browser_capabilities', 'hardware_info', 'ip_address',
                    'canvas_signature', 'webgl_signature', 'font_enumeration',
                    'behavioral_consistency', 'timing_patterns', 'advanced_patterns'
                ],
                'detection_rules': len(self.thresholds),
                'suspicious_patterns': len(self.suspicious_patterns),
                'known_bad_signatures': {
                    'canvas_hashes': len(self.known_bad_canvas_hashes),
                    'webgl_signatures': len(self.known_bad_webgl_signatures)
                }
            },
            'rule_based_analysis': {
                'thresholds_used': self.thresholds,
                'pattern_matching': True,
                'feature_scoring': True,
                'decision_tree': 'if_then_rules'
            }
        }
    
    def _create_fingerprint_result(self, fingerprint_data, risk_level, risk_indicators):
        """Create standardized fingerprint result"""
        return {
            'fingerprint': fingerprint_data,
            'analysis': {
                'risk_level': risk_level,
                'risk_indicators': risk_indicators,
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            },
            'verdict': {
                'is_suspicious': risk_level in ['medium', 'high'],
                'recommendation': 'monitor' if risk_level == 'medium' else ('block' if risk_level == 'high' else 'allow'),
                'confidence': 0.7 if risk_indicators else 0.5
            },
            'module_info': {
                'module': 'fingerprinting',
                'analysis_method': 'metadata_heuristics',
                'features_analyzed': ['user_agent', 'ip_address', 'device_hash']
            }
        }
    
    def get_info(self):
        """Get enhanced module information with signature tracking stats"""
        return {
            'module': 'enhanced_fingerprinting',
            'version': '2.0',
            'risk_levels': ['minimal', 'low', 'medium', 'high'],
            'analysis_features': [
                'user_agent', 'ip_address', 'device_fingerprint',
                'webdriver_detection', 'plugins_analysis', 'mime_types_analysis',
                'screen_properties', 'touch_support', 'browser_capabilities',
                'hardware_info', 'canvas_signature', 'webgl_signature',
                'font_enumeration', 'behavioral_consistency', 'timing_patterns'
            ],
            'hash_method': 'sha256',
            'signature_tracking': {
                'canvas_signatures_tracked': len(self.canvas_signature_tracker),
                'webgl_signatures_tracked': len(self.webgl_signature_tracker),
                'known_bad_canvas_hashes': len(self.known_bad_canvas_hashes),
                'known_bad_webgl_signatures': len(self.known_bad_webgl_signatures)
            },
            'thresholds': self.thresholds,
            'timing_thresholds': self.timing_thresholds
        }
    
    def add_known_bad_signature(self, signature_type, signature_value):
        """Add a new known bad signature to the detection system"""
        if signature_type == 'canvas':
            self.known_bad_canvas_hashes.add(signature_value)
            print(f"Added bad canvas hash: {signature_value}")
        elif signature_type == 'webgl':
            self.known_bad_webgl_signatures.add(signature_value)
            print(f"Added bad WebGL signature: {signature_value}")
        else:
            print(f"Unknown signature type: {signature_type}")
    
    def get_signature_stats(self):
        """Get statistics about tracked signatures"""
        canvas_stats = {}
        for signature, ips in self.canvas_signature_tracker.items():
            if len(ips) > 1:
                canvas_stats[signature] = len(ips)
        
        webgl_stats = {}
        for signature, ips in self.webgl_signature_tracker.items():
            if len(ips) > 1:
                webgl_stats[signature] = len(ips)
        
        return {
            'duplicate_canvas_signatures': canvas_stats,
            'duplicate_webgl_signatures': webgl_stats,
            'total_canvas_tracked': len(self.canvas_signature_tracker),
            'total_webgl_tracked': len(self.webgl_signature_tracker)
        }
