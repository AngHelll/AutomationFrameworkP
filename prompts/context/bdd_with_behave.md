# BDD with Behave - Complete Guide for AI

## What is BDD?

**Behavior-Driven Development (BDD)** is a software development approach that:
- Uses natural language to describe test scenarios
- Makes tests readable by non-technical stakeholders
- Focuses on behavior rather than implementation
- Follows Given-When-Then pattern

## Framework BDD Setup

### Technology
- **Framework:** Behave 1.2.6
- **Language:** Gherkin (Given-When-Then syntax)
- **Integration:** Works alongside Pytest tests

### Directory Structure

```
features/
├── environment.py           # Behave hooks and setup
├── behave.ini              # Behave configuration
├── login.feature           # Login scenarios
├── github_cli.feature      # GitHub CLI scenarios
├── example.feature         # Simple example scenarios
│
└── steps/                  # Step definitions
    ├── login_steps.py      # Login step implementations
    ├── github_cli_steps.py # GitHub CLI step implementations
    └── common_steps.py     # Reusable steps
```

---

## Gherkin Syntax

### Basic Structure

```gherkin
Feature: Feature Name
  As a [role]
  I want to [action]
  So that [benefit]

  Scenario: Scenario Name
    Given [context/precondition]
    When [action]
    And [additional action]
    Then [expected outcome]
    And [additional outcome]
```

### Keywords

| Keyword | Purpose | Example |
|---------|---------|---------|
| `Feature` | Groups related scenarios | `Feature: User Login` |
| `Scenario` | Single test case | `Scenario: Successful login` |
| `Given` | Setup/preconditions | `Given I am on the login page` |
| `When` | Actions | `When I click the login button` |
| `Then` | Assertions | `Then I should see the dashboard` |
| `And` | Additional steps | `And I should see a welcome message` |
| `But` | Negative assertions | `But I should not see an error` |
| `Background` | Common steps for all scenarios | Runs before each scenario |
| `Scenario Outline` | Data-driven scenarios | With Examples table |
| `Examples` | Test data for outlines | Table of parameters |

---

## Feature Files

### Example: login.feature

```gherkin
Feature: User Login
  As a user
  I want to log in to the application
  So that I can access my account

  Background:
    Given I am on the login page

  @smoke @login
  Scenario: Successful login with valid credentials
    When I enter username "valid_user"
    And I enter password "valid_password"
    And I click the login button
    Then I should be logged in successfully
    And I should see the dashboard

  @login
  Scenario Outline: Login with different credentials
    When I enter username "<username>"
    And I enter password "<password>"
    And I click the login button
    Then the login should "<result>"

    Examples:
      | username      | password    | result  |
      | valid_user    | valid_pass  | succeed |
      | invalid_user  | wrong_pass  | fail    |
```

---

## Step Definitions

### Basic Steps

```python
# features/steps/login_steps.py
from behave import given, when, then
from pages.login_page import LoginPage
from utils.logger import logger

@given('I am on the login page')
def step_navigate_to_login(context):
    """Navigate to login page"""
    context.login_page = LoginPage(context.driver)
    context.login_page.navigate_to_page()
    logger.info("Navigated to login page")

@when('I enter username "{username}"')
def step_enter_username(context, username):
    """Enter username"""
    context.login_page.input_username(username)
    logger.info(f"Entered username: {username}")

@then('I should be logged in successfully')
def step_verify_login(context):
    """Verify successful login"""
    assert context.login_page.is_login_successful()
    logger.info("✅ Login successful")
```

### Step Parameters

```python
# String parameter
@when('I enter username "{username}"')
def step(context, username):
    pass

# Integer parameter
@when('I wait for {seconds:d} seconds')
def step(context, seconds):
    pass

# Float parameter
@then('the price should be {price:f} dollars')
def step(context, price):
    pass
```

### Context Object

```python
# Store data in context
context.username = "test_user"
context.login_page = LoginPage(context.driver)

# Access later
username = context.username
context.login_page.login(username, password)
```

---

## environment.py Hooks

```python
# features/environment.py

def before_all(context):
    """Runs once before all features"""
    # Global setup
    logger.info("Test suite starting")

def before_feature(context, feature):
    """Runs before each feature"""
    logger.info(f"Feature: {feature.name}")

def before_scenario(context, scenario):
    """Runs before each scenario"""
    # Initialize browser for each scenario
    context.driver = BrowserManager.get_driver()
    logger.info(f"Scenario: {scenario.name}")

def after_scenario(context, scenario):
    """Runs after each scenario"""
    # Capture screenshot on failure
    if scenario.status == "failed":
        context.screenshot.capture_on_failure(scenario.name, "Failed")
    
    # Quit browser
    context.driver.quit()

def after_all(context):
    """Runs once after all features"""
    logger.info("Test suite completed")
```

---

## Running Behave Tests

### Basic Commands

```bash
# Run all features
behave

# Run specific feature
behave features/login.feature

# Run with tags
behave --tags=smoke
behave --tags=login
behave --tags="smoke and login"
behave --tags="not slow"

# Run specific scenario
behave features/login.feature:10  # Line number

# Verbose output
behave -v

# Show skipped scenarios
behave --show-skipped

# Stop on first failure
behave --stop

# Dry run (check syntax)
behave --dry-run

# Generate JUnit XML
behave --junit --junit-directory=reports/behave-junit
```

### Parallel Execution

```bash
# Install behave-parallel
pip install behave-parallel

# Run in parallel
behave --parallel
behave --parallel --processes 4
```

---

## Tags

### Using Tags

```gherkin
@smoke @login
Scenario: Quick smoke test
  # Tagged with both smoke and login

@slow
Scenario: Performance test
  # Tagged as slow test

@wip  # Work In Progress
Scenario: Not ready yet
  # Skip this in CI/CD
```

### Running Tagged Scenarios

```bash
# Run smoke tests
behave --tags=smoke

# Run everything except slow tests
behave --tags="not slow"

# Run smoke OR login
behave --tags="smoke,login"

# Run smoke AND login
behave --tags="smoke and login"

# Skip WIP scenarios
behave --tags="not wip"
```

---

## Best Practices

### 1. Write Declarative Scenarios

✅ **DO:**
```gherkin
Scenario: User logs in successfully
  Given I am logged in as "admin"
  When I navigate to the dashboard
  Then I should see my profile
```

❌ **DON'T:**
```gherkin
Scenario: User logs in successfully
  Given I open browser
  And I navigate to "https://example.com/login"
  And I find element with id "username"
  And I type "admin"
  # Too implementation-focused!
```

### 2. Keep Scenarios Independent

Each scenario should:
- Set up its own prerequisites
- Not depend on other scenarios
- Clean up after itself

### 3. Use Background Wisely

```gherkin
Feature: Dashboard
  Background:
    Given I am logged in as "user"
    # Runs before EVERY scenario

  Scenario: View profile
    When I click on profile
    # Background runs first

  Scenario: Edit settings
    When I click on settings
    # Background runs again
```

### 4. Use Scenario Outline for Data-Driven Tests

```gherkin
Scenario Outline: Login with various credentials
  When I login with "<username>" and "<password>"
  Then the result should be "<result>"

  Examples:
    | username | password | result  |
    | admin    | pass123  | success |
    | user     | wrong    | fail    |
    | empty    | pass123  | fail    |
```

### 5. Reuse Steps

Create common steps that can be reused:

```python
# common_steps.py
@given('I navigate to "{url}"')
def step_navigate(context, url):
    context.driver.get(url)

@then('the page title should contain "{text}"')
def step_verify_title(context, text):
    assert text in context.driver.title
```

---

## Integration with Page Objects

```python
# features/steps/login_steps.py
from behave import given, when, then
from pages.login_page import LoginPage

@given('I am on the login page')
def step_impl(context):
    # Use existing page objects!
    context.login_page = LoginPage(context.driver)
    context.login_page.navigate_to_page()

@when('I login with valid credentials')
def step_impl(context):
    # Reuse page object methods
    context.login_page.login("user", "password")

@then('I should be logged in')
def step_impl(context):
    # Use page object assertions
    assert context.login_page.is_login_successful()
```

---

## Debugging BDD Tests

### 1. Verbose Output

```bash
behave -v  # Verbose
behave --no-capture  # Show print statements
```

### 2. Run Single Scenario

```bash
# By line number
behave features/login.feature:15

# By name (partial match)
behave --name="successful login"
```

### 3. Add Debug Steps

```python
@when('I debug')
def step_debug(context):
    import pdb; pdb.set_trace()
    # Debugger stops here
```

### 4. Check Undefined Steps

```bash
behave --dry-run
# Shows which steps are not implemented
```

---

## Common Patterns

### Pattern 1: Login Before Tests

```gherkin
Background:
  Given I am logged in as "admin"
```

```python
@given('I am logged in as "{user}"')
def step_login(context, user):
    context.execute_steps(f'''
        Given I am on the login page
        When I enter username "{user}"
        And I enter password "password"
        And I click login
    ''')
```

### Pattern 2: Table Data

```gherkin
Scenario: Create users
  Given the following users exist:
    | username | email           | role  |
    | alice    | alice@test.com  | admin |
    | bob      | bob@test.com    | user  |
```

```python
@given('the following users exist')
def step_create_users(context):
    for row in context.table:
        username = row['username']
        email = row['email']
        role = row['role']
        # Create user
```

### Pattern 3: Multi-line Text

```gherkin
Scenario: Send message
  When I send the following message:
    """
    Hello,
    This is a multi-line message.
    Best regards
    """
```

```python
@when('I send the following message')
def step_send_message(context):
    message = context.text  # Multi-line text
    # Send message
```

---

## Behave vs Pytest

| Aspect | Behave | Pytest |
|--------|--------|--------|
| Syntax | Gherkin (natural language) | Python code |
| Readability | High (non-technical friendly) | Medium (technical) |
| Flexibility | Medium | High |
| Best For | Acceptance tests, BDD | Unit/Integration tests |
| Stakeholder | Business team | Development team |

**Use Both:**
- Behave for high-level business scenarios
- Pytest for technical/unit tests

---

## AI Assistant Capabilities

When helping with BDD:

### Can Generate:
- Feature files from requirements
- Step definitions from features
- Page object integration
- Test data tables
- Tagged scenarios

### Can Help With:
- Converting pytest tests to BDD
- Writing clear Gherkin scenarios
- Implementing undefined steps
- Debugging step failures
- Organizing features

### Example Request:
**User:** "Create a BDD scenario for user registration"

**AI Response:**
```gherkin
Feature: User Registration
  As a new user
  I want to register an account
  So that I can use the application

  @smoke @registration
  Scenario: Successful registration with valid data
    Given I am on the registration page
    When I enter email "user@example.com"
    And I enter password "SecurePass123"
    And I enter password confirmation "SecurePass123"
    And I click the register button
    Then I should see a success message
    And I should receive a confirmation email
```

---

## Summary

✅ BDD with Behave is now integrated  
✅ Features folder with examples  
✅ Step definitions created  
✅ Environment hooks configured  
✅ Works with existing page objects  
✅ Can run alongside Pytest tests  

**Command:** `behave` to run all BDD scenarios!

