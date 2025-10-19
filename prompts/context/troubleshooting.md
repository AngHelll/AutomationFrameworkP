# Troubleshooting Guide for AI Assistant

## Common Issues and Solutions

### 1. Element Not Found Errors

**Symptom:**
```
selenium.common.exceptions.NoSuchElementException: 
Message: no such element: Unable to locate element
```

**Possible Causes & Solutions:**

#### A. Element hasn't loaded yet
✅ **Solution:**
```python
# Add explicit wait
self.wait_for_element_visible(By.ID, "element-id", timeout=20)

# Or increase timeout in settings
EXPLICIT_WAIT=30  # in .env file
```

#### B. Wrong locator
✅ **Solution:**
```python
# Verify locator in browser dev tools (F12)
# Try alternative strategies:
(By.ID, "element-id")           # Best
(By.CSS_SELECTOR, "#element-id")   # Alternative
(By.XPATH, "//div[@id='element-id']")  # Last resort
```

#### C. Element in iframe
✅ **Solution:**
```python
# Switch to iframe first
driver.switch_to.frame("iframe-name")
element = driver.find_element(By.ID, "element")
driver.switch_to.default_content()  # Switch back
```

#### D. Element is dynamically generated
✅ **Solution:**
```python
# Wait for AJAX/JavaScript completion
WebDriverWait(driver, 10).until(
    lambda d: d.execute_script("return document.readyState") == "complete"
)
```

---

### 2. Stale Element Reference

**Symptom:**
```
selenium.common.exceptions.StaleElementReferenceException:
Message: stale element reference: element is not attached to the page document
```

**Cause:** Element was found but DOM changed before interaction

✅ **Solution:**
```python
# Option 1: Retry mechanism (already built-in)
@retry_on_exception(max_attempts=3)
def click_element(self, by, value):
    element = self.find_element(by, value)
    element.click()

# Option 2: Re-find element
def safe_click(self, by, value):
    for attempt in range(3):
        try:
            element = self.find_element(by, value)
            element.click()
            break
        except StaleElementReferenceException:
            if attempt == 2:
                raise
            time.sleep(1)
```

---

### 3. Timeout Exceptions

**Symptom:**
```
selenium.common.exceptions.TimeoutException:
Message: timeout: Timed out receiving message from renderer
```

**Possible Causes & Solutions:**

#### A. Page loads slowly
✅ **Solution:**
```python
# Increase timeout
driver.set_page_load_timeout(60)  # seconds

# Or in .env
EXPLICIT_WAIT=30
```

#### B. Element never appears
✅ **Solution:**
```python
# Check if element exists first
if self.is_element_present(By.ID, "element", timeout=5):
    # Proceed
else:
    logger.warning("Element not present, skipping")
```

#### C. Network issues
✅ **Solution:**
```python
# Add retry mechanism
@retry_on_exception(max_attempts=5, delay=2.0)
def navigate_with_retry(self, url):
    self.driver.get(url)
```

---

### 4. Element Click Intercepted

**Symptom:**
```
selenium.common.exceptions.ElementClickInterceptedException:
Message: element click intercepted
```

**Cause:** Another element is covering the target element

✅ **Solutions:**
```python
# Option 1: Scroll to element
self.scroll_to_element(By.ID, "button")
element.click()

# Option 2: JavaScript click
element = self.find_element(By.ID, "button")
self.driver.execute_script("arguments[0].click();", element)

# Option 3: Wait for overlay to disappear
WebDriverWait(driver, 10).until(
    EC.invisibility_of_element_located((By.CLASS_NAME, "loading-overlay"))
)
element.click()
```

---

### 5. WebDriver Binary Issues

**Symptom:**
```
WebDriverException: 'chromedriver' executable needs to be in PATH
```

✅ **Solution:**
```python
# Framework uses webdriver-manager (auto-downloads)
# If issues persist:

# Option 1: Update webdriver-manager
pip install --upgrade webdriver-manager

# Option 2: Clear cache
import os
cache_path = "~/.wdm"
os.system(f"rm -rf {cache_path}")  # Linux/Mac
os.system(f"rmdir /s {cache_path}")  # Windows

# Option 3: Manually specify driver path
from selenium.webdriver.chrome.service import Service
service = Service(executable_path="/path/to/chromedriver")
driver = webdriver.Chrome(service=service)
```

---

### 6. Tests Fail in Headless Mode

**Symptom:** Tests pass with GUI but fail in headless mode

✅ **Solutions:**
```python
# Option 1: Enable JavaScript (if disabled)
ENABLE_JAVASCRIPT=true  # in .env

# Option 2: Increase window size
options.add_argument("--window-size=1920,1080")

# Option 3: Disable GPU (headless issues)
options.add_argument("--disable-gpu")

# Option 4: Run with visible browser first
HEADLESS=false pytest tests/test_name.py
```

---

### 7. Parallel Execution Failures

**Symptom:** Tests pass individually but fail when run in parallel

**Possible Causes & Solutions:**

#### A. Shared state/resources
✅ **Solution:**
```python
# Use function-scoped fixtures
@pytest.fixture(scope="function")  # Not "session"
def driver(request):
    driver = BrowserManager.get_driver()
    yield driver
    driver.quit()
```

#### B. Race conditions
✅ **Solution:**
```python
# Add unique identifiers
test_id = str(uuid.uuid4())
screenshot_name = f"test_{test_id}.png"
```

#### C. Port conflicts
✅ **Solution:**
```bash
# Limit workers
pytest -n 4  # Instead of -n auto
```

---

### 8. Import Errors

**Symptom:**
```
ModuleNotFoundError: No module named 'selenium'
```

✅ **Solutions:**
```bash
# Option 1: Install dependencies
pip install -r requirements.txt

# Option 2: Check virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt

# Option 3: Verify Python version
python --version  # Should be 3.8+
```

---

### 9. Configuration Not Loading

**Symptom:** Settings from .env not being applied

✅ **Solutions:**
```bash
# Option 1: Verify .env location
ls -la .env  # Should be in project root

# Option 2: Check .env format
# No spaces around =
BROWSER=chrome  # Correct
BROWSER = chrome  # Wrong!

# Option 3: Reload environment
# Restart terminal or:
source .env  # Linux/Mac
```

---

### 10. Screenshot Failures

**Symptom:**
```
PermissionError: [Errno 13] Permission denied: 'screenshots/test.png'
```

✅ **Solutions:**
```bash
# Option 1: Create directory
mkdir screenshots
chmod 755 screenshots  # Linux/Mac

# Option 2: Check permissions
ls -l screenshots/

# Option 3: Clear old screenshots
rm screenshots/*.png  # Linux/Mac
del screenshots\*.png  # Windows
```

---

## Debugging Strategies

### 1. Enable Debug Logging

```bash
# Run with debug output
pytest --log-cli-level=DEBUG tests/test_name.py

# Or in code
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 2. Run Single Test

```bash
# Isolate the failing test
pytest tests/test_file.py::TestClass::test_method -v

# With debug and no capture
pytest tests/test_file.py::test_name -v -s --log-cli-level=DEBUG
```

### 3. Add Breakpoints

```python
# In test or page object
def test_something(self):
    self.page.navigate_to_page()
    import pdb; pdb.set_trace()  # Debugger stops here
    self.page.click_button()
```

### 4. Increase Visibility

```bash
# Run without headless to see what's happening
HEADLESS=false pytest tests/test_name.py

# Slow down execution
import time
time.sleep(2)  # Temporarily, for debugging
```

### 5. Check Browser Console

```python
# Get browser console logs
logs = driver.get_log('browser')
for log in logs:
    print(log)
```

### 6. Verify Page Source

```python
# Check if element exists in page source
page_source = driver.page_source
if "expected-text" in page_source:
    print("Text found in page")
else:
    print("Text NOT found")
    print(page_source[:500])  # Print first 500 chars
```

---

## Performance Issues

### Slow Test Execution

**Symptoms:** Tests take too long to run

✅ **Solutions:**
```bash
# 1. Use parallel execution
pytest -n auto

# 2. Disable images (if not needed)
ENABLE_IMAGES=false

# 3. Use headless mode
HEADLESS=true

# 4. Reduce retries (if stable)
RETRY_COUNT=2

# 5. Run only changed tests
pytest --lf  # Last failed
pytest --ff  # Failed first
```

### Memory Issues

**Symptoms:** High memory usage, crashes

✅ **Solutions:**
```python
# 1. Ensure driver cleanup
@pytest.fixture(scope="function")
def driver(request):
    driver = BrowserManager.get_driver()
    yield driver
    driver.quit()  # Important!

# 2. Limit parallel workers
pytest -n 4  # Instead of auto

# 3. Clear cache
driver.delete_all_cookies()
```

---

## Framework-Specific Issues

### Issue: Tests collection warnings

**Problem:** `TestDataLoader` class detected as test

✅ **Solution:**
```python
# Rename class to avoid "Test" prefix
class DataLoader:  # Not TestDataLoader
    pass
```

### Issue: URL trailing slash mismatch

**Problem:** `https://example.com/` != `https://example.com`

✅ **Solution:**
```python
# Normalize URLs
current_url = driver.current_url.rstrip('/')
expected_url = expected.rstrip('/')
assert current_url == expected_url
```

### Issue: Locator not found after page update

**Problem:** Website changed, locators outdated

✅ **Solution:**
```python
# 1. Inspect current page (F12 in browser)
# 2. Update locators in page object
LOCATORS = {
    'button': (By.ID, "new-button-id"),  # Updated
}

# 3. Add fallback locators
def find_submit_button(self):
    try:
        return self.find_element(By.ID, "submit")
    except NoSuchElementException:
        return self.find_element(By.CSS_SELECTOR, "button[type='submit']")
```

---

## Getting Help

### 1. Check Documentation
- README.md
- GUIA_NOVATOS.md (Spanish)
- FIXES_APPLIED.md
- This troubleshooting guide

### 2. Check Logs
```bash
# Framework logs
cat logs/test_execution_*.log

# Pytest output
pytest -v --tb=long
```

### 3. Check Screenshots
```bash
ls screenshots/FAILURE_*.png
```

### 4. Use AI Assistant
```bash
# Ask about specific errors
"Why is my test failing with NoSuchElementException?"
"How do I fix stale element errors?"
"What's the best way to wait for dynamic content?"
```

---

## Quick Reference: Error Messages

| Error | Common Cause | Quick Fix |
|-------|--------------|-----------|
| `NoSuchElementException` | Element not loaded | Add explicit wait |
| `StaleElementReferenceException` | DOM changed | Use retry mechanism |
| `TimeoutException` | Slow page/network | Increase timeout |
| `ElementClickInterceptedException` | Element covered | Scroll or JS click |
| `WebDriverException` | Driver issue | Update webdriver-manager |
| `ModuleNotFoundError` | Missing dependency | `pip install -r requirements.txt` |
| `PermissionError` | File access | Check permissions |
| `ConnectionRefusedError` | Browser not starting | Check browser installation |

---

## Prevention Tips

1. ✅ Use explicit waits, not sleep()
2. ✅ Implement retry mechanisms
3. ✅ Use stable locators (ID > CSS > XPath)
4. ✅ Handle exceptions gracefully
5. ✅ Log everything
6. ✅ Capture screenshots on failure
7. ✅ Run tests in isolation
8. ✅ Keep dependencies updated
9. ✅ Use version control
10. ✅ Regular code reviews

---

Remember: Most issues are solved by:
1. Checking logs
2. Adding waits
3. Verifying locators
4. Running in non-headless mode
5. Reading error messages carefully

