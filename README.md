# Python Selenium Automation Framework

**Production-ready test automation framework using Selenium, Pytest, and Behave for BDD.**

---

## Features

- **Page Object Model (POM)** - Clean separation of test logic and page structure
- **Dual Test Approaches** - Pytest (technical) + Behave (BDD)
- **Multi-Browser Support** - Chrome, Firefox, Edge
- **Parallel Execution** - Run tests concurrently for faster feedback
- **Retry Mechanisms** - Handle flaky tests automatically
- **Screenshot Capture** - Auto-capture on failures
- **Comprehensive Logging** - Detailed execution logs
- **Environment Configuration** - Flexible `.env`-based setup
- **Docker Ready** - Containerized execution
- **AI-Powered** - Complete context for AI code generation

---

## Quick Start

### 1. Install Dependencies

```bash
git clone <repository-url>
cd AutomationFramework
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your settings
```

### 3. Run Tests

```bash
# Pytest (technical tests)
pytest                          # All tests
pytest -n auto                  # Parallel execution
pytest -v                       # Verbose output

# Behave (BDD tests)
behave                          # All BDD scenarios
behave --tags=smoke            # Smoke tests only
behave features/login.feature  # Specific feature
```

---

## Project Structure

```
AutomationFramework/
├── config/                 # Framework configuration
├── pages/                  # Page Object Model
├── tests/                  # Pytest test suites
├── features/               # BDD test suites (Behave)
├── utils/                  # Utilities (logger, retry, screenshots)
├── test_data/              # JSON test data
├── prompts/                # AI context files
└── docs/                   # Documentation
```

---

## Configuration

Edit `.env` file:

```env
# Browser
BROWSER=chrome              # chrome|firefox|edge
HEADLESS=true               # Run without GUI

# Timeouts
IMPLICIT_WAIT=10
EXPLICIT_WAIT=20

# Features
SCREENSHOT_ON_FAILURE=true
RETRY_COUNT=3
```

---

## Writing Tests

### Pytest Tests

```python
import pytest
from pages.login_page import LoginPage

class TestLogin:
    @pytest.fixture(autouse=True)
    def setup_test(self, driver):
        self.login_page = LoginPage(driver)
    
    def test_successful_login(self):
        self.login_page.navigate_to_page()
        self.login_page.login("user", "pass")
        assert self.login_page.is_login_successful()
```

### BDD Tests (Behave)

```gherkin
# features/login.feature
Feature: User Login
  Scenario: Successful login
    Given I am on the login page
    When I enter valid credentials
    Then I should be logged in
```

```python
# features/steps/login_steps.py
from behave import given, when, then

@given('I am on the login page')
def step_impl(context):
    context.login_page.navigate_to_page()
```

---

## Test Execution

```bash
# Run all tests
pytest                              # Pytest tests
behave                              # BDD tests

# Filtering
pytest -k "login"                   # Filter by name
behave --tags=smoke                 # Filter by tag

# Parallel execution
pytest -n auto                      # Auto-detect cores
pytest -n 4                         # 4 workers

# Specific browsers
pytest --browser=firefox
BROWSER=firefox pytest
```

---

## Documentation

- **[README.md](README.md)** - This file (quick start)
- **[docs/GUIA_NOVATOS.md](docs/GUIA_NOVATOS.md)** - Spanish beginner guide
- **[prompts/](prompts/)** - Complete AI context for code generation
- **[CHANGELOG.md](CHANGELOG.md)** - Version history

---

## Docker Execution

```bash
# Build image
docker build -t automation-framework .

# Run tests
docker run automation-framework pytest
docker run automation-framework behave
```

---

## Test Results

Current status:
- **Pytest Tests:** 14 passed, 2 skipped (87.5% pass rate)
- **BDD Scenarios:** 3 feature files with multiple scenarios
- **Execution Time:** ~50 seconds (parallel)

---

## Requirements

- Python 3.9+
- Chrome/Firefox/Edge browser
- pip (Python package manager)

---

## Support

For detailed documentation:
- Technical Reference: `prompts/context/FRAMEWORK.md`
- Architecture Details: `prompts/context/architecture.md`
- Best Practices: `prompts/context/best_practices.md`
- BDD Guide: `prompts/context/bdd_with_behave.md`
- Troubleshooting: `prompts/context/troubleshooting.md`

---

## License

[Add your license here]

---

**Framework Version:** 1.2.0  
**Status:** Production Ready ✅
