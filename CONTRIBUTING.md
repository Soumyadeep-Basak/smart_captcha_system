# 🤝 Contributing to Smart Captcha System

Thank you for your interest in contributing to the Smart Captcha System! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Node.js 16+
- Git
- Basic understanding of machine learning and web security

### Development Environment Setup

1. **Fork and Clone**
```bash
git clone https://github.com/your-username/smart-captcha-system.git
cd smart-captcha-system
```

2. **Backend Setup**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies
```

3. **Frontend Setup**
```bash
cd frontend
npm install
npm run dev
```

4. **Pre-commit Hooks**
```bash
pre-commit install
```

## 📝 Contribution Guidelines

### Code Style

#### Python
- Follow PEP 8 style guide
- Use type hints for function parameters and return values
- Maximum line length: 88 characters (Black formatter)
- Use meaningful variable and function names

```python
def analyze_mouse_behavior(events: List[Dict[str, Any]]) -> Dict[str, float]:
    """Analyze mouse movement patterns for bot detection.
    
    Args:
        events: List of mouse movement events with timestamps and coordinates
        
    Returns:
        Dictionary containing analysis results and confidence scores
    """
    pass
```

#### JavaScript/React
- Use ESLint and Prettier for code formatting
- Prefer functional components with hooks
- Use TypeScript where possible
- Follow React best practices

```javascript
const BehaviorCapture = ({ onDataCapture, isEnabled = true }) => {
  const [events, setEvents] = useState([]);
  
  useEffect(() => {
    if (!isEnabled) return;
    // Event capture logic
  }, [isEnabled]);
  
  return <div>{/* Component JSX */}</div>;
};
```

### Commit Messages

Use conventional commits format:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat(honeypot): add new JavaScript-based trap mechanism
fix(api): resolve race condition in prediction endpoint
docs(readme): update installation instructions
```

## 🐛 Bug Reports

### Before Submitting

1. Check existing issues to avoid duplicates
2. Test with the latest version
3. Provide minimal reproduction steps

### Bug Report Template

```markdown
**Bug Description**
A clear description of the bug.

**Steps to Reproduce**
1. Go to '...'
2. Click on '...'
3. See error

**Expected Behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment**
- OS: [e.g., Windows 10]
- Browser: [e.g., Chrome 91]
- Python Version: [e.g., 3.9.5]
- Node.js Version: [e.g., 16.14.0]
```

## 💡 Feature Requests

### Feature Request Template

```markdown
**Feature Description**
A clear description of the feature you'd like.

**Problem Statement**
What problem does this solve?

**Proposed Solution**
How would you like this implemented?

**Alternative Solutions**
Any alternative approaches considered?

**Additional Context**
Any other context about the feature.
```

## 🧪 Testing

### Running Tests

```bash
# Backend tests
python -m pytest backend/tests/ -v

# Frontend tests
cd frontend && npm test

# Integration tests
python scripts/test_integration.py

# Bot simulation tests
python scripts/test_honeypot_system.py
```

### Writing Tests

#### Python Tests
```python
import pytest
from backend.api.modules.honeypot import HoneypotModule

class TestHoneypotModule:
    def setup_method(self):
        self.honeypot = HoneypotModule()
    
    def test_hidden_field_detection(self):
        metadata = {'hidden_honeypot_field': 'bot-filled-value'}
        result = self.honeypot.analyze([], metadata)
        assert result['honeypot_verdict']['is_bot'] is True
```

#### Frontend Tests
```javascript
import { render, screen, fireEvent } from '@testing-library/react';
import BehaviorCapture from '../components/BehaviorCapture';

test('captures mouse movements correctly', () => {
  const mockCapture = jest.fn();
  render(<BehaviorCapture onDataCapture={mockCapture} />);
  
  fireEvent.mouseMove(screen.getByTestId('capture-area'));
  expect(mockCapture).toHaveBeenCalled();
});
```

## 📦 Pull Request Process

### Before Submitting

1. **Update Documentation**: Ensure README and code comments are updated
2. **Add Tests**: Include tests for new functionality
3. **Check Formatting**: Run linters and formatters
4. **Test Locally**: Verify all tests pass

### Pull Request Template

```markdown
**Description**
Brief description of changes.

**Type of Change**
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

**Testing**
- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] Manual testing completed

**Checklist**
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No merge conflicts
```

### Review Process

1. **Automated Checks**: CI/CD pipeline runs tests and checks
2. **Code Review**: Maintainers review code for quality and correctness
3. **Testing**: Changes tested in staging environment
4. **Approval**: At least one maintainer approval required
5. **Merge**: Squash and merge into main branch

## 🏗️ Architecture Guidelines

### Adding New Detection Modules

1. **Create Module Class**
```python
class NewDetectionModule:
    def __init__(self):
        self.module_name = 'new_detection'
        self.version = '1.0'
    
    def analyze(self, events, metadata):
        # Implementation
        return {
            'analysis': {...},
            'verdict': {...},
            'module_info': {...}
        }
    
    def get_info(self):
        return {
            'module': self.module_name,
            'version': self.version,
            'description': 'Module description'
        }
```

2. **Register in Main API**
```python
# In app.py
new_module = NewDetectionModule()

# In combine_module_results function
new_result = new_module.analyze(events, metadata)
```

3. **Add Tests**
```python
def test_new_detection_module():
    module = NewDetectionModule()
    result = module.analyze(test_events, test_metadata)
    assert 'analysis' in result
    assert 'verdict' in result
```

### Frontend Component Guidelines

1. **Component Structure**
```javascript
// components/NewComponent.jsx
import { useState, useEffect } from 'react';

const NewComponent = ({ prop1, prop2, onEvent }) => {
  const [state, setState] = useState(initialState);
  
  useEffect(() => {
    // Side effects
  }, [dependencies]);
  
  const handleEvent = (event) => {
    // Event handling
    onEvent?.(event);
  };
  
  return (
    <div className="new-component">
      {/* Component JSX */}
    </div>
  );
};

export default NewComponent;
```

2. **State Management**
- Use React hooks for local state
- Use Redux for global state
- Minimize prop drilling

## 📚 Documentation

### Code Documentation

- Use docstrings for Python functions and classes
- Use JSDoc comments for JavaScript functions
- Include examples in documentation
- Keep documentation up to date with code changes

### README Updates

When adding new features:
1. Update feature list
2. Add usage examples
3. Update API documentation
4. Include configuration options

## 🔒 Security Guidelines

### Reporting Security Issues

**DO NOT** open public GitHub issues for security vulnerabilities.

Instead:
1. Email: security@smartcaptcha.dev
2. Include detailed description
3. Provide reproduction steps
4. Allow time for response before disclosure

### Security Best Practices

- Validate all inputs
- Use parameterized queries
- Implement rate limiting
- Follow OWASP guidelines
- Regular dependency updates

## 🎯 Priority Areas

We especially welcome contributions in:

1. **Machine Learning**: New algorithms, feature engineering
2. **Security**: Advanced bot detection techniques
3. **Performance**: Optimization and scalability improvements
4. **Documentation**: Tutorials, examples, and guides
5. **Testing**: Automated tests and validation tools

## 🏆 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Invited to maintainer team (for significant contributions)

## 📞 Getting Help

- **Discord**: Join our community server
- **GitHub Discussions**: Ask questions and share ideas
- **Email**: contributors@smartcaptcha.dev

## 📜 Code of Conduct

Please follow our [Code of Conduct](CODE_OF_CONDUCT.md) in all interactions.

---

Thank you for contributing to making the web more secure and user-friendly! 🚀
