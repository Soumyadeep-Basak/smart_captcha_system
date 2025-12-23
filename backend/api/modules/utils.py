"""
Utility Functions for Bot Detection System

This module provides common utility functions used across
different detection modules.
"""

from typing import List, Dict, Any, Tuple
import hashlib
import re
from datetime import datetime


def calculate_variance(values: List[float]) -> float:
    """
    Calculate variance of a list of values.
    
    Args:
        values: List of numeric values
        
    Returns:
        Variance of the values
    """
    if not values or len(values) < 2:
        return 0.0
    
    mean = sum(values) / len(values)
    variance = sum((x - mean) ** 2 for x in values) / len(values)
    return variance


def calculate_entropy(text: str) -> float:
    """
    Calculate Shannon entropy of a string.
    
    Args:
        text: Input string
        
    Returns:
        Entropy value
    """
    if not text:
        return 0.0
    
    import math
    
    # Count character frequencies
    char_counts = {}
    for char in text:
        char_counts[char] = char_counts.get(char, 0) + 1
    
    # Calculate entropy
    length = len(text)
    entropy = 0.0
    for count in char_counts.values():
        probability = count / length
        entropy -= probability * math.log2(probability)
    
    return entropy


def generate_hash(elements: List[str], hash_length: int = 16) -> str:
    """
    Generate a hash from multiple elements.
    
    Args:
        elements: List of string elements to hash
        hash_length: Length of the resulting hash
        
    Returns:
        Hash string
    """
    try:
        combined = '|'.join(str(elem) for elem in elements)
        hash_object = hashlib.sha256(combined.encode())
        return hash_object.hexdigest()[:hash_length]
    except Exception:
        return 'unknown'


def normalize_score(value: float, min_val: float = 0.0, max_val: float = 1.0) -> float:
    """
    Normalize a score to a specific range.
    
    Args:
        value: Input value
        min_val: Minimum value of output range
        max_val: Maximum value of output range
        
    Returns:
        Normalized score
    """
    return max(min_val, min(max_val, value))


def extract_browser_os_from_ua(user_agent: str) -> Tuple[str, str, bool]:
    """
    Extract browser, OS, and mobile status from user agent.
    
    Args:
        user_agent: User agent string
        
    Returns:
        Tuple of (browser, os, is_mobile)
    """
    if not user_agent:
        return 'unknown', 'unknown', False
    
    ua_lower = user_agent.lower()
    
    # Detect browser
    browser = 'unknown'
    if 'chrome' in ua_lower and 'edge' not in ua_lower:
        browser = 'chrome'
    elif 'firefox' in ua_lower:
        browser = 'firefox'
    elif 'safari' in ua_lower and 'chrome' not in ua_lower:
        browser = 'safari'
    elif 'edge' in ua_lower:
        browser = 'edge'
    elif 'opera' in ua_lower or 'opr' in ua_lower:
        browser = 'opera'
    
    # Detect OS
    os = 'unknown'
    is_mobile = False
    
    if 'windows' in ua_lower:
        os = 'windows'
    elif 'mac' in ua_lower and 'iphone' not in ua_lower and 'ipad' not in ua_lower:
        os = 'macos'
    elif 'linux' in ua_lower and 'android' not in ua_lower:
        os = 'linux'
    elif 'android' in ua_lower:
        os = 'android'
        is_mobile = True
    elif 'iphone' in ua_lower or 'ipad' in ua_lower or 'ipod' in ua_lower:
        os = 'ios'
        is_mobile = True
    
    return browser, os, is_mobile


def check_pattern_match(text: str, patterns: List[str]) -> Tuple[bool, List[str]]:
    """
    Check if text matches any of the provided patterns.
    
    Args:
        text: Text to check
        patterns: List of patterns to match against
        
    Returns:
        Tuple of (matched, list of matched patterns)
    """
    if not text:
        return False, []
    
    text_lower = text.lower()
    matched_patterns = []
    
    for pattern in patterns:
        if pattern.lower() in text_lower:
            matched_patterns.append(pattern)
    
    return len(matched_patterns) > 0, matched_patterns


def calculate_time_statistics(timestamps: List[float]) -> Dict[str, float]:
    """
    Calculate timing statistics from a list of timestamps.
    
    Args:
        timestamps: List of timestamp values
        
    Returns:
        Dictionary with timing statistics
    """
    if not timestamps or len(timestamps) < 2:
        return {
            'avg_time': 0.0,
            'min_time': 0.0,
            'max_time': 0.0,
            'variance': 0.0,
            'is_regular': False
        }
    
    # Calculate time differences
    time_diffs = [timestamps[i] - timestamps[i-1] for i in range(1, len(timestamps))]
    
    if not time_diffs:
        return {
            'avg_time': 0.0,
            'min_time': 0.0,
            'max_time': 0.0,
            'variance': 0.0,
            'is_regular': False
        }
    
    avg_time = sum(time_diffs) / len(time_diffs)
    min_time = min(time_diffs)
    max_time = max(time_diffs)
    variance = calculate_variance(time_diffs)
    
    # Check if timing is suspiciously regular
    unique_diffs = len(set(time_diffs))
    is_regular = unique_diffs < len(time_diffs) * 0.3
    
    return {
        'avg_time': avg_time,
        'min_time': min_time,
        'max_time': max_time,
        'variance': variance,
        'is_regular': is_regular
    }


def is_valid_ip(ip_address: str) -> bool:
    """
    Validate IP address format.
    
    Args:
        ip_address: IP address string
        
    Returns:
        True if valid, False otherwise
    """
    if not ip_address:
        return False
    
    # IPv4 pattern
    ipv4_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if re.match(ipv4_pattern, ip_address):
        parts = ip_address.split('.')
        return all(0 <= int(part) <= 255 for part in parts)
    
    # IPv6 pattern (simplified)
    ipv6_pattern = r'^([0-9a-fA-F]{0,4}:){7}[0-9a-fA-F]{0,4}$'
    if re.match(ipv6_pattern, ip_address):
        return True
    
    return False


def classify_ip_type(ip_address: str) -> str:
    """
    Classify IP address type.
    
    Args:
        ip_address: IP address string
        
    Returns:
        IP type classification
    """
    if not ip_address:
        return 'unknown'
    
    # Localhost
    if ip_address in ['127.0.0.1', '::1', 'localhost']:
        return 'localhost'
    
    # Private IP ranges
    if (ip_address.startswith('192.168.') or
        ip_address.startswith('10.') or
        ip_address.startswith('172.16.') or
        ip_address.startswith('172.31.')):
        return 'private'
    
    return 'public'


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    Safely divide two numbers, returning default on division by zero.
    
    Args:
        numerator: Numerator value
        denominator: Denominator value
        default: Default value to return on division by zero
        
    Returns:
        Division result or default
    """
    try:
        if denominator == 0:
            return default
        return numerator / denominator
    except (TypeError, ValueError):
        return default


def clamp(value: float, min_val: float, max_val: float) -> float:
    """
    Clamp a value between minimum and maximum bounds.
    
    Args:
        value: Value to clamp
        min_val: Minimum bound
        max_val: Maximum bound
        
    Returns:
        Clamped value
    """
    return max(min_val, min(max_val, value))


def get_timestamp_iso() -> str:
    """
    Get current timestamp in ISO format with UTC timezone.
    
    Returns:
        ISO-formatted timestamp string
    """
    return datetime.utcnow().isoformat() + 'Z'


def truncate_string(text: str, max_length: int = 50, suffix: str = '...') -> str:
    """
    Truncate a string to a maximum length.
    
    Args:
        text: Input text
        max_length: Maximum length
        suffix: Suffix to add when truncating
        
    Returns:
        Truncated string
    """
    if not text or len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix
