# 🚀 Enterprise-Grade Python Automation Framework

A professional, scalable automation testing framework built with Python, Selenium, and Pytest. Designed for enterprise-level testing with advanced features like retry mechanisms, comprehensive logging, screenshot capture, and parallel execution support.

## ✨ Key Features

- **🔄 Retry Mechanisms**: Built-in retry logic for flaky elements and network issues
- **📸 Screenshot Capture**: Automatic screenshots on test failures and key actions
- **📝 Comprehensive Logging**: Structured logging with file and console output
- **⚙️ Centralized Configuration**: Environment-based configuration management
- **🖥️ Multi-Browser Support**: Chrome, Firefox, and Edge with optimized options
- **📊 Advanced Reporting**: Allure and HTML reporting with metadata
- **🧪 Page Object Model**: Clean, maintainable page object implementation
- **📁 Test Data Management**: Centralized test data with JSON configuration
- **🚀 Parallel Execution**: Support for concurrent test execution
- **🐳 Docker Ready**: Containerized execution support

## 🏗️ Architecture Overview

```
AutomationFramework/
├── config/                 # Configuration management
│   ├── settings.py        # Centralized settings
│   └── browser_setup.py   # Browser initialization
├── pages/                 # Page Object Model
│   ├── base_page.py       # Base page with common functionality
│   ├── github_cli_page.py # GitHub CLI page object
│   └── login_page.py      # Login page object
├── tests/                 # Test suites
│   ├── test_github_cli.py # GitHub CLI tests
│   └── test_login.py      # Login tests
├── utils/                 # Utility classes
│   ├── logger.py          # Logging utility
│   ├── retry_mechanism.py # Retry logic
│   ├── screenshot_capture.py # Screenshot utility
│   └── test_data_loader.py # Test data management
├── test_data/             # Test data files
│   └── test_data.json     # Centralized test data
├── logs/                  # Execution logs
├── screenshots/           # Test screenshots
├── reports/               # Test reports
├── docs/                  # Documentation
│   ├── README.md          # Documentation index
│   └── SPANISH_GUIDE.md   # Spanish guide for beginners
└── conftest.py           # Pytest configuration
```

## 📚 Documentation

### 🌍 **For Spanish Speakers & Beginners**
- **[Complete Spanish Guide](docs/SPANISH_GUIDE.md)** - Comprehensive guide in Spanish for users with basic technical level
- **Perfect for**: Newcomers to automation testing, Spanish-speaking developers
- **Content**: Basic concepts, practical examples, troubleshooting, step-by-step tutorials

### 🇺🇸 **For English Speakers & Advanced Users**
- **This README** - Complete technical documentation and API reference
- **Perfect for**: Experienced developers, technical teams, enterprise users
- **Content**: Technical specifications, advanced features, best practices

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd AutomationFramework

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the root directory:

```env
# Test Environment
TEST_ENV=staging
BASE_URL=https://cli.github.com

# Browser Configuration
BROWSER=chrome
HEADLESS=true
IMPLICIT_WAIT=10
EXPLICIT_WAIT=20

# Test Configuration
SCREENSHOT_ON_FAILURE=true
RETRY_COUNT=3
RETRY_DELAY=2
```

### 3. Run Tests

```bash
# Run all tests
pytest

# Run tests with specific browser
pytest --browser=firefox

# Run tests in headless mode
pytest --headless

# Run tests in parallel
pytest -n auto

# Run specific test file
pytest tests/test_github_cli.py

# Run tests with verbose output
pytest -v

# Generate HTML report
pytest --html=reports/report.html
```

## 🧪 Writing Tests

### Basic Test Structure

```python
import pytest
from pages.github_cli_page import GitHubCLIPage
from utils.logger import logger

class TestGitHubCLI:
    """Test suite for GitHub CLI functionality"""
    
    @pytest.fixture(autouse=True)
    def setup_test(self, driver):
        """Setup test environment"""
        self.github_page = GitHubCLIPage(driver)
    
    def test_page_loads_successfully(self):
        """Verify page loads with all critical elements"""
        logger.info("Testing page load functionality")
        
        # Navigate to page
        self.github_page.navigate_to_page()
        
        # Verify page is loaded
        assert self.github_page.is_page_loaded()
        
        logger.info("✅ Page loaded successfully")
```

### Using Test Data

```python
from utils.test_data_loader import test_data

def test_with_data():
    """Test using centralized test data"""
    # Get user data
    user = test_data.get_user_data("valid_user")
    
    # Get expected text
    expected_header = test_data.get_assertion_data("expected_texts", "main_header")
    
    # Use in assertions
    assert expected_header in actual_header
```

## ⚙️ Configuration

### Browser Options

```python
# Chrome-specific options
chrome_options = {
    "headless": True,
    "no_sandbox": True,
    "disable_dev_shm_usage": True,
    "disable_gpu": True,
    "window_size": "1920,1080"
}

# Firefox-specific options
firefox_options = {
    "headless": True,
    "window_size": "1920,1080"
}
```

### Timeout Configuration

```python
# Page load timeout
EXPLICIT_WAIT = 20

# Element wait timeout
IMPLICIT_WAIT = 10

# Retry configuration
RETRY_COUNT = 3
RETRY_DELAY = 2
```

## 📊 Reporting

### HTML Reports

```bash
# Generate HTML report
pytest --html=reports/report.html --self-contained-html

# Generate HTML report with metadata
pytest --html=reports/report.html --metadata Project "Automation Framework"
```

### Allure Reports

```bash
# Install Allure
pip install allure-pytest

# Run tests with Allure
pytest --alluredir=reports/allure-results

# Generate Allure report
allure serve reports/allure-results
```

## 🔧 Advanced Features

### Retry Mechanisms

```python
from utils.retry_mechanism import retry_on_exception

@retry_on_exception(max_attempts=3, delay=1.0)
def flaky_operation():
    """Operation that might fail occasionally"""
    return perform_operation()
```

### Screenshot Capture

```python
from utils.screenshot_capture import ScreenshotCapture

# Capture screenshot on failure
screenshot = ScreenshotCapture(driver)
screenshot.capture_on_failure("test_name", "error_message")

# Capture screenshot before action
screenshot.capture_before_action("click_button")
```

### Custom Logging

```python
from utils.logger import logger

# Different log levels
logger.info("Test started")
logger.debug("Element found")
logger.warning("Retry attempt")
logger.error("Test failed")
```

## 🐳 Docker Support

### Build and Run

```bash
# Build Docker image
docker build -t automation-framework .

# Run tests in Docker
docker run -v $(pwd)/reports:/app/reports automation-framework

# Run with specific browser
docker run -e BROWSER=firefox automation-framework
```

## 📈 Performance Optimization

### Browser Optimizations

- Disable images and JavaScript for faster loading
- Optimized window sizes
- Headless mode support
- Custom user agents

### Test Execution

- Parallel test execution
- Optimized wait strategies
- Efficient element location
- Resource cleanup

## 🧹 Best Practices

### Code Organization

1. **Page Objects**: Keep locators centralized and methods focused
2. **Test Data**: Use external data files for maintainability
3. **Logging**: Log all important actions and decisions
4. **Error Handling**: Implement proper exception handling
5. **Cleanup**: Always clean up resources in fixtures

### Test Design

1. **Single Responsibility**: Each test should verify one thing
2. **Descriptive Names**: Use clear, descriptive test names
3. **Setup/Teardown**: Use fixtures for common setup
4. **Assertions**: Use meaningful assertion messages
5. **Data-Driven**: Use parametrized tests for similar scenarios

## 🔍 Troubleshooting

### Common Issues

1. **Element Not Found**: Check locators and wait times
2. **Browser Crashes**: Verify driver compatibility
3. **Slow Execution**: Enable headless mode and disable images
4. **Screenshot Failures**: Check directory permissions

### Debug Mode

```bash
# Run with debug logging
pytest --log-cli-level=DEBUG

# Run single test with verbose output
pytest -v -s tests/test_github_cli.py::TestGitHubCLI::test_page_loads
```

## 📚 API Reference

### BasePage Methods

- `navigate_to_page()`: Navigate to page URL
- `find_element(by, value)`: Find element with retry
- `click_element(by, value)`: Click element safely
- `input_text(by, value, text)`: Input text with validation
- `wait_for_element_visible(by, value)`: Wait for element visibility

### TestDataLoader Methods

- `get_user_data(user_type)`: Get user information
- `get_url(url_key)`: Get URL by key
- `get_assertion_data(type, key)`: Get assertion data
- `get_performance_data(metric)`: Get performance thresholds

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:

- **📚 Check Documentation First**:
  - [Spanish Guide for Beginners](docs/SPANISH_GUIDE.md) - Complete guide in Spanish
  - [Documentation Index](docs/README.md) - All available guides
- **🐛 Report Issues**: Create an issue in the repository
- **🔍 Troubleshooting**: Review the troubleshooting section below
- **📞 Contact**: Contact the development team

### 🌍 **Language Support**
- **Español**: [Guía Completa para Principiantes](docs/SPANISH_GUIDE.md)
- **English**: This README and technical documentation

---

**Built with ❤️ for Quality Assurance Teams**
