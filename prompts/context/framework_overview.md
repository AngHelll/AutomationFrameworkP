# Automation Framework - Complete Context for AI

## Framework Identity
**Name:** Enterprise Python Automation Framework  
**Version:** 2.0.0  
**Purpose:** Production-ready Selenium-based test automation framework  
**Language:** Python 3.13+  
**Test Runner:** Pytest  
**Author:** QA Team

---

## Core Philosophy

This framework follows these principles:
1. **Page Object Model (POM)**: Clean separation between test logic and page structure
2. **DRY (Don't Repeat Yourself)**: Reusable components and utilities
3. **Fail-Fast with Recovery**: Retry mechanisms for flaky tests
4. **Comprehensive Logging**: Track everything for debugging
5. **Configurability**: Environment-based configuration without code changes

---

## Technology Stack

### Core Dependencies
```python
selenium==4.29.0          # Browser automation
pytest==8.3.4             # Test framework
pytest-xdist==3.6.1       # Parallel execution
pytest-html==4.1.1        # HTML reporting
python-dotenv==1.0.1      # Environment configuration
webdriver-manager==4.0.2  # Automatic driver management
```

### Supported Browsers
- Chrome (recommended)
- Firefox
- Edge

### Supported Platforms
- Windows ✅
- Linux ✅
- macOS ✅
- Docker ✅

---

## Project Structure

```
AutomationFramework/
├── config/                      # Configuration layer
│   ├── __init__.py
│   ├── settings.py             # Environment settings
│   ├── browser_setup.py        # Browser initialization
│   └── env_template.txt        # Configuration template
│
├── pages/                      # Page Object Model
│   ├── __init__.py
│   ├── base_page.py           # Abstract base class
│   ├── github_cli_page.py     # Example page object
│   ├── login_page.py          # Login page object
│   └── dashboard_page.py      # Dashboard page object
│
├── tests/                      # Test suites
│   ├── __init__.py
│   ├── test_github_cli.py     # GitHub CLI tests
│   └── test_login.py          # Login tests
│
├── utils/                      # Utility modules
│   ├── __init__.py
│   ├── logger.py              # Logging utility
│   ├── retry_mechanism.py     # Retry decorators
│   ├── screenshot_capture.py  # Screenshot utility
│   ├── test_data_loader.py    # Test data management
│   └── helpers.py             # Helper functions
│
├── test_data/                  # Test data files
│   └── test_data.json         # Centralized test data
│
├── prompts/                    # AI context (new)
│   ├── context/               # Framework documentation
│   ├── examples/              # Few-shot examples
│   └── system/                # System prompts
│
├── logs/                       # Execution logs
├── screenshots/                # Test screenshots
├── reports/                    # Test reports
├── docs/                       # Documentation
│   ├── README.md
│   └── SPANISH_GUIDE.md
│
├── conftest.py                 # Pytest configuration
├── pytest.ini                  # Pytest settings
├── requirements.txt            # Dependencies
├── .env.example                # Example configuration
├── .gitignore                  # Git ignore rules
├── Dockerfile                  # Docker configuration
├── README.md                   # Main documentation
├── GUIA_NOVATOS.md            # Spanish beginner guide
└── FIXES_APPLIED.md           # Fix documentation
```

---

## Key Components

### 1. Configuration Layer (`config/`)

**settings.py**
- Loads environment variables
- Provides centralized configuration
- Manages browser options
- Handles timeouts and retries

**browser_setup.py**
- Initializes WebDriver
- Configures browser options
- Manages driver lifecycle
- Supports multiple browsers

### 2. Page Objects (`pages/`)

**BasePage** (Abstract)
- Common page operations
- Element finding with retry
- Wait strategies
- Screenshot capture
- Navigation helpers

**Concrete Pages**
- Inherit from BasePage
- Define page-specific locators
- Implement page-specific methods
- Validate page state

### 3. Test Layer (`tests/`)

- Uses Pytest framework
- Leverages fixtures
- Implements test classes
- Uses assertions
- Generates reports

### 4. Utilities (`utils/`)

**Logger**
- File and console output
- Different log levels
- Structured formatting
- Test lifecycle tracking

**Retry Mechanism**
- Decorator pattern
- Exponential backoff
- Configurable attempts
- Exception handling

**Screenshot Capture**
- On failure capture
- Before/after actions
- Element-specific screenshots
- Automatic naming

**Test Data Loader**
- JSON-based data
- Centralized management
- Type-safe access
- Environment-specific data

---

## Configuration

### Environment Variables (.env)

```env
# Browser Settings
BROWSER=chrome
HEADLESS=true
ENABLE_JAVASCRIPT=true
ENABLE_IMAGES=true

# Timeouts
IMPLICIT_WAIT=10
EXPLICIT_WAIT=20

# Test Settings
SCREENSHOT_ON_FAILURE=true
RETRY_COUNT=3
RETRY_DELAY=2

# Environment
TEST_ENV=staging
BASE_URL=https://cli.github.com
```

### Pytest Configuration (pytest.ini)

```ini
[pytest]
addopts = -n auto --html=reports/test_report.html --self-contained-html
```

---

## Test Execution

### Basic Commands

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_github_cli.py

# Run with verbose output
pytest -v

# Run in parallel
pytest -n auto

# Run specific test method
pytest tests/test_github_cli.py::TestGitHubCLI::test_page_loads

# Run with custom browser
pytest --browser=firefox

# Run in headless mode
pytest --headless
```

### Test Markers

```python
@pytest.mark.skip(reason="Feature not implemented")
@pytest.mark.parametrize("platform", ["windows", "mac"])
@pytest.mark.slow
```

---

## Current Test Statistics

- **Total Tests:** 16
- **Passing:** 14
- **Skipped:** 2
- **Pass Rate:** 87.5%
- **Execution Time:** ~50 seconds (parallel)

---

## Known Patterns

### Creating a New Page Object

```python
from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class NewPage(BasePage):
    LOCATORS = {
        'element': (By.ID, "element-id"),
    }
    
    def _get_page_url(self) -> str:
        return TestSettings.get_urls()["page_key"]
    
    def is_page_loaded(self) -> bool:
        return self.is_element_visible(*self.LOCATORS['element'])
```

### Creating a New Test

```python
import pytest
from pages.new_page import NewPage
from utils.logger import logger

class TestNewFeature:
    @pytest.fixture(autouse=True)
    def setup_test(self, driver):
        self.page = NewPage(driver)
    
    def test_feature(self):
        self.page.navigate_to_page()
        assert self.page.is_page_loaded()
```

---

## Common Issues & Solutions

### Issue: Element not found
**Solution:** Check locators, increase wait times, verify page loaded

### Issue: Stale element
**Solution:** Retry mechanism handles automatically

### Issue: Tests fail in headless
**Solution:** Check JavaScript/Images settings

### Issue: Slow execution
**Solution:** Use parallel execution (`-n auto`)

---

## Dependencies Management

```bash
# Install dependencies
pip install -r requirements.txt

# Update dependencies
pip install --upgrade -r requirements.txt

# Freeze current versions
pip freeze > requirements.txt
```

---

## Git Workflow

```bash
# Check status
git st  # Alias for status

# Stage changes
git add <files>

# Commit
git cm "message"  # Alias for commit -m

# Push
git push origin main
```

---

## Framework Strengths

1. ✅ **Production Ready**: Used in real projects
2. ✅ **Well Documented**: Multiple language support
3. ✅ **Highly Configurable**: Environment-based settings
4. ✅ **Robust**: Retry mechanisms and error handling
5. ✅ **Fast**: Parallel execution support
6. ✅ **Maintainable**: Clean architecture (POM)
7. ✅ **Observable**: Comprehensive logging
8. ✅ **Portable**: Docker support

---

## Version History

- **v2.0.0**: AI integration, improved configuration
- **v1.5.0**: Fixed all test issues, 100% pass rate
- **v1.0.0**: Initial enterprise framework

---

## Support Resources

- README.md - English documentation
- GUIA_NOVATOS.md - Spanish beginner guide  
- FIXES_APPLIED.md - Recent fixes documentation
- docs/SPANISH_GUIDE.md - Comprehensive Spanish guide

---

This context provides AI models with complete understanding of the framework architecture, patterns, and usage.

