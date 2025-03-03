import pytest
from config.browser_setup import get_driver

def pytest_addoption(parser):
    """Allow browser selection from CLI."""
    parser.addoption("--browser", action="store", default="chrome", help="Choose browser: chrome, firefox, edge")

@pytest.fixture
def driver(request):
    """Initialize WebDriver and close it after each test."""
    browser = request.config.getoption("--browser")
    driver = get_driver(browser)
    driver.get("https://example.com/login")  # Replace with actual test URL
    yield driver
    driver.quit()

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """Add metadata to pytest-html reports."""
    if hasattr(config, "_metadata"):
        config._metadata["Project Name"] = "Automation Framework"
        config._metadata["Tested By"] = "QA Team"
        config._metadata["Platform"] = "Windows"
        config._metadata["Python Version"] = "3.13"
