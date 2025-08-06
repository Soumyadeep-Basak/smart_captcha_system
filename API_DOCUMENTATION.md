# 🛡️ Smart Captcha System - API Documentation

## Overview

The Smart Captcha System provides a REST API for bot detection using advanced behavioral analysis, machine learning, and honeypot mechanisms. This API is designed to integrate seamlessly with existing web applications.

## Base URL

```
http://localhost:5000
```

## Authentication

Currently, the API does not require authentication for local development. For production deployment, implement appropriate authentication mechanisms.

## Endpoints

### 1. Health Check

Check the system's health and module status.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "service": "unified_bot_detection_api",
  "timestamp": "2025-08-07T10:30:00.000Z",
  "architecture": "modular_single_api",
  "modules": {
    "ml_model": {
      "module": "ml_model",
      "version": "2.0",
      "status": "loaded",
      "models_available": ["autoencoder_mouse", "autoencoder_keystroke"]
    },
    "honeypot": {
      "module": "enhanced_honeypot",
      "version": "2.0",
      "honeypot_types": ["hidden_css_field", "fake_submit_button", "js_optional_field"]
    },
    "fingerprinting": {
      "module": "fingerprinting",
      "version": "1.0",
      "features": ["canvas", "webgl", "browser_info"]
    }
  }
}
```

### 2. Bot Detection (Main Endpoint)

Analyze user behavior and detect bots using multiple detection methods.

**Endpoint:** `POST /predict`

**Request Body:**
```json
{
  "mouseMoveCount": 150,
  "keyPressCount": 45,
  "events": [
    {
      "event_name": "mousemove",
      "x_position": 245,
      "y_position": 156,
      "timestamp": 1691395200000
    },
    {
      "event_name": "keypress",
      "key": "a",
      "timestamp": 1691395201000
    }
  ],
  "honeypot_data": {
    "hidden_honeypot_field": "",
    "fake_submit_clicked": false,
    "js_optional_field": "",
    "js_enabled": true,
    "honeypot_triggers": {
      "hidden_field": false,
      "fake_submit": false,
      "js_optional": false
    }
  },
  "browserFingerprint": {
    "webdriver_detected": false,
    "plugins_count": 5,
    "mime_types_count": 4,
    "canvas_hash": "a1b2c3d4e5f6",
    "webgl_supported": true,
    "screen_width": 1920,
    "screen_height": 1080
  },
  "metadata": {
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "timestamp": "2025-08-07T10:30:00.000Z"
  }
}
```

**Response:**
```json
{
  "ip_address": "127.0.0.1",
  "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
  "current_timestamp": "2025-08-07T10:30:00.000Z",
  "mouseMoveCount": 150,
  "keyPressCount": 45,
  "prediction": [
    {
      "bot": false,
      "reconstruction_error": 0.15,
      "confidence": 0.92,
      "raw_error": 0.15
    }
  ],
  "enhanced_analysis": {
    "final_verdict": {
      "is_bot": false,
      "confidence": 0.89,
      "bot_probability": 0.12,
      "risk_level": "low",
      "recommendation": "allow",
      "decision_threshold": 0.4,
      "decision_logic": "weighted_probability(0.12) > adaptive_threshold(0.4) = false"
    },
    "ml_analysis": {
      "bot_detected": false,
      "reconstruction_error": 0.15,
      "confidence": 0.85,
      "method": "autoencoder_ensemble",
      "threshold": 300
    },
    "honeypot_analysis": {
      "threat_detected": false,
      "threat_level": "low",
      "honeypot_score": 0.0,
      "confidence": 0.9,
      "honeypot_summary": {
        "total_honeypots": 3,
        "triggered_honeypots": 0,
        "detection_method": "multi_layer_honeypot"
      },
      "honeypot_details": {
        "detailed_results": {
          "hidden_field": {
            "triggered": false,
            "score": 0.0,
            "details": ""
          },
          "fake_submit": {
            "triggered": false,
            "score": 0.0,
            "details": ""
          },
          "optional_field": {
            "triggered": false,
            "score": 0.0,
            "details": ""
          }
        }
      }
    },
    "fingerprint_analysis": {
      "risk_level": "low",
      "risk_score": 0.1,
      "is_suspicious": false,
      "confidence": 0.88,
      "feature_analysis": {
        "webdriver_detected": false,
        "plugins_count": 5,
        "mime_types_count": 4,
        "screen_suspicious": false
      }
    }
  },
  "api_metadata": {
    "architecture": "modular_single_api",
    "modules_used": ["ml_model", "honeypot", "fingerprinting"],
    "processing_timestamp": "2025-08-07T10:30:00.000Z",
    "version": "3.0"
  }
}
```

### 3. Detailed Analysis

Get comprehensive analysis breakdown for debugging and research.

**Endpoint:** `POST /analyze/detailed`

**Request Body:** Same as `/predict`

**Response:**
```json
{
  "timestamp": "2025-08-07T10:30:00.000Z",
  "input_analysis": {
    "events_count": 195,
    "metadata": {...},
    "browser_fingerprint_features": 8,
    "enhanced_features": {
      "webdriver_detected": false,
      "plugins_count": 5,
      "mime_types_count": 4,
      "suspicious_patterns": []
    }
  },
  "module_results": {
    "ml_model": {...},
    "honeypot": {...},
    "enhanced_fingerprinting": {...}
  },
  "combined_analysis": {...},
  "api_info": {
    "architecture": "modular_single_api_enhanced",
    "version": "3.1",
    "fingerprinting_features": "rule_based_enhanced"
  }
}
```

### 4. Historical Predictions

Retrieve stored prediction data for analysis and monitoring.

**Endpoint:** `GET /predictions`

**Query Parameters:**
- `limit` (optional): Number of predictions to return (default: 50)
- `offset` (optional): Number of predictions to skip (default: 0)

**Response:**
```json
[
  {
    "ipAddress": "127.0.0.1",
    "userAgent": "Mozilla/5.0...",
    "timestamp": "2025-08-07T10:30:00.000Z",
    "mouseMoveCount": 150,
    "keyPressCount": 45,
    "isBot": false,
    "prediction": [{"bot": false, "reconstruction_error": 0.15}],
    "enhanced_analysis": {...},
    "browserFeatures": {...},
    "fingerprintRisk": {...}
  }
]
```

### 5. Module Information

Get information about available detection modules.

**Endpoint:** `GET /modules/info`

**Response:**
```json
{
  "api": "unified_bot_detection",
  "architecture": "modular_single_api",
  "modules": {
    "ml_model": {
      "module": "ml_model",
      "version": "2.0",
      "description": "Autoencoder-based behavioral analysis",
      "features": ["mouse_movement", "keystroke_dynamics"]
    },
    "honeypot": {
      "module": "enhanced_honeypot",
      "version": "2.0",
      "honeypot_types": ["hidden_css_field", "fake_submit_button", "js_optional_field"],
      "description": "3-layer honeypot system for advanced bot detection"
    },
    "fingerprinting": {
      "module": "fingerprinting",
      "version": "1.0",
      "features": ["canvas", "webgl", "browser_info"],
      "description": "Browser fingerprinting for device identification"
    }
  }
}
```

## Request/Response Details

### Event Object Structure

Each event in the `events` array should follow this structure:

```json
{
  "event_name": "mousemove|keypress|click|scroll",
  "x_position": 245,        // For mouse events
  "y_position": 156,        // For mouse events
  "key": "a",              // For keyboard events
  "timestamp": 1691395200000  // Unix timestamp in milliseconds
}
```

### Honeypot Data Structure

The `honeypot_data` object contains:

```json
{
  "hidden_honeypot_field": "",      // Value of hidden field (should be empty)
  "fake_submit_clicked": false,     // Whether fake submit was clicked
  "js_optional_field": "",          // Value of JS optional field
  "js_enabled": true,               // Whether JavaScript is enabled
  "honeypot_triggers": {
    "hidden_field": false,          // Whether hidden field was filled
    "fake_submit": false,           // Whether fake submit was clicked
    "js_optional": false            // Whether JS field was filled incorrectly
  }
}
```

### Browser Fingerprint Structure

The `browserFingerprint` object includes:

```json
{
  "webdriver_detected": false,     // Selenium/automation detection
  "plugins_count": 5,              // Number of browser plugins
  "mime_types_count": 4,           // Number of MIME types
  "canvas_hash": "a1b2c3d4e5f6",   // Canvas fingerprint hash
  "webgl_supported": true,         // WebGL capability
  "screen_width": 1920,            // Screen resolution width
  "screen_height": 1080,           // Screen resolution height
  "timezone_offset": -300,         // Timezone offset in minutes
  "language": "en-US",             // Browser language
  "platform": "Win32"             // Operating system platform
}
```

## Error Handling

### Error Response Format

```json
{
  "error": "Error description",
  "status_code": 400,
  "timestamp": "2025-08-07T10:30:00.000Z",
  "details": {
    "field": "Specific error details"
  }
}
```

### Common Error Codes

| Code | Description |
|------|-------------|
| 400 | Bad Request - Invalid input data |
| 404 | Not Found - Endpoint not found |
| 500 | Internal Server Error - Processing error |
| 503 | Service Unavailable - Module loading error |

### Error Examples

**Missing Required Fields:**
```json
{
  "error": "mouseMoveCount, keyPressCount, and events are required",
  "status_code": 400,
  "timestamp": "2025-08-07T10:30:00.000Z"
}
```

**Invalid Event Format:**
```json
{
  "error": "Invalid event format",
  "status_code": 400,
  "details": {
    "event_index": 5,
    "missing_field": "timestamp"
  }
}
```

## Rate Limiting

The API implements rate limiting to prevent abuse:

- **Default Limit**: 100 requests per minute per IP
- **Burst Limit**: 10 requests per second
- **Headers**: Rate limit information included in response headers

**Rate Limit Headers:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1691395260
```

## Integration Examples

### JavaScript/React Integration

```javascript
const detectBot = async (behaviorData) => {
  try {
    const response = await fetch('http://localhost:5000/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(behaviorData)
    });
    
    const result = await response.json();
    
    if (result.enhanced_analysis?.final_verdict?.is_bot) {
      // Handle bot detection
      console.log('Bot detected:', result.enhanced_analysis.final_verdict);
      return true;
    }
    
    return false;
  } catch (error) {
    console.error('Detection error:', error);
    return false; // Fail open
  }
};
```

### Python Integration

```python
import requests
import json

def detect_bot(behavior_data):
    """Detect if user behavior indicates bot activity."""
    try:
        response = requests.post(
            'http://localhost:5000/predict',
            json=behavior_data,
            timeout=5
        )
        response.raise_for_status()
        
        result = response.json()
        final_verdict = result.get('enhanced_analysis', {}).get('final_verdict', {})
        
        return {
            'is_bot': final_verdict.get('is_bot', False),
            'confidence': final_verdict.get('confidence', 0),
            'analysis': result.get('enhanced_analysis', {})
        }
        
    except requests.RequestException as e:
        print(f"Detection error: {e}")
        return {'is_bot': False, 'confidence': 0}  # Fail open
```

### cURL Examples

**Basic Detection:**
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "mouseMoveCount": 50,
    "keyPressCount": 20,
    "events": [
      {"event_name": "mousemove", "x_position": 100, "y_position": 200, "timestamp": 1691395200000}
    ],
    "honeypot_data": {"hidden_honeypot_field": "", "fake_submit_clicked": false},
    "metadata": {"user_agent": "Mozilla/5.0..."}
  }'
```

**Health Check:**
```bash
curl -X GET http://localhost:5000/health
```

## Best Practices

### 1. Data Collection
- Collect events continuously during user interaction
- Include sufficient context (at least 10-20 events)
- Capture both mouse and keyboard events when possible

### 2. Error Handling
- Implement fallback behavior for API failures
- Use exponential backoff for retries
- Log errors for debugging

### 3. Performance
- Batch events when possible
- Cache results for repeated requests
- Monitor API response times

### 4. Security
- Validate data before sending to API
- Use HTTPS in production
- Implement proper authentication
- Rate limit client-side requests

## Monitoring and Debugging

### Debug Mode

Enable debug mode by setting environment variable:
```bash
FLASK_ENV=development
LOG_LEVEL=DEBUG
```

### Logging

The API logs detailed information for debugging:
- Request/response data
- Module execution times
- Detection decisions
- Error details

### Health Monitoring

Monitor these metrics:
- API response time
- Detection accuracy
- Error rates
- Module availability

---

For additional support or questions, please refer to the [main documentation](README.md) or open an issue on GitHub.
