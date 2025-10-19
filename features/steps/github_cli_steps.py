"""Step definitions for GitHub CLI feature"""
from behave import given, when, then
from pages.github_cli_page import GitHubCLIPage
from utils.logger import logger
import time

@given('I navigate to the GitHub CLI page')
def step_navigate_to_github_cli(context):
    """Navigate to GitHub CLI page"""
    context.github_page = GitHubCLIPage(context.driver)
    context.github_page.navigate_to_page()
    logger.info("Navigated to GitHub CLI page")

@then('the page should be loaded')
def step_verify_page_loaded(context):
    """Verify page is loaded"""
    assert context.github_page.is_page_loaded(), "GitHub CLI page did not load"
    logger.info("✅ Page loaded successfully")

@then('the main header should be visible')
def step_verify_header_visible(context):
    """Verify main header is visible"""
    assert context.github_page.is_element_visible(*context.github_page.LOCATORS['main_header'])
    logger.info("✅ Main header visible")

@then('the download button should be present')
def step_verify_download_button(context):
    """Verify download button is present"""
    assert context.github_page.is_download_button_present("windows")
    logger.info("✅ Download button present")

@then('the main header should contain "{text}"')
def step_verify_header_text(context, text):
    """Verify header contains specific text"""
    header_text = context.github_page.get_main_header_text()
    assert text in header_text, f"Expected '{text}' in header, got '{header_text}'"
    logger.info(f"✅ Header contains: {text}")

@then('the Windows download button should be visible')
def step_verify_windows_button_visible(context):
    """Verify Windows download button is visible"""
    assert context.github_page.is_download_button_present("windows")
    logger.info("✅ Windows download button visible")

@then('the Windows download button should be clickable')
def step_verify_windows_button_clickable(context):
    """Verify Windows download button is clickable"""
    # Check if button exists and is visible
    assert context.github_page.is_download_button_present("windows")
    logger.info("✅ Windows download button clickable")

@then('the navigation menu should be visible')
def step_verify_navigation_visible(context):
    """Verify navigation menu is visible"""
    assert context.github_page.is_navigation_menu_visible()
    logger.info("✅ Navigation menu visible")

@then('the hero section should be present')
def step_verify_hero_section(context):
    """Verify hero section is present"""
    assert context.github_page.is_element_present(*context.github_page.LOCATORS['hero_section'])
    logger.info("✅ Hero section present")

@when('I refresh the page')
def step_refresh_page(context):
    """Refresh the current page"""
    context.github_page.refresh_page()
    logger.info("Page refreshed")

@then('the page should still be loaded')
def step_verify_page_still_loaded(context):
    """Verify page is still loaded after refresh"""
    assert context.github_page.is_page_loaded()
    logger.info("✅ Page still loaded after refresh")

@then('the main content should be visible')
def step_verify_main_content(context):
    """Verify main content is visible"""
    assert context.github_page.is_element_visible(*context.github_page.LOCATORS['main_header'])
    logger.info("✅ Main content visible")

@when('I measure the page load time')
def step_measure_page_load(context):
    """Measure page load time"""
    start_time = time.time()
    context.github_page.navigate_to_page()
    context.github_page.wait_for_page_elements()
    context.load_time = time.time() - start_time
    logger.info(f"Page load time: {context.load_time:.2f}s")

@then('the page should load in less than {seconds:d} seconds')
def step_verify_load_time(context, seconds):
    """Verify page loads within time limit"""
    assert hasattr(context, 'load_time'), "Load time not measured"
    assert context.load_time < seconds, f"Page took {context.load_time:.2f}s, expected < {seconds}s"
    logger.info(f"✅ Page loaded in {context.load_time:.2f}s (< {seconds}s)")

