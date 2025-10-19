# How to Add New Features - Step by Step Guide

## Adding a New Page Object

### Step 1: Create the Page Object File

```bash
# Create file in pages/ directory
touch pages/checkout_page.py
```

### Step 2: Define the Page Object Class

```python
# pages/checkout_page.py
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.settings import TestSettings
from utils.logger import logger

class CheckoutPage(BasePage):
    """Page object for checkout functionality"""
    
    # Step 3: Define locators
    LOCATORS = {
        'product_name': (By.CLASS_NAME, "product-name"),
        'quantity_input': (By.ID, "quantity"),
        'total_price': (By.ID, "total"),
        'checkout_button': (By.ID, "checkout-btn"),
        'success_message': (By.CLASS_NAME, "success"),
    }
    
    #Step 4: Implement required abstract methods
    def _get_page_url(self) -> str:
        """Return checkout page URL"""
        return f"{TestSettings.BASE_URL}/checkout"
    
    def is_page_loaded(self) -> bool:
        """Verify checkout page loaded"""
        return (
            self.is_element_visible(*self.LOCATORS['product_name']) and
            self.is_element_visible(*self.LOCATORS['checkout_button'])
        )
    
    # Step 5: Add page-specific methods
    def get_product_name(self) -> str:
        """Get product name from checkout"""
        return self.get_element_text(*self.LOCATORS['product_name'])
    
    def set_quantity(self, quantity: int) -> None:
        """Set product quantity"""
        self.input_text(*self.LOCATORS['quantity_input'], str(quantity))
        logger.info(f"Set quantity to: {quantity}")
    
    def click_checkout(self) -> None:
        """Click checkout button"""
        self.click_element(*self.LOCATORS['checkout_button'])
    
    def is_checkout_successful(self) -> bool:
        """Check if checkout succeeded"""
        return self.is_element_visible(*self.LOCATORS['success_message'], timeout=10)
```

---

## Adding New Tests

### Step 1: Create Test File

```bash
# Create file in tests/ directory
touch tests/test_checkout.py
```

### Step 2: Define Test Class

```python
# tests/test_checkout.py
import pytest
from pages.checkout_page import CheckoutPage
from utils.logger import logger
from utils.test_data_loader import test_data

class TestCheckout:
    """Test suite for checkout functionality"""
    
    @pytest.fixture(autouse=True)
    def setup_test(self, driver):
        """Setup before each test"""
        self.checkout_page = CheckoutPage(driver)
        self.driver = driver
    
    def test_successful_checkout_with_single_item(self):
        """Verify checkout works with one item"""
        logger.info("Testing single item checkout")
        
        # Arrange
        expected_product = "Test Product"
        quantity = 1
        
        # Act
        self.checkout_page.navigate_to_page()
        assert self.checkout_page.is_page_loaded()
        
        product_name = self.checkout_page.get_product_name()
        self.checkout_page.set_quantity(quantity)
        self.checkout_page.click_checkout()
        
        # Assert
        assert self.checkout_page.is_checkout_successful()
        assert product_name == expected_product
        logger.info("✅ Checkout successful")
    
    @pytest.mark.parametrize("quantity", [1, 2, 5, 10])
    def test_checkout_with_different_quantities(self, quantity):
        """Test checkout with various quantities"""
        self.checkout_page.navigate_to_page()
        self.checkout_page.set_quantity(quantity)
        self.checkout_page.click_checkout()
        assert self.checkout_page.is_checkout_successful()
```

---

## Adding New Utility Functions

### Step 1: Choose or Create Utility File

```python
# If adding to existing: utils/helpers.py
# If new category: utils/api_helpers.py
```

### Step 2: Implement Utility

```python
# utils/helpers.py
def generate_random_email() -> str:
    """Generate random email for testing"""
    import uuid
    return f"test_{uuid.uuid4().hex[:8]}@example.com"

def wait_for_file_download(download_dir: str, timeout: int = 30) -> str:
    """Wait for file to appear in download directory"""
    import time
    import os
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        files = os.listdir(download_dir)
        if files:
            return os.path.join(download_dir, files[0])
        time.sleep(0.5)
    raise TimeoutError(f"No file downloaded within {timeout}s")
```

---

## Adding Configuration Options

### Step 1: Add to settings.py

```python
# config/settings.py
class TestSettings:
    # Add new configuration
    API_BASE_URL = os.getenv("API_BASE_URL", "https://api.example.com")
    API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))
    ENABLE_API_TESTS = os.getenv("ENABLE_API_TESTS", "false").lower() == "true"
```

### Step 2: Add to .env.example

```env
# API Configuration
API_BASE_URL=https://api.example.com
API_TIMEOUT=30
ENABLE_API_TESTS=true
```

### Step 3: Document in README

Update README.md with new configuration options.

---

## Adding Test Data

### Step 1: Update test_data.json

```json
{
  "users": {
    "checkout_user": {
      "username": "checkout_test",
      "email": "checkout@example.com",
      "credit_card": "4111111111111111"
    }
  },
  "products": {
    "test_product": {
      "name": "Test Product",
      "price": 99.99,
      "sku": "TEST-001"
    }
  }
}
```

### Step 2: Access in Tests

```python
from utils.test_data_loader import test_data

user = test_data.get_user_data("checkout_user")
# Use user["username"], user["email"], etc.
```

---

## Adding New Browser Support

### Step 1: Update browser_setup.py

```python
# config/browser_setup.py
@staticmethod
def _setup_safari_driver() -> webdriver.Safari:
    """Setup Safari driver"""
    options = webdriver.SafariOptions()
    driver = webdriver.Safari(options=options)
    return driver

@staticmethod
def get_driver(browser: str = None):
    # Add to factory
    elif browser == "safari":
        driver = BrowserManager._setup_safari_driver()
```

### Step 2: Update settings.py

```python
# config/settings.py
"safari": {
    "headless": False,  # Safari doesn't support headless
    "window_size": "1920,1080"
}
```

---

## Adding Custom Pytest Markers

### Step 1: Add to pytest.ini

```ini
[pytest]
markers =
    smoke: Quick smoke tests
    regression: Full regression suite
    api: API tests
    slow: Tests that take longer
```

### Step 2: Use in Tests

```python
@pytest.mark.smoke
def test_critical_flow(self):
    pass

@pytest.mark.slow
def test_performance(self):
    pass
```

### Step 3: Run Marked Tests

```bash
pytest -m smoke    # Run only smoke tests
pytest -m "not slow"  # Skip slow tests
```

---

## Adding Reporting Enhancements

### Step 1: Install Reporter

```bash
pip install allure-pytest
```

### Step 2: Add to requirements.txt

```
allure-pytest==2.13.2
```

### Step 3: Configure in pytest.ini

```ini
[pytest]
addopts = --alluredir=reports/allure-results
```

### Step 4: Generate Reports

```bash
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

---

## Quick Reference Checklist

When adding a new feature:

### Page Object Checklist
- [ ] Create file in `pages/` directory
- [ ] Inherit from `BasePage`
- [ ] Define `LOCATORS` dictionary
- [ ] Implement `_get_page_url()`
- [ ] Implement `is_page_loaded()`
- [ ] Add page-specific methods
- [ ] Add docstrings
- [ ] Test manually

### Test Checklist
- [ ] Create file in `tests/` directory (prefix with `test_`)
- [ ] Create test class (prefix with `Test`)
- [ ] Add `setup_test` fixture
- [ ] Write test methods (prefix with `test_`)
- [ ] Use AAA pattern (Arrange, Act, Assert)
- [ ] Add descriptive assertions
- [ ] Add logging
- [ ] Run and verify

### Utility Checklist
- [ ] Add to appropriate file in `utils/`
- [ ] Add type hints
- [ ] Add docstring
- [ ] Add error handling
- [ ] Add logging if needed
- [ ] Write unit tests (future)

### Configuration Checklist
- [ ] Add to `settings.py`
- [ ] Add to `.env.example`
- [ ] Document in README
- [ ] Test with different values

---

## Common Patterns

### Pattern 1: Data-Driven Tests

```python
@pytest.mark.parametrize("username,password,expected", [
    ("valid_user", "valid_pass", True),
    ("invalid_user", "wrong_pass", False),
])
def test_login_scenarios(self, username, password, expected):
    result = self.login_page.login(username, password)
    assert result == expected
```

### Pattern 2: Test Fixtures

```python
@pytest.fixture(scope="function")
def logged_in_user(driver):
    """Fixture that provides a logged-in session"""
    page = LoginPage(driver)
    page.navigate_to_page()
    page.login("test_user", "password")
    yield page
    # Cleanup if needed
```

### Pattern 3: Custom Waits

```python
def wait_for_ajax_complete(self, timeout=10):
    """Wait for all AJAX requests to complete"""
    WebDriverWait(self.driver, timeout).until(
        lambda d: d.execute_script("return jQuery.active == 0")
    )
```

---

## Testing New Features

```bash
# Run only your new tests
pytest tests/test_checkout.py -v

# Run with verbose logging
pytest tests/test_checkout.py -v --log-cli-level=DEBUG

# Run without headless to see browser
HEADLESS=false pytest tests/test_checkout.py
```

---

## Committing New Features

```bash
# Add files
git add pages/checkout_page.py tests/test_checkout.py

# Commit with descriptive message
git commit -m "feat: Add checkout page object and tests

- Implemented CheckoutPage with product selection
- Added tests for single and multiple item checkout
- Includes parametrized tests for quantity variations
- All tests passing (5 new tests)"

# Push
git push origin main
```

---

Remember: 
- Start small, test often
- Follow existing patterns
- Document as you go
- Ask AI for help!

