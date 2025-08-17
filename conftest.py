import pytest
import os
from datetime import datetime
from config.browser_setup import BrowserManager
from config.settings import TestSettings
from utils.logger import logger
from utils.screenshot_capture import ScreenshotCapture

def pytest_addoption(parser):
    """Add custom command line options for test configuration"""
    parser.addoption(
        "--browser", 
        action="store", 
        default=TestSettings.BROWSER, 
        help="Choose browser: chrome, firefox, edge"
    )
    parser.addoption(
        "--headless", 
        action="store_true", 
        default=TestSettings.HEADLESS,
        help="Run tests in headless mode"
    )
    parser.addoption(
        "--environment", 
        action="store", 
        default=TestSettings.ENVIRONMENT,
        help="Test environment: staging, production, development"
    )
    parser.addoption(
        "--parallel", 
        action="store_true", 
        default=False,
        help="Run tests in parallel mode"
    )

@pytest.fixture(scope="session")
def test_session_info():
    """Provide test session information"""
    return {
        "start_time": datetime.now().isoformat(),
        "environment": TestSettings.ENVIRONMENT,
        "browser": TestSettings.BROWSER,
        "headless": TestSettings.HEADLESS
    }

@pytest.fixture(scope="function")
def driver(request):
    """
    Initialize WebDriver and provide it to tests with proper cleanup
    
    This fixture:
    - Creates a new browser instance for each test
    - Captures screenshots on test failures
    - Ensures proper cleanup after each test
    - Logs test execution details
    """
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    
    # Override settings if command line options are provided
    if headless != TestSettings.HEADLESS:
        os.environ["HEADLESS"] = str(headless).lower()
    
    driver = None
    screenshot_capture = None
    
    try:
        # Initialize browser driver
        logger.info(f"🚀 Initializing {browser} browser for test: {request.node.name}")
        driver = BrowserManager.get_driver(browser)
        
        # Initialize screenshot capture
        screenshot_capture = ScreenshotCapture(driver)
        
        # Log driver information
        driver_info = BrowserManager.get_driver_info(driver)
        logger.info(f"Browser initialized: {driver_info}")
        
        yield driver
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize browser for test {request.node.name}: {str(e)}")
        raise
    
    finally:
        # Cleanup: close browser and capture final screenshot
        if driver:
            try:
                # Capture screenshot before closing (useful for debugging)
                if screenshot_capture:
                    final_screenshot = screenshot_capture.capture_screenshot(
                        f"test_end_{request.node.name.replace(' ', '_')}"
                    )
                    if final_screenshot:
                        logger.debug(f"Final screenshot captured: {final_screenshot}")
                
                driver.quit()
                logger.info(f"✅ Browser closed for test: {request.node.name}")
                
            except Exception as e:
                logger.warning(f"⚠️ Error during browser cleanup: {str(e)}")

@pytest.fixture(scope="function")
def screenshot_capture(driver):
    """Provide screenshot capture utility for tests"""
    return ScreenshotCapture(driver)

@pytest.fixture(scope="function")
def test_data():
    """Provide test data for tests"""
    return {
        "valid_user": {
            "username": "test_user",
            "password": "test_password",
            "email": "test@example.com"
        },
        "invalid_user": {
            "username": "invalid_user",
            "password": "wrong_password",
            "email": "invalid@example.com"
        },
        "test_urls": {
            "github_cli": "https://cli.github.com",
            "login": "https://example.com/login",
            "dashboard": "https://example.com/dashboard"
        }
    }

@pytest.fixture(autouse=True)
def test_logging(request):
    """Automatically log test start and end"""
    test_name = request.node.name
    
    # Log test start
    logger.log_test_start(test_name)
    
    yield
    
    # Log test end (this will run after the test completes)
    # Note: We can't determine pass/fail here as pytest handles that separately
    logger.log_test_end(test_name, "completed")

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """Configure pytest with metadata and custom options"""
    if hasattr(config, "_metadata"):
        config._metadata["Project Name"] = "Automation Framework"
        config._metadata["Tested By"] = "QA Team"
        config._metadata["Platform"] = "Windows"
        config._metadata["Python Version"] = "3.13"
        config._metadata["Environment"] = TestSettings.ENVIRONMENT
        config._metadata["Browser"] = TestSettings.BROWSER
        config._metadata["Headless Mode"] = str(TestSettings.HEADLESS)
        config._metadata["Framework Version"] = "2.0.0"

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture screenshots and additional information on test failures"""
    outcome = yield
    report = outcome.get_result()
    
    # Only process if the test failed
    if report.when == "call" and report.failed:
        try:
            # Get the driver from the test if available
            driver = item.funcargs.get("driver")
            if driver:
                # Capture screenshot on failure
                screenshot_capture = ScreenshotCapture(driver)
                screenshot_path = screenshot_capture.capture_on_failure(
                    item.name, 
                    str(call.excinfo) if call.excinfo else "Test failed"
                )
                
                # Add screenshot to the report
                if screenshot_path and os.path.exists(screenshot_path):
                    report.attachments.append(("screenshot", screenshot_path, "image/png"))
                    logger.info(f"📸 Failure screenshot captured: {screenshot_path}")
                
        except Exception as e:
            logger.warning(f"⚠️ Failed to capture failure screenshot: {str(e)}")

@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    """Log test session completion summary"""
    logger.info("=" * 60)
    logger.info("🏁 TEST SESSION COMPLETED")
    logger.info("=" * 60)
    logger.info(f"Exit status: {exitstatus}")
    logger.info(f"Total tests collected: {len(session.items)}")
    
    # Count passed and failed tests safely
    passed_count = 0
    failed_count = 0
    
    for item in session.items:
        if hasattr(item, 'rep_call'):
            if hasattr(item.rep_call, 'passed') and item.rep_call.passed:
                passed_count += 1
            elif hasattr(item.rep_call, 'failed') and item.rep_call.failed:
                failed_count += 1
    
    logger.info(f"Tests passed: {passed_count}")
    logger.info(f"Tests failed: {failed_count}")
    logger.info("=" * 60)
