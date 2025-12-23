"""
Configuration constants for Bot Detection System

This module centralizes all configuration values, thresholds, and weights
used across the bot detection modules for better maintainability.
"""

# ML Model Configuration
ML_CONFIG = {
    'threshold': 500,
    'max_threshold': 1500.0,
    'feature_dimensions': 40,
}

# Honeypot Module Configuration
HONEYPOT_CONFIG = {
    'weights': {
        'hidden_field': 0.4,     # Strongest indicator
        'fake_submit': 0.3,      # Strong indicator
        'optional_field': 0.3    # Moderate indicator
    },
    'suspicious_threshold': 0.3,
    'high_threat_threshold': 0.6,
    'behavioral_weight': 0.2,
    'honeypot_weight': 0.8,
}

# Fingerprinting Module Configuration
FINGERPRINTING_CONFIG = {
    'thresholds': {
        'plugins_min': 0,
        'mime_types_min': 0,
        'screen_min_width': 400,
        'screen_min_height': 300,
        'ua_min_length': 20,
        'hardware_concurrency_min': 0,
        'canvas_min_length': 20,
        'webgl_min_length': 10,
    },
    'timing_thresholds': {
        'canvas_render_time_max': 1000,
        'webgl_render_time_max': 2000,
        'plugin_enum_time_max': 500,
    },
    'risk_score_thresholds': {
        'high': 0.8,
        'medium': 0.5,
        'low': 0.3,
        'bot_likely': 0.6,
    },
}

# Module Weight Configuration for Combined Analysis
MODULE_WEIGHTS = {
    'honeypot': 0.45,      # Highest weight - most reliable
    'ml_model': 0.35,      # Medium weight
    'fingerprint': 0.20,   # Supporting evidence
}

# Decision Thresholds
DECISION_THRESHOLDS = {
    'default': 0.4,
    'single_honeypot': 0.25,
    'multiple_honeypots': 0.1,
    'webdriver_detected': 0.2,
    'high_fingerprint_risk': 0.3,
}

# Honeypot Bonus Configuration
HONEYPOT_BONUS = {
    'per_trigger': 0.15,
    'max_bonus': 0.45,
}

# Suspicious Pattern Lists
SUSPICIOUS_PATTERNS = [
    'headless', 'phantom', 'selenium', 'webdriver', 'puppeteer',
    'chrome-headless', 'chromeless', 'bot', 'crawler', 'spider',
    'automation', 'script', 'test'
]

# Known Bad Signatures (can be extended at runtime)
KNOWN_BAD_CANVAS_HASHES = {
    '6a3f5e2c4b8d7a1f',  # Common headless signature
    'e4b8c6d2a5f7e9c1',  # Another headless pattern
    'ffffffffffffffff',  # All-white canvas
    '0000000000000000',  # All-black canvas
    'abcdef1234567890',  # Generic test signature
    '1234567890abcdef',  # Another test pattern
}

KNOWN_BAD_WEBGL_SIGNATURES = {
    'mesa',       # Common in headless environments
    'vmware',     # Virtual machine signatures
    'virtual',    # Virtual GPU signatures
    'software',   # Software rendering
    'null',       # Null renderer
}

# Automation Detection Signatures
AUTOMATION_SIGNATURES = [
    'navigator.webdriver',
    'window.cdc_',
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

# Logging Configuration
LOGGING_CONFIG = {
    'max_predictions_stored': 1000,
    'log_level': 'INFO',
}

# API Configuration
API_CONFIG = {
    'version': '3.0',
    'architecture': 'modular_single_api',
}
