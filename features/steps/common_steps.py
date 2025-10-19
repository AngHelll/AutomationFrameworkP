"""Common step definitions used across features"""
from behave import given, when, then
from pages.login_page import LoginPage
from utils.logger import logger

@given('I navigate to "{url}"')
def step_navigate_to_url(context, url):
    """Navigate to specified URL"""
    context.driver.get(url)
    context.current_url = url
    logger.info(f"Navigated to: {url}")

@then('the page title should contain "{text}"')
def step_verify_page_title(context, text):
    """Verify page title contains text"""
    title = context.driver.title
    assert text in title, f"Expected '{text}' in title, got '{title}'"
    logger.info(f"✅ Page title contains: {text}")

@when('I get the main header text')
def step_get_header_text(context):
    """Get main header text"""
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    wait = WebDriverWait(context.driver, 10)
    header = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
    context.header_text = header.text
    logger.info(f"Header text: {context.header_text}")

@then('it should contain "{text}"')
def step_verify_text_contains(context, text):
    """Verify stored text contains expected text"""
    assert hasattr(context, 'header_text'), "Header text not stored"
    assert text in context.header_text, f"Expected '{text}' in '{context.header_text}'"
    logger.info(f"✅ Text contains: {text}")

@then('the paragraph text should be displayed')
def step_verify_paragraph_displayed(context):
    """Verify paragraph text is displayed"""
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    wait = WebDriverWait(context.driver, 10)
    paragraph = wait.until(EC.presence_of_element_located((By.TAG_NAME, "p")))
    assert paragraph.is_displayed(), "Paragraph not displayed"
    logger.info("✅ Paragraph is displayed")

@then('a link should be present on the page')
def step_verify_link_present(context):
    """Verify at least one link is present"""
    from selenium.webdriver.common.by import By
    links = context.driver.find_elements(By.TAG_NAME, "a")
    assert len(links) > 0, "No links found on page"
    logger.info(f"✅ Found {len(links)} link(s) on page")

@when('I wait for {seconds:d} seconds')
def step_wait_seconds(context, seconds):
    """Wait for specified seconds"""
    import time
    time.sleep(seconds)
    logger.info(f"Waited {seconds} seconds")

@then('the element "{locator}" should be visible')
def step_verify_element_visible(context, locator):
    """Verify element is visible by CSS selector"""
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    wait = WebDriverWait(context.driver, 10)
    element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, locator)))
    assert element.is_displayed()
    logger.info(f"✅ Element visible: {locator}")

@when('I click the element "{locator}"')
def step_click_element(context, locator):
    """Click element by CSS selector"""
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    wait = WebDriverWait(context.driver, 10)
    element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, locator)))
    element.click()
    logger.info(f"Clicked element: {locator}")

@then('the current URL should contain "{text}"')
def step_verify_url_contains(context, text):
    """Verify current URL contains text"""
    current_url = context.driver.current_url
    assert text in current_url, f"Expected '{text}' in URL, got '{current_url}'"
    logger.info(f"✅ URL contains: {text}")

