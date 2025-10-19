"""
Behave environment configuration
Sets up browser and other resources for BDD tests
"""
from config.browser_setup import BrowserManager
from config.settings import TestSettings
from utils.logger import logger
from utils.screenshot_capture import ScreenshotCapture

def before_all(context):
    """
    Runs once before all features
    Setup global configuration
    """
    logger.info("=" * 60)
    logger.info("🚀 BEHAVE TEST SUITE STARTING")
    logger.info("=" * 60)
    logger.info(f"Environment: {TestSettings.ENVIRONMENT}")
    logger.info(f"Browser: {TestSettings.BROWSER}")
    logger.info(f"Headless: {TestSettings.HEADLESS}")
    logger.info("=" * 60)

def before_feature(context, feature):
    """
    Runs before each feature
    """
    logger.info(f"📋 Feature: {feature.name}")

def before_scenario(context, scenario):
    """
    Runs before each scenario
    Initialize browser for each scenario
    """
    logger.info(f"🎬 Scenario: {scenario.name}")
    
    # Initialize browser
    context.browser = TestSettings.BROWSER
    context.driver = BrowserManager.get_driver(context.browser)
    
    # Initialize screenshot utility
    context.screenshot = ScreenshotCapture(context.driver)
    
    logger.info(f"✅ Browser initialized: {context.browser}")

def after_scenario(context, scenario):
    """
    Runs after each scenario
    Cleanup browser and capture screenshots on failure
    """
    # Capture screenshot if scenario failed
    if scenario.status == "failed":
        logger.error(f"❌ Scenario FAILED: {scenario.name}")
        screenshot_name = f"FAILURE_{scenario.name.replace(' ', '_')}"
        screenshot_path = context.screenshot.capture_on_failure(
            screenshot_name,
            "Scenario failed"
        )
        if screenshot_path:
            logger.info(f"📸 Failure screenshot: {screenshot_path}")
    else:
        logger.info(f"✅ Scenario PASSED: {scenario.name}")
    
    # Quit browser
    if hasattr(context, 'driver'):
        try:
            context.driver.quit()
            logger.info("🔒 Browser closed")
        except Exception as e:
            logger.warning(f"⚠️  Error closing browser: {str(e)}")

def after_feature(context, feature):
    """
    Runs after each feature
    """
    logger.info(f"✓ Feature completed: {feature.name}")
    logger.info("-" * 60)

def after_all(context):
    """
    Runs once after all features
    """
    logger.info("=" * 60)
    logger.info("🏁 BEHAVE TEST SUITE COMPLETED")
    logger.info("=" * 60)

def before_tag(context, tag):
    """
    Runs before scenarios with specific tags
    Can be used for conditional setup
    """
    if tag == "slow":
        logger.info("⚠️  Running slow test - increased timeout")
        if hasattr(context, 'driver'):
            context.driver.set_page_load_timeout(60)
    
    if tag == "api":
        logger.info("🔌 API test - setting up API client")
        # Setup API client if needed
    
    if tag == "database":
        logger.info("💾 Database test - setting up database connection")
        # Setup database connection if needed

def after_tag(context, tag):
    """
    Runs after scenarios with specific tags
    """
    pass

def before_step(context, step):
    """
    Runs before each step
    Optional: useful for detailed logging
    """
    # Uncomment for very detailed logging
    # logger.debug(f"Step: {step.name}")
    pass

def after_step(context, step):
    """
    Runs after each step
    Can be used to capture step-level screenshots
    """
    if step.status == "failed":
        logger.error(f"❌ Step failed: {step.name}")

