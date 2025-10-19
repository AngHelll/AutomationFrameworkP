# Best Practices Guide for AI Assistant

## Code Organization

### 1. Page Objects

✅ **DO:**
```python
class LoginPage(BasePage):
    """Login page object with clear responsibilities"""
    
    # Centralized locators
    LOCATORS = {
        'username_field': (By.ID, "username"),
        'password_field': (By.ID, "password"),
        'login_button': (By.XPATH, "//button[@type='submit']"),
        'error_message': (By.CLASS_NAME, "error"),
    }
    
    def login(self, username: str, password: str) -> bool:
        """Perform login action - single responsibility"""
        self.input_text(*self.LOCATORS['username_field'], username)
        self.input_text(*self.LOCATORS['password_field'], password)
        self.click_element(*self.LOCATORS['login_button'])
        return self.is_login_successful()
```

❌ **DON'T:**
```python
class LoginPage(BasePage):
    def login(self, username, password):
        # Hardcoded locators - BAD!
        driver.find_element(By.ID, "user").send_keys(username)
        # No error handling
        # No return value
        # No logging
```

---

### 2. Test Structure

✅ **DO:**
```python
class TestLogin:
    """Test suite with clear setup and organization"""
    
    @pytest.fixture(autouse=True)
    def setup_test(self, driver):
        """Setup runs before each test"""
        self.login_page = LoginPage(driver)
        self.driver = driver
    
    def test_successful_login_with_valid_credentials(self):
        """Descriptive test name - states what and why"""
        # Arrange
        username = test_data.get_user_data("valid_user")["username"]
        password = test_data.get_user_data("valid_user")["password"]
        
        # Act
        self.login_page.navigate_to_page()
        success = self.login_page.login(username, password)
        
        # Assert
        assert success, "Login should succeed with valid credentials"
        logger.info("✅ Login successful")
```

❌ **DON'T:**
```python
def test_1(driver):  # Unclear name
    # No setup
    # Mixed concerns
    driver.get("url")
    driver.find_element(By.ID, "user").send_keys("admin")
    # Magic strings
    # No clear AAA pattern
```

---

## Naming Conventions

### Files and Folders
```
✅ test_login.py          # Test files: test_*.py
✅ login_page.py          # Page objects: *_page.py
✅ test_data_loader.py    # Utilities: descriptive_name.py
✅ __init__.py            # Package markers
```

### Classes
```python
✅ class LoginPage:          # PascalCase for classes
✅ class TestLogin:          # Test classes: Test*
✅ class DataLoader:         # Descriptive names
```

### Methods
```python
✅ def test_successful_login():           # snake_case, descriptive
✅ def is_element_visible():              # Boolean methods: is_*, has_*
✅ def get_user_credentials():            # Getter methods: get_*
✅ def navigate_to_dashboard():           # Action methods: verb_noun
```

### Variables
```python
✅ username_field = (By.ID, "username")   # snake_case, descriptive
✅ MAX_RETRY_COUNT = 3                    # UPPER_CASE for constants
✅ is_logged_in = False                   # Boolean variables: is_*, has_*
```

---

## Locator Strategies

### Priority Order (Best to Worst)

1. **ID** - Most stable
```python
✅ (By.ID, "login-button")
```

2. **NAME** - Good for forms
```python
✅ (By.NAME, "username")
```

3. **CLASS_NAME** - Use with caution
```python
⚠️ (By.CLASS_NAME, "btn-primary")  # Can change with CSS
```

4. **CSS_SELECTOR** - Flexible
```python
✅ (By.CSS_SELECTOR, "button[type='submit']")
```

5. **XPATH** - Last resort
```python
⚠️ (By.XPATH, "//button[@class='btn']")  # Fragile
❌ (By.XPATH, "/html/body/div[1]/div[2]/button")  # Very fragile!
```

### Locator Best Practices

✅ **DO:**
```python
# Use data-testid for test stability
LOCATORS = {
    'submit_btn': (By.CSS_SELECTOR, "[data-testid='submit-button']"),
    'user_field': (By.ID, "username"),
}
```

❌ **DON'T:**
```python
# Avoid positional selectors
('xpath', "//div[1]/div[2]/button[3]")  # Breaks easily!
```

---

## Wait Strategies

### Explicit Waits (Recommended)

✅ **DO:**
```python
# Wait for specific condition
self.wait_for_element_visible(By.ID, "result")
self.wait_for_element_clickable(By.ID, "submit")

# Custom wait
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "element"))
)
```

❌ **DON'T:**
```python
# Hardcoded sleeps - BAD!
time.sleep(5)  # What are we waiting for?
```

### When to Use Each Wait

| Wait Type | Use Case | Example |
|-----------|----------|---------|
| `presence_of_element_located` | Element exists in DOM | Dynamic content |
| `visibility_of_element_located` | Element is visible | Hidden elements |
| `element_to_be_clickable` | Ready for interaction | Buttons, links |
| `text_to_be_present` | Text appears | Validation messages |

---

## Error Handling

✅ **DO:**
```python
def click_element(self, by: By, value: str) -> None:
    """Click element with proper error handling"""
    try:
        element = self.wait_for_element_clickable(by, value)
        element.click()
        logger.log_element_action("Clicked", f"{by}={value}")
    except TimeoutException:
        logger.error(f"Element not clickable: {by}={value}")
        self.screenshot.capture_on_failure("click_timeout", f"{by}={value}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error clicking {by}={value}: {str(e)}")
        raise
```

❌ **DON'T:**
```python
def click(self, locator):
    try:
        driver.find_element(locator).click()
    except:  # Catching all exceptions - BAD!
        pass  # Silently failing - WORSE!
```

---

## Logging

✅ **DO:**
```python
# Log at appropriate levels
logger.info("✅ Test started: test_login")
logger.debug(f"Attempting login with user: {username}")
logger.warning("⚠️ Retry attempt 2 of 3")
logger.error("❌ Login failed: Invalid credentials")

# Log with context
logger.log_element_action("Clicked", "login_button")
logger.log_page_navigation("https://example.com/login")
```

❌ **DON'T:**
```python
# No logging
def login(self, user, pass):
    # What's happening? We don't know!
    element.click()

# Or excessive logging
logger.debug("Step 1")
logger.debug("Step 2")  # Too verbose!
```

---

## Test Data Management

✅ **DO:**
```python
# Centralized test data
from utils.test_data_loader import test_data

user = test_data.get_user_data("valid_user")
url = test_data.get_url("login")
expected_text = test_data.get_assertion_data("expected_texts", "welcome")
```

❌ **DON'T:**
```python
# Hardcoded data in tests
username = "admin123"  # Magic strings
password = "Pass@123"  # Security risk!
url = "https://prod.example.com"  # Environment-specific
```

---

## Assertions

✅ **DO:**
```python
# Descriptive assertion messages
assert page.is_logged_in(), "User should be logged in after successful login"
assert "Welcome" in page.get_header_text(), f"Expected 'Welcome' in header, got: {page.get_header_text()}"

# Multiple assertions for clarity
assert page.is_element_visible(*LOCATORS['dashboard'])
assert page.get_username() == expected_username
assert page.has_admin_privileges()
```

❌ **DON'T:**
```python
# No assertion message
assert page.is_logged_in()  # Why did it fail?

# Too many assertions in one line
assert page.check1() and page.check2() and page.check3()  # Which one failed?
```

---

## Configuration

✅ **DO:**
```python
# Use environment variables
BROWSER = os.getenv("BROWSER", "chrome")
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"

# Centralize configuration
class TestSettings:
    BROWSER = os.getenv("BROWSER", "chrome")
    TIMEOUT = int(os.getenv("TIMEOUT", "10"))
```

❌ **DON'T:**
```python
# Hardcoded configuration
browser = "chrome"  # Can't change without code modification
wait_time = 10      # Not configurable
```

---

## Performance Best Practices

### 1. Parallel Execution
```bash
✅ pytest -n auto          # Use all CPU cores
✅ pytest -n 4             # Use 4 workers
```

### 2. Selective Test Execution
```bash
✅ pytest tests/test_login.py              # Run specific file
✅ pytest -k "login"                       # Run tests matching pattern
✅ pytest -m "smoke"                       # Run marked tests
```

### 3. Optimize Waits
```python
✅ Use explicit waits (faster, more reliable)
❌ Avoid implicit waits globally
❌ Never use time.sleep()
```

### 4. Reuse Browser Sessions
```python
✅ @pytest.fixture(scope="session")  # For compatible tests
⚠️ @pytest.fixture(scope="function") # For isolated tests
```

---

## Documentation

✅ **DO:**
```python
def login(self, username: str, password: str) -> bool:
    """
    Perform login with provided credentials.
    
    Args:
        username: User's login name
        password: User's password
    
    Returns:
        bool: True if login successful, False otherwise
    
    Example:
        >>> page.login("admin", "password123")
        True
    """
```

❌ **DON'T:**
```python
def login(self, u, p):  # No docstring, unclear parameters
    pass
```

---

## Git Practices

✅ **DO:**
```bash
# Descriptive commit messages
git commit -m "feat: Add login page object with retry mechanism"
git commit -m "fix: Resolve timeout issue in dashboard tests"
git commit -m "docs: Update API documentation for BasePage"

# Use branches
git checkout -b feature/add-api-tests
git checkout -b fix/login-timeout
```

❌ **DON'T:**
```bash
git commit -m "update"        # What was updated?
git commit -m "fix"           # What was fixed?
git commit -m "changes"       # What changed?
```

---

## Security Best Practices

✅ **DO:**
```python
# Use environment variables for sensitive data
password = os.getenv("TEST_PASSWORD")
api_key = os.getenv("API_KEY")

# Add .env to .gitignore
# Use .env.example for reference
```

❌ **DON'T:**
```python
# Hardcoded credentials
password = "SuperSecret123"  # Never do this!
api_key = "sk-1234567890"    # Security risk!
```

---

## Code Review Checklist

Before submitting code, check:

- [ ] Follows naming conventions
- [ ] Has proper error handling
- [ ] Includes logging
- [ ] Has docstrings
- [ ] Uses type hints
- [ ] No hardcoded values
- [ ] Tests pass locally
- [ ] No sensitive data exposed
- [ ] Code is DRY (Don't Repeat Yourself)
- [ ] Follows PEP 8 style guide

---

## Common Anti-Patterns to Avoid

❌ **1. God Objects**
```python
# Don't create classes that do everything
class SuperPage(BasePage):
    def login(self): pass
    def search(self): pass
    def checkout(self): pass
    def admin_tasks(self): pass  # Too many responsibilities!
```

❌ **2. Copy-Paste Programming**
```python
# Don't duplicate code
def test_1(): page.login("user1", "pass1")
def test_2(): page.login("user2", "pass2")  # Use fixtures or parametrize!
```

❌ **3. Magic Numbers/Strings**
```python
# Don't use unexplained values
time.sleep(5)  # Why 5? Use named constant: LOAD_WAIT_TIME = 5
assert text == "Success"  # Use: EXPECTED_SUCCESS_MESSAGE
```

❌ **4. Testing Implementation Details**
```python
# Test behavior, not implementation
assert element.get_attribute("class") == "active"  # Fragile!
# Better: assert page.is_active()  # Test behavior
```

---

## Performance Anti-Patterns

❌ **Avoid:**
```python
# Multiple page loads in one test
driver.get("page1")
driver.get("page2")
driver.get("page3")  # Slow! Split into separate tests

# Unnecessary waits
time.sleep(10)  # Always bad!

# Not using parallel execution
pytest  # Use: pytest -n auto
```

---

## Summary: The Golden Rules

1. **DRY** - Don't Repeat Yourself
2. **KISS** - Keep It Simple, Stupid
3. **YAGNI** - You Aren't Gonna Need It
4. **Single Responsibility** - One class/method, one job
5. **Explicit over Implicit** - Be clear about intentions
6. **Fail Fast** - Catch errors early
7. **Test Behavior** - Not implementation details
8. **Document Why** - Not just what
9. **Security First** - Never commit secrets
10. **Performance Matters** - Optimize when necessary

---

Following these practices will result in:
✅ Maintainable code
✅ Reliable tests
✅ Fast execution
✅ Easy debugging
✅ Happy team members!

