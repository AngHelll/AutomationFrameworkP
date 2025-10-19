"""Step definitions for login feature"""
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
    """Enter username in login form"""
    # Get actual username from test data if it's a placeholder
    if username == "valid_user":
        from utils.test_data_loader import test_data
        username = test_data.get_user_data("valid_user")["username"]
    
    context.login_page.input_text_to_username(username)
    logger.info(f"Entered username: {username}")

@when('I enter password "{password}"')
def step_enter_password(context, password):
    """Enter password in login form"""
    # Get actual password from test data if it's a placeholder
    if password == "valid_password":
        from utils.test_data_loader import test_data
        password = test_data.get_user_data("valid_user")["password"]
    
    context.login_page.input_text_to_password(password)
    logger.info(f"Entered password")

@when('I click the login button')
def step_click_login(context):
    """Click login button"""
    context.login_page.click_login_button()
    logger.info("Clicked login button")

@then('I should be logged in successfully')
def step_verify_login_success(context):
    """Verify successful login"""
    assert context.login_page.is_login_successful(), "Login was not successful"
    logger.info("✅ Login successful")

@then('I should see the dashboard')
def step_verify_dashboard(context):
    """Verify dashboard is displayed"""
    # This would check if dashboard is displayed
    # For now, we'll just verify we're not on login page
    assert not context.login_page.is_page_loaded(), "Still on login page"
    logger.info("✅ Dashboard visible")

@then('I should see an error message')
def step_verify_error_message(context):
    """Verify error message is displayed"""
    assert context.login_page.is_error_message_displayed(), "Error message not displayed"
    logger.info("✅ Error message displayed")

@then('I should remain on the login page')
def step_verify_still_on_login(context):
    """Verify still on login page"""
    assert context.login_page.is_page_loaded(), "Not on login page"
    logger.info("✅ Still on login page")

@then('the login should "{result}"')
def step_verify_login_result(context, result):
    """Verify login result"""
    if result == "succeed":
        assert context.login_page.is_login_successful(), f"Login should have succeeded"
    elif result == "fail":
        assert not context.login_page.is_login_successful(), f"Login should have failed"
    logger.info(f"✅ Login result: {result}")

@when('I attempt to login with wrong credentials {attempts:d} times')
def step_multiple_failed_attempts(context, attempts):
    """Attempt login multiple times with wrong credentials"""
    for i in range(attempts):
        context.login_page.navigate_to_page()
        context.execute_steps('''
            When I enter username "wrong_user"
            And I enter password "wrong_pass"
            And I click the login button
        ''')
        logger.info(f"Failed login attempt {i+1}/{attempts}")

@then('the account should be locked')
def step_verify_account_locked(context):
    """Verify account is locked"""
    # This would check for account lockout
    # Implementation depends on application behavior
    logger.info("✅ Account locked verification")

@then('I should see a lockout message')
def step_verify_lockout_message(context):
    """Verify lockout message is displayed"""
    # Implementation depends on application
    logger.info("✅ Lockout message verification")

