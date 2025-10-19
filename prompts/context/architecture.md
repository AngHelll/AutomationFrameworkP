# Framework Architecture - Deep Dive for AI

## Architectural Patterns

### 1. Page Object Model (POM)

**Pattern:** Structural Design Pattern  
**Purpose:** Separate test logic from UI structure  
**Benefits:** Maintainability, reusability, readability

#### Implementation

```
┌─────────────────┐
│   BasePage      │ (Abstract)
│   - driver      │
│   - wait        │
│   - screenshot  │
│   - retry       │
└────────┬────────┘
         │ inherits
         ├─────────────┬──────────────┬─────────────┐
         │             │              │             │
┌────────▼───────┐ ┌──▼──────────┐ ┌─▼───────────┐ ┌─▼────────────┐
│ GitHubCLIPage  │ │ LoginPage   │ │DashboardPage│ │ YourNewPage  │
│                │ │             │ │             │ │              │
│ - LOCATORS     │ │ - LOCATORS  │ │ - LOCATORS  │ │ - LOCATORS   │
│ - methods()    │ │ - methods() │ │ - methods() │ │ - methods()  │
└────────────────┘ └─────────────┘ └─────────────┘ └──────────────┘
```

**Key Responsibilities:**
- **BasePage**: Common operations (find, click, wait, screenshot)
- **Concrete Pages**: Page-specific locators and business logic

---

### 2. Test Pyramid

```
           ┌─────────┐
          ╱  E2E (4)  ╲      ← Comprehensive UI tests
         ╱─────────────╲
        ╱ Integration   ╲    ← Page interactions
       ╱    (8 tests)    ╲
      ╱───────────────────╲
     ╱     Unit Tests      ╲  ← Individual components
    ╱      (Future)         ╲
   ╱─────────────────────────╲
```

**Current Focus:** E2E and Integration tests  
**Future:** Add unit tests for utilities

---

### 3. Dependency Injection

**Pattern:** Constructor Injection  
**Implementation:** Pytest Fixtures

```python
@pytest.fixture(scope="function")
def driver(request):
    """Provides WebDriver to tests"""
    driver = BrowserManager.get_driver()
    yield driver
    driver.quit()

# Tests receive driver automatically
def test_feature(driver):
    page = MyPage(driver)
    page.navigate_to_page()
```

---

### 4. Factory Pattern

**Location:** `config/browser_setup.py`  
**Purpose:** Create browser instances

```python
class BrowserManager:
    @staticmethod
    def get_driver(browser: str):
        if browser == "chrome":
            return _setup_chrome_driver()
        elif browser == "firefox":
            return _setup_firefox_driver()
        elif browser == "edge":
            return _setup_edge_driver()
```

---

### 5. Decorator Pattern

**Location:** `utils/retry_mechanism.py`  
**Purpose:** Add retry behavior

```python
@retry_on_exception(max_attempts=3, delay=1.0)
def find_element(self, by, value):
    # Automatically retries on failure
    return self.driver.find_element(by, value)
```

---

### 6. Singleton Pattern

**Location:** `utils/logger.py`  
**Purpose:** Single logger instance

```python
class TestLogger:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

---

## Component Architecture

### Configuration Layer

```
┌──────────────────────────────────────┐
│         Configuration Layer          │
├──────────────────────────────────────┤
│                                      │
│  ┌──────────────┐  ┌──────────────┐ │
│  │  settings.py │  │browser_setup │ │
│  │              │  │    .py       │ │
│  │ - ENV vars   │  │ - Driver     │ │
│  │ - Timeouts   │  │   init       │ │
│  │ - URLs       │  │ - Options    │ │
│  │ - Flags      │  │ - Factory    │ │
│  └──────────────┘  └──────────────┘ │
│                                      │
│  ┌──────────────────────────────┐   │
│  │       .env / .env.example    │   │
│  │  - User configuration        │   │
│  └──────────────────────────────┘   │
└──────────────────────────────────────┘
```

---

### Page Object Layer

```
┌──────────────────────────────────────┐
│         Page Object Layer            │
├──────────────────────────────────────┤
│                                      │
│  ┌──────────────────────────────┐   │
│  │       BasePage (ABC)         │   │
│  │  - driver: WebDriver         │   │
│  │  - wait: WebDriverWait       │   │
│  │  - retry: ElementRetry       │   │
│  │  - screenshot: ScreenCapture │   │
│  │                              │   │
│  │  + find_element()            │   │
│  │  + click_element()           │   │
│  │  + input_text()              │   │
│  │  + wait_for_element()        │   │
│  │  + navigate_to_page()        │   │
│  │  + is_page_loaded() [ABC]    │   │
│  └──────────────────────────────┘   │
│              ▲                       │
│              │ inheritance           │
│  ┌───────────┴──────────┬───────┐   │
│  │                      │       │   │
│  │  Concrete Pages:     │       │   │
│  │  - GitHubCLIPage     │       │   │
│  │  - LoginPage         │       │   │
│  │  - DashboardPage     │       │   │
│  └──────────────────────┴───────┘   │
└──────────────────────────────────────┘
```

---

### Test Layer

```
┌──────────────────────────────────────┐
│            Test Layer                │
├──────────────────────────────────────┤
│                                      │
│  ┌──────────────────────────────┐   │
│  │     conftest.py              │   │
│  │  - Fixtures (driver, etc)    │   │
│  │  - Hooks (setup/teardown)    │   │
│  │  - Metadata configuration    │   │
│  └──────────────────────────────┘   │
│               │                      │
│               │ provides fixtures    │
│               ▼                      │
│  ┌──────────────────────────────┐   │
│  │      Test Classes            │   │
│  │  - TestGitHubCLI             │   │
│  │  - TestLogin                 │   │
│  │  - TestDashboard             │   │
│  │                              │   │
│  │  Each test:                  │   │
│  │  1. Setup (fixture)          │   │
│  │  2. Execute (test method)    │   │
│  │  3. Assert (validation)      │   │
│  │  4. Teardown (cleanup)       │   │
│  └──────────────────────────────┘   │
└──────────────────────────────────────┘
```

---

### Utility Layer

```
┌──────────────────────────────────────┐
│           Utility Layer              │
├──────────────────────────────────────┤
│                                      │
│  ┌────────────┐  ┌─────────────┐    │
│  │   Logger   │  │   Retry     │    │
│  │            │  │  Mechanism  │    │
│  │ - Singleton│  │             │    │
│  │ - File log │  │ - Decorator │    │
│  │ - Console  │  │ - Backoff   │    │
│  └────────────┘  └─────────────┘    │
│                                      │
│  ┌────────────┐  ┌─────────────┐    │
│  │Screenshot  │  │Test Data    │    │
│  │ Capture    │  │  Loader     │    │
│  │            │  │             │    │
│  │ - On fail  │  │ - JSON      │    │
│  │ - Before/  │  │ - Users     │    │
│  │   After    │  │ - URLs      │    │
│  └────────────┘  └─────────────┘    │
└──────────────────────────────────────┘
```

---

## Data Flow

### Test Execution Flow

```
1. pytest startup
   │
   ├─→ Load pytest.ini
   ├─→ Discover tests
   ├─→ Load conftest.py
   │
2. For each test:
   │
   ├─→ Run setup (pytest_configure hook)
   ├─→ Create driver (fixture)
   ├─→ Initialize page object
   ├─→ Execute test method
   │   ├─→ Navigate to page
   │   ├─→ Interact with elements
   │   ├─→ Perform assertions
   │   └─→ Log actions
   │
   ├─→ Test result (pass/fail)
   │   │
   │   └─→ If fail:
   │       ├─→ Capture screenshot
   │       └─→ Log error details
   │
   ├─→ Run teardown
   ├─→ Close driver
   └─→ Generate report
```

---

### Element Interaction Flow

```
Test → Page Object → BasePage → Retry → WebDriver → Browser
                                   │
                                   └─→ Logger (log action)
                                   └─→ Screenshot (capture)
```

**Example:**
```python
# Test calls
page.click_element(By.ID, "button")
    ↓
# BasePage method
def click_element(self, by, value):
    ↓
# Wait for element
element = self.wait_for_element_clickable(by, value)
    ↓
# Capture before screenshot
self.screenshot.capture_before_action()
    ↓
# Click (with retry)
@retry_on_exception()
element.click()
    ↓
# Log action
logger.log_element_action("Clicked", f"{by}={value}")
    ↓
# Capture after screenshot
self.screenshot.capture_after_action()
```

---

## Configuration Hierarchy

```
┌───────────────────────────────────────┐
│    1. pytest.ini (pytest config)      │
└───────────────────────────────────────┘
                 │
                 ▼
┌───────────────────────────────────────┐
│    2. .env file (environment vars)    │
└───────────────────────────────────────┘
                 │
                 ▼
┌───────────────────────────────────────┐
│    3. settings.py (default values)    │
└───────────────────────────────────────┘
                 │
                 ▼
┌───────────────────────────────────────┐
│    4. Command line arguments          │
│       (override everything)           │
└───────────────────────────────────────┘
```

**Priority:** Command line > .env > settings.py > pytest.ini

---

## Error Handling Strategy

```
┌──────────────────┐
│  Action Attempt  │
└────────┬─────────┘
         │
         ▼
    ┌────────┐
    │Success?│───Yes───→ Continue
    └───┬────┘
        │ No
        ▼
┌──────────────────┐
│  Retry Mechanism │
│  (max 3 attempts)│
└────────┬─────────┘
         │
         ▼
    ┌────────┐
    │Success?│───Yes───→ Continue
    └───┬────┘
        │ No
        ▼
┌──────────────────┐
│ Capture Screen   │
│ Log Error        │
│ Fail Test        │
└──────────────────┘
```

---

## Parallel Execution Architecture

```
┌─────────────────────────────────────┐
│         Main Process                │
│       (pytest-xdist)                │
└───┬─────────┬─────────┬────────┬────┘
    │         │         │        │
    ▼         ▼         ▼        ▼
┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐
│Worker │ │Worker │ │Worker │ │Worker │
│  1    │ │  2    │ │  3    │ │  n    │
│       │ │       │ │       │ │       │
│Test A │ │Test B │ │Test C │ │Test n │
│Driver │ │Driver │ │Driver │ │Driver │
└───────┘ └───────┘ └───────┘ └───────┘
```

**Note:** Each worker has isolated:
- WebDriver instance
- Screenshot folder
- Log file
- Test results

---

## Extensibility Points

### 1. Add New Page Object
- Inherit from `BasePage`
- Define `LOCATORS` dictionary
- Implement `_get_page_url()`
- Implement `is_page_loaded()`
- Add page-specific methods

### 2. Add New Utility
- Create in `utils/` directory
- Follow existing patterns
- Add to `__init__.py` if needed
- Document usage

### 3. Add New Browser
- Update `browser_setup.py`
- Add to factory method
- Configure options
- Test compatibility

### 4. Add New Report Type
- Add pytest plugin to requirements
- Configure in pytest.ini
- Update conftest.py hooks

---

## Design Decisions

### Why Pytest over unittest?
- Better fixtures
- Powerful plugins
- Parallel execution
- Better reporting
- More Pythonic

### Why Page Object Model?
- Maintainability
- Reusability
- Separation of concerns
- Easy to scale

### Why Retry Mechanism?
- Handle flaky tests
- Network instability
- Timing issues
- Stale elements

### Why Centralized Logging?
- Debugging
- Auditing
- Performance tracking
- Issue diagnosis

---

This architecture supports:
✅ Scalability  
✅ Maintainability  
✅ Testability  
✅ Reusability  
✅ Flexibility

