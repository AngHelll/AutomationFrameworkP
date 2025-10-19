# Framework Technical Reference

**This document provides the complete technical reference for AI agents.**

---

## Framework Identity

- **Type:** Selenium-based test automation framework
- **Language:** Python 3.13+
- **Test Runners:** Pytest (technical tests) + Behave (BDD tests)
- **Architecture:** Page Object Model (POM)
- **Status:** Production-ready

---

## Technology Stack

### Core Dependencies
```
selenium==4.29.0          # Browser automation
pytest==8.3.4             # Technical test framework
pytest-xdist==3.6.1       # Parallel test execution
behave==1.2.6             # BDD test framework
python-dotenv==1.0.1      # Environment configuration
webdriver-manager==4.0.2  # Automatic driver management
```

### Supported Browsers
- Chrome (primary, recommended)
- Firefox (supported)
- Edge (supported)

### Supported Platforms
- Windows, Linux, macOS, Docker

---

## Project Structure

```
AutomationFramework/
├── config/                      # Configuration layer
│   ├── settings.py             # Framework settings (loads from .env)
│   └── browser_setup.py        # Browser initialization logic
│
├── pages/                      # Page Object Model
│   ├── base_page.py           # Abstract base class (all pages inherit)
│   └── *_page.py              # Concrete page objects
│
├── tests/                      # Pytest test suites
│   └── test_*.py              # Test files (Pytest discovers these)
│
├── features/                   # BDD test suites
│   ├── *.feature              # Gherkin scenarios
│   ├── steps/                 # Step definitions
│   └── environment.py         # Behave hooks
│
├── utils/                      # Utility modules
│   ├── logger.py              # Centralized logging
│   ├── retry_mechanism.py     # Retry logic for flaky operations
│   ├── screenshot_capture.py  # Screenshot utility
│   └── test_data_loader.py    # JSON test data loader
│
├── test_data/                  # Test data
│   └── test_data.json         # Centralized JSON test data
│
├── logs/                       # Execution logs (auto-generated)
├── screenshots/                # Screenshots (auto-generated)
├── reports/                    # Test reports (auto-generated)
│
├── conftest.py                 # Pytest fixtures and hooks
├── pytest.ini                  # Pytest configuration
├── .env                        # Environment config (not in Git)
├── .env.example                # Config template (in Git)
└── requirements.txt            # Python dependencies
```

---

## Configuration System

### Environment Variables (.env)

The framework uses `.env` file for all configuration. Create it by copying `.env.example`.

**Browser Configuration:**
```env
BROWSER=chrome                  # chrome|firefox|edge
HEADLESS=true                   # true|false
ENABLE_JAVASCRIPT=true          # true|false
ENABLE_IMAGES=true              # true|false
```

**Timeouts:**
```env
IMPLICIT_WAIT=10                # seconds
EXPLICIT_WAIT=20                # seconds
PAGE_LOAD_TIMEOUT=30            # seconds
```

**Test Settings:**
```env
SCREENSHOT_ON_FAILURE=true      # Capture screenshots on test failure
RETRY_COUNT=3                   # Number of retries for flaky operations
RETRY_DELAY=2                   # Seconds between retries
```

**Environment:**
```env
TEST_ENV=staging                # staging|production|development
BASE_URL=https://example.com    # Base URL for tests
```

### Access Configuration in Code

```python
from config.settings import TestSettings

browser = TestSettings.BROWSER
headless = TestSettings.HEADLESS
base_url = TestSettings.BASE_URL
```

---

## Page Object Model

### BasePage (Abstract)

All page objects inherit from `BasePage` located in `pages/base_page.py`.

**Required Methods to Implement:**
```python
def _get_page_url(self) -> str:
    """Return the page URL"""
    
def is_page_loaded(self) -> bool:
    """Verify page loaded successfully"""
```

**Available Methods:**
- `navigate_to_page()` - Navigate to page URL
- `click_element(by, locator)` - Click element with retry
- `input_text(by, locator, text)` - Input text with retry
- `get_element_text(by, locator)` - Get text with retry
- `is_element_visible(by, locator, timeout)` - Check visibility
- `is_element_present(by, locator)` - Check presence
- `wait_for_element(by, locator, timeout)` - Explicit wait
- `take_screenshot(name)` - Capture screenshot

### Creating Page Objects

**1. Create file in `pages/` directory:**
```python
# pages/checkout_page.py
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.settings import TestSettings

class CheckoutPage(BasePage):
    """Checkout page object"""
    
    # Define locators
    LOCATORS = {
        'product_name': (By.CLASS_NAME, "product-name"),
        'checkout_button': (By.ID, "checkout-btn"),
        'success_message': (By.CLASS_NAME, "success"),
    }
    
    # Implement required methods
    def _get_page_url(self) -> str:
        return f"{TestSettings.BASE_URL}/checkout"
    
    def is_page_loaded(self) -> bool:
        return self.is_element_visible(*self.LOCATORS['checkout_button'])
    
    # Add page-specific methods
    def click_checkout(self) -> None:
        """Click checkout button"""
        self.click_element(*self.LOCATORS['checkout_button'])
```

---

## Writing Tests

### Pytest Tests

**1. Create test file in `tests/` directory:**

File naming: `test_*.py` (Pytest discovers files starting with `test_`)

**2. Structure:**
```python
import pytest
from pages.checkout_page import CheckoutPage

class TestCheckout:
    """Checkout test suite"""
    
    @pytest.fixture(autouse=True)
    def setup_test(self, driver):
        """Setup runs before each test"""
        self.checkout_page = CheckoutPage(driver)
        self.driver = driver
    
    def test_successful_checkout(self):
        """Test checkout flow"""
        # Arrange
        self.checkout_page.navigate_to_page()
        assert self.checkout_page.is_page_loaded()
        
        # Act
        self.checkout_page.click_checkout()
        
        # Assert
        assert self.checkout_page.is_element_visible(
            *self.checkout_page.LOCATORS['success_message']
        )
```

**3. Run tests:**
```bash
pytest                                  # All tests
pytest tests/test_checkout.py          # Specific file
pytest -v                               # Verbose
pytest -n auto                          # Parallel
pytest -k "checkout"                    # Filter by name
```

### BDD Tests (Behave)

**1. Create feature file in `features/` directory:**

```gherkin
# features/checkout.feature
Feature: Checkout Process
  
  Scenario: Successful checkout
    Given I am on the checkout page
    When I click the checkout button
    Then I should see a success message
```

**2. Create step definitions in `features/steps/`:**

```python
# features/steps/checkout_steps.py
from behave import given, when, then
from pages.checkout_page import CheckoutPage

@given('I am on the checkout page')
def step_impl(context):
    context.checkout_page = CheckoutPage(context.driver)
    context.checkout_page.navigate_to_page()

@when('I click the checkout button')
def step_impl(context):
    context.checkout_page.click_checkout()

@then('I should see a success message')
def step_impl(context):
    assert context.checkout_page.is_element_visible(
        *context.checkout_page.LOCATORS['success_message']
    )
```

**3. Run BDD tests:**
```bash
behave                                  # All features
behave features/checkout.feature        # Specific feature
behave --tags=smoke                     # Tagged scenarios
behave -v                               # Verbose
```

---

## Utility Modules

### Logger

**Usage:**
```python
from utils.logger import logger

logger.info("Test started")
logger.debug("Debugging info")
logger.warning("Warning message")
logger.error("Error occurred")
```

**Output:** Logs to both console and `logs/test_execution_YYYYMMDD_HHMMSS.log`

### Retry Mechanism

**Decorator usage:**
```python
from utils.retry_mechanism import retry_on_exception

@retry_on_exception(max_attempts=3, delay=2)
def flaky_operation():
    # Operation that might fail
    pass
```

**The decorator automatically:**
- Retries on failure up to `max_attempts` times
- Waits `delay` seconds between retries
- Logs each attempt

### Screenshot Capture

**Usage:**
```python
from utils.screenshot_capture import ScreenshotCapture

screenshot = ScreenshotCapture(driver)
screenshot.capture_on_failure("test_name", "error_message")
screenshot.capture_before_action("action_name")
screenshot.capture_after_action("action_name")
```

**Screenshots save to:** `screenshots/` directory with timestamps

### Test Data Loader

**1. Define data in `test_data/test_data.json`:**
```json
{
  "users": {
    "valid_user": {
      "username": "test_user",
      "password": "test_pass"
    }
  }
}
```

**2. Access in tests:**
```python
from utils.test_data_loader import test_data

user = test_data.get_user_data("valid_user")
username = user["username"]
password = user["password"]
```

---

## Test Execution Commands

### Pytest (Technical Tests)
```bash
pytest                              # Run all Pytest tests
pytest -v                           # Verbose output
pytest -n auto                      # Parallel execution
pytest tests/test_checkout.py       # Specific file
pytest -k "test_checkout"           # Filter by name
pytest --browser=firefox            # Custom browser
pytest --headless                   # Headless mode
pytest --html=reports/report.html   # HTML report
```

### Behave (BDD Tests)
```bash
behave                              # Run all BDD tests
behave -v                           # Verbose output
behave --tags=smoke                 # Tagged scenarios
behave --tags="not slow"            # Exclude tags
behave features/checkout.feature    # Specific feature
behave --no-capture                 # Show print statements
```

---

## Adding New Features

### Add New Page Object

1. Create `pages/new_page.py`
2. Inherit from `BasePage`
3. Define `LOCATORS` dictionary
4. Implement `_get_page_url()`
5. Implement `is_page_loaded()`
6. Add page-specific methods

### Add New Pytest Test

1. Create `tests/test_new_feature.py`
2. Create test class (name starts with `Test`)
3. Add `setup_test` fixture
4. Write test methods (names start with `test_`)
5. Run: `pytest tests/test_new_feature.py`

### Add New BDD Feature

1. Create `features/new_feature.feature` (Gherkin)
2. Create `features/steps/new_feature_steps.py`
3. Implement step definitions using `@given`, `@when`, `@then`
4. Run: `behave features/new_feature.feature`

### Add Configuration Option

1. Add to `config/settings.py`:
   ```python
   NEW_OPTION = os.getenv("NEW_OPTION", "default")
   ```
2. Add to `.env.example`:
   ```env
   NEW_OPTION=value
   ```
3. Document in README

### Add Utility Function

1. Add to appropriate file in `utils/`
2. Add type hints
3. Add docstring
4. Import and use in tests

---

## Debugging

### Run Single Test
```bash
pytest tests/test_file.py::TestClass::test_method -v
```

### Disable Headless
```bash
HEADLESS=false pytest tests/test_file.py
```

### Enable Debug Logging
```bash
pytest tests/test_file.py --log-cli-level=DEBUG
```

### Inspect Screenshots
Check `screenshots/` directory for failure screenshots

### Check Logs
Check `logs/` directory for execution logs

---

## Common Patterns

### Data-Driven Tests (Pytest)
```python
@pytest.mark.parametrize("username,password", [
    ("user1", "pass1"),
    ("user2", "pass2"),
])
def test_login(self, username, password):
    self.login_page.login(username, password)
```

### Scenario Outline (Behave)
```gherkin
Scenario Outline: Login with different users
  When I login with "<username>" and "<password>"
  Then the result should be "<result>"
  
  Examples:
    | username | password | result  |
    | user1    | pass1    | success |
    | user2    | wrong    | fail    |
```

### Custom Fixtures (Pytest)
```python
@pytest.fixture
def logged_in_user(driver):
    """Provide logged-in session"""
    login_page = LoginPage(driver)
    login_page.login("user", "pass")
    yield login_page
```

### Background Steps (Behave)
```gherkin
Feature: Dashboard
  Background:
    Given I am logged in
  
  Scenario: View profile
    When I click profile
    Then I see my details
```

---

## Framework Principles

1. **Single Responsibility:** Each class/method has one purpose
2. **DRY:** Reuse code through inheritance and utilities
3. **Explicit Waits:** Use explicit waits, not sleep()
4. **Retry Logic:** Handle flaky tests automatically
5. **Logging:** Log all important actions
6. **Page Objects:** Never interact with WebDriver directly in tests
7. **Configuration:** Never hardcode values, use settings
8. **Clean Tests:** Arrange-Act-Assert pattern

---

## Key Commands Quick Reference

```bash
# Setup
pip install -r requirements.txt
cp .env.example .env

# Run Tests
pytest                          # Pytest tests
behave                          # BDD tests
pytest -n auto                  # Parallel
behave --tags=smoke            # Smoke tests

# Development
pytest -v --tb=short           # Detailed failures
behave --no-capture            # See print output
HEADLESS=false pytest          # Visual debugging
```

---

**This framework provides everything needed for production-grade test automation using both traditional Pytest and BDD approaches.**

