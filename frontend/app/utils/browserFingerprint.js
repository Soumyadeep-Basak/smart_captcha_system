// Browser Fingerprinting Utility - Advanced Bot Detection
// Collects browser features that are commonly spoofed or missing in bots

export const collectBrowserFingerprint = () => {
  const fingerprint = {};

  try {
    // 🔥 Very High Priority Features
    
    // 1. navigator.webdriver - Detects headless Chrome, Puppeteer
    fingerprint.webdriver_detected = navigator.webdriver || false;
    
    // 2. navigator.plugins.length - Bots usually return 0
    fingerprint.plugins_count = navigator.plugins ? navigator.plugins.length : 0;
    fingerprint.plugins_list = navigator.plugins ? 
      Array.from(navigator.plugins).map(plugin => plugin.name).slice(0, 5) : []; // First 5 plugins
    
    // 3. navigator.mimeTypes.length - Similar to plugins
    fingerprint.mime_types_count = navigator.mimeTypes ? navigator.mimeTypes.length : 0;
    
    // ✅ High Priority Features
    
    // 4. User-Agent Analysis
    fingerprint.user_agent = navigator.userAgent || '';
    fingerprint.user_agent_length = fingerprint.user_agent.length;
    
    // Check for suspicious user agent patterns
    const suspiciousPatterns = [
      'headless', 'phantom', 'selenium', 'webdriver', 'puppeteer', 
      'chrome-headless', 'chromeless', 'bot', 'crawler', 'spider'
    ];
    fingerprint.suspicious_ua_patterns = suspiciousPatterns.filter(pattern => 
      fingerprint.user_agent.toLowerCase().includes(pattern)
    );
    
    // ⚠️ Medium Priority Features
    
    // 5. Screen size - Bots sometimes return 0x0 or odd values
    fingerprint.screen_width = screen.width || 0;
    fingerprint.screen_height = screen.height || 0;
    fingerprint.screen_color_depth = screen.colorDepth || 0;
    fingerprint.screen_pixel_depth = screen.pixelDepth || 0;
    
    // Detect suspicious screen sizes
    fingerprint.suspicious_screen = (
      fingerprint.screen_width === 0 || 
      fingerprint.screen_height === 0 ||
      fingerprint.screen_width === fingerprint.screen_height || // Square screens are rare
      (fingerprint.screen_width < 800 && fingerprint.screen_height < 600) // Very small screens
    );
    
    // ⚠️ Low Priority Features
    
    // 6. Touch support - Detects mobile emulation failures
    fingerprint.max_touch_points = navigator.maxTouchPoints || 0;
    fingerprint.touch_support = 'ontouchstart' in window;
    
    // Additional Advanced Features
    
    // 7. Language and timezone detection
    fingerprint.language = navigator.language || '';
    fingerprint.languages = navigator.languages ? navigator.languages.slice(0, 3) : [];
    fingerprint.timezone = Intl.DateTimeFormat().resolvedOptions().timeZone || '';
    
    // 8. Hardware concurrency
    fingerprint.hardware_concurrency = navigator.hardwareConcurrency || 0;
    
    // 9. Platform information
    fingerprint.platform = navigator.platform || '';
    fingerprint.os_cpu = navigator.oscpu || '';
    
    // 10. Browser features
    fingerprint.cookie_enabled = navigator.cookieEnabled || false;
    fingerprint.do_not_track = navigator.doNotTrack || '';
    
    // 11. Window properties
    fingerprint.window_outer_width = window.outerWidth || 0;
    fingerprint.window_outer_height = window.outerHeight || 0;
    fingerprint.window_inner_width = window.innerWidth || 0;
    fingerprint.window_inner_height = window.innerHeight || 0;
    
    // 12. Device memory (if supported)
    fingerprint.device_memory = navigator.deviceMemory || 0;
    
    // 13. Connection information (if supported)
    if (navigator.connection) {
      fingerprint.connection_type = navigator.connection.effectiveType || '';
      fingerprint.connection_downlink = navigator.connection.downlink || 0;
    }
    
    // 14. Permissions API
    fingerprint.permissions_supported = 'permissions' in navigator;
    
    // 15. WebGL fingerprinting
    try {
      const canvas = document.createElement('canvas');
      const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
      if (gl) {
        fingerprint.webgl_vendor = gl.getParameter(gl.VENDOR) || '';
        fingerprint.webgl_renderer = gl.getParameter(gl.RENDERER) || '';
        fingerprint.webgl_supported = true;
      } else {
        fingerprint.webgl_supported = false;
      }
    } catch (e) {
      fingerprint.webgl_supported = false;
    }
    
    // 16. Canvas fingerprinting
    try {
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      ctx.textBaseline = 'top';
      ctx.font = '14px Arial';
      ctx.fillText('Browser fingerprint test 🤖', 2, 2);
      fingerprint.canvas_fingerprint = canvas.toDataURL().slice(-50); // Last 50 chars
      fingerprint.canvas_supported = true;
    } catch (e) {
      fingerprint.canvas_supported = false;
    }
    
    // 17. Performance API
    fingerprint.performance_supported = 'performance' in window;
    fingerprint.performance_timing_supported = window.performance && 'timing' in window.performance;
    
    // 18. Storage availability
    fingerprint.local_storage_supported = 'localStorage' in window;
    fingerprint.session_storage_supported = 'sessionStorage' in window;
    fingerprint.indexed_db_supported = 'indexedDB' in window;
    
    // 19. Audio context
    try {
      const audioContext = new (window.AudioContext || window.webkitAudioContext)();
      fingerprint.audio_context_supported = true;
      fingerprint.audio_sample_rate = audioContext.sampleRate || 0;
      audioContext.close();
    } catch (e) {
      fingerprint.audio_context_supported = false;
    }
    
    // 20. Battery API (deprecated but might be available)
    fingerprint.battery_supported = 'getBattery' in navigator;
    
    // 21. Gamepad API
    fingerprint.gamepad_supported = 'getGamepads' in navigator;
    
    // 22. Media devices
    fingerprint.media_devices_supported = 'mediaDevices' in navigator;
    
    // 23. Notification API
    fingerprint.notification_permission = 'Notification' in window ? Notification.permission : 'unsupported';
    
    // 24. Clipboard API
    fingerprint.clipboard_supported = 'clipboard' in navigator;
    
    // 🚀 ADVANCED AUTOMATION DETECTION
    
    // 25. Automation signatures detection
    const automationSignatures = [];
    
    // Check for webdriver properties
    if ('webdriver' in navigator) automationSignatures.push('navigator.webdriver');
    if (window.cdc_adoQpoasnfa76pfcZLmcfl_Array) automationSignatures.push('window.cdc_');
    if (window._phantom) automationSignatures.push('_phantom');
    if (window._selenium) automationSignatures.push('_selenium');
    if (window.callPhantom) automationSignatures.push('callPhantom');
    if (window.callSelenium) automationSignatures.push('callSelenium');
    if (window.__webdriver_script_fn) automationSignatures.push('__webdriver_script_fn');
    if (window.__webdriver_evaluate) automationSignatures.push('__webdriver_evaluate');
    if (window.__webdriver_unwrapped) automationSignatures.push('__webdriver_unwrapped');
    if (window.__fxdriver_unwrapped) automationSignatures.push('__fxdriver_unwrapped');
    if (window.__driver_evaluate) automationSignatures.push('__driver_evaluate');
    if (window.__webdriver_script_func) automationSignatures.push('__webdriver_script_func');
    if (window.__webdriver_script_function) automationSignatures.push('__webdriver_script_function');
    
    fingerprint.automation_signatures = automationSignatures;
    
    // 26. Missing window properties detection
    const expectedProperties = ['outerHeight', 'outerWidth', 'screenY', 'screenX', 'scrollX', 'scrollY'];
    const missingProperties = [];
    
    expectedProperties.forEach(prop => {
      if (!(prop in window) || window[prop] === undefined) {
        missingProperties.push(prop);
      }
    });
    
    fingerprint.missing_window_properties = missingProperties;
    
    // 27. Phantom-specific detection
    const phantomIndicators = [];
    if (window._phantom) phantomIndicators.push('window._phantom');
    if (window.phantom) phantomIndicators.push('window.phantom');
    if (window.callPhantom) phantomIndicators.push('window.callPhantom');
    if (navigator.userAgent.includes('PhantomJS')) phantomIndicators.push('PhantomJS_userAgent');
    
    fingerprint.phantom_indicators = phantomIndicators;
    
    // 28. Selenium-specific detection
    const seleniumIndicators = [];
    if (window.selenium) seleniumIndicators.push('window.selenium');
    if (window._selenium) seleniumIndicators.push('window._selenium');
    if (window.__selenium_unwrapped) seleniumIndicators.push('window.__selenium_unwrapped');
    if (document.documentElement.getAttribute('webdriver')) seleniumIndicators.push('webdriver_attribute');
    
    fingerprint.selenium_indicators = seleniumIndicators;
    
    // 29. Chrome headless detection
    let chromeHeadless = false;
    
    // Check for missing chrome properties
    if (window.chrome && (!window.chrome.runtime || !window.chrome.runtime.onConnect)) {
      chromeHeadless = true;
    }
    
    // Check for headless user agent
    if (navigator.userAgent.includes('HeadlessChrome')) {
      chromeHeadless = true;
    }
    
    // Check for missing window chrome object
    if (!window.chrome) {
      chromeHeadless = true;
    }
    
    fingerprint.chrome_headless_detected = chromeHeadless;
    
    // 30. Enhanced navigator properties
    fingerprint.navigator_properties = {
      languages: navigator.languages || [],
      connection: navigator.connection ? {
        effectiveType: navigator.connection.effectiveType,
        downlink: navigator.connection.downlink,
        rtt: navigator.connection.rtt
      } : null,
      cookieEnabled: navigator.cookieEnabled,
      onLine: navigator.onLine,
      doNotTrack: navigator.doNotTrack
    };
    
    // 31. iframe support detection
    fingerprint.iframe_support = 'HTMLIFrameElement' in window;
    
    // 32. Font enumeration (basic)
    const testFonts = ['Arial', 'Times New Roman', 'Courier New', 'Helvetica', 'Georgia', 'Verdana'];
    const detectedFonts = [];
    
    testFonts.forEach(font => {
      const testElement = document.createElement('span');
      testElement.style.fontFamily = font;
      testElement.style.fontSize = '12px';
      testElement.textContent = 'mmmmmmmmmmlli';
      testElement.style.position = 'absolute';
      testElement.style.left = '-9999px';
      document.body.appendChild(testElement);
      
      if (testElement.offsetWidth > 0) {
        detectedFonts.push(font);
      }
      
      document.body.removeChild(testElement);
    });
    
    fingerprint.fonts_count = detectedFonts.length;
    fingerprint.fonts_list = detectedFonts;
    
    // Add timestamp
    fingerprint.fingerprint_timestamp = Date.now();
    
    console.log('🔍 Browser fingerprint collected:', fingerprint);
    return fingerprint;
    
  } catch (error) {
    console.error('❌ Error collecting browser fingerprint:', error);
    return {
      error: error.message,
      webdriver_detected: false,
      plugins_count: 0,
      mime_types_count: 0,
      user_agent: '',
      screen_width: 0,
      screen_height: 0,
      max_touch_points: 0,
      fingerprint_timestamp: Date.now()
    };
  }
};

// Rule-based bot detection scores for frontend preview
export const calculateFingerprintRisk = (fingerprint) => {
  let riskScore = 0;
  const riskFactors = [];
  
  // 🔥 CRITICAL: Zero features pattern (headless detection)
  const zeroFeatures = [];
  if (fingerprint.plugins_count === 0) zeroFeatures.push('plugins');
  if (fingerprint.mime_types_count === 0) zeroFeatures.push('mime_types');
  if (fingerprint.fonts_count === 0) zeroFeatures.push('fonts');
  
  if (zeroFeatures.length >= 2) {
    riskScore += 0.9;
    riskFactors.push(`headless_pattern_${zeroFeatures.length}_features`);
  } else if (zeroFeatures.length === 1) {
    riskScore += 0.4;
    riskFactors.push(`single_zero_${zeroFeatures[0]}`);
  }
  
  // 🔥 Very High Risk Indicators
  if (fingerprint.webdriver_detected) {
    riskScore += 0.9;
    riskFactors.push('webdriver_detected');
  }
  
  if (fingerprint.automation_signatures && fingerprint.automation_signatures.length > 0) {
    riskScore += 0.8;
    riskFactors.push(`automation_signatures_${fingerprint.automation_signatures.length}`);
  }
  
  if (fingerprint.chrome_headless_detected) {
    riskScore += 0.9;
    riskFactors.push('chrome_headless');
  }
  
  if (fingerprint.phantom_indicators && fingerprint.phantom_indicators.length > 0) {
    riskScore += 0.8;
    riskFactors.push(`phantom_detected_${fingerprint.phantom_indicators.length}`);
  }
  
  if (fingerprint.selenium_indicators && fingerprint.selenium_indicators.length > 0) {
    riskScore += 0.8;
    riskFactors.push(`selenium_detected_${fingerprint.selenium_indicators.length}`);
  }
  
  // ✅ High Risk Indicators
  if (fingerprint.suspicious_ua_patterns && fingerprint.suspicious_ua_patterns.length > 0) {
    riskScore += 0.7;
    riskFactors.push('suspicious_user_agent');
  }
  
  if (fingerprint.missing_window_properties && fingerprint.missing_window_properties.length >= 2) {
    riskScore += 0.6;
    riskFactors.push(`missing_properties_${fingerprint.missing_window_properties.length}`);
  }
  
  if (fingerprint.user_agent_length < 50) {
    riskScore += 0.5;
    riskFactors.push('short_user_agent');
  }
  
  // ⚠️ Medium Risk Indicators
  if (fingerprint.suspicious_screen) {
    riskScore += 0.4;
    riskFactors.push('suspicious_screen_size');
  }
  
  if (!fingerprint.webgl_supported) {
    riskScore += 0.3;
    riskFactors.push('no_webgl');
  }
  
  if (!fingerprint.canvas_supported) {
    riskScore += 0.3;
    riskFactors.push('no_canvas');
  }
  
  if (!fingerprint.iframe_support) {
    riskScore += 0.3;
    riskFactors.push('no_iframe_support');
  }
  
  // Low Risk Indicators
  if (fingerprint.hardware_concurrency === 0) {
    riskScore += 0.2;
    riskFactors.push('no_hardware_info');
  }
  
  if (!fingerprint.navigator_properties || !fingerprint.navigator_properties.languages || fingerprint.navigator_properties.languages.length === 0) {
    riskScore += 0.2;
    riskFactors.push('no_languages');
  }
  
  if (fingerprint.notification_permission === 'undefined' || !fingerprint.notification_permission) {
    riskScore += 0.2;
    riskFactors.push('undefined_notifications');
  }
  
  return {
    riskScore: Math.min(riskScore, 1.0),
    riskFactors,
    riskLevel: riskScore >= 0.8 ? 'CRITICAL' : (riskScore >= 0.6 ? 'HIGH' : (riskScore >= 0.4 ? 'MEDIUM' : 'LOW')),
    isBot: riskScore >= 0.6,
    zeroFeaturesCount: zeroFeatures.length,
    automationSignatures: fingerprint.automation_signatures?.length || 0
  };
};
