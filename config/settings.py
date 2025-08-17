import os
from typing import Dict, Any

class TestSettings:
    """Centralized configuration management for the automation framework"""
    
    # Environment Configuration
    ENVIRONMENT = os.getenv("TEST_ENV", "staging")
    BASE_URL = os.getenv("BASE_URL", "https://cli.github.com")
    
    # Browser Configuration
    BROWSER = os.getenv("BROWSER", "chrome")
    HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
    IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", "10"))
    EXPLICIT_WAIT = int(os.getenv("EXPLICIT_WAIT", "20"))
    
    # Test Configuration
    SCREENSHOT_ON_FAILURE = os.getenv("SCREENSHOT_ON_FAILURE", "true").lower() == "true"
    RETRY_COUNT = int(os.getenv("RETRY_COUNT", "3"))
    RETRY_DELAY = int(os.getenv("RETRY_DELAY", "2"))
    
    # Reporting Configuration
    ALLURE_RESULTS_DIR = os.getenv("ALLURE_RESULTS_DIR", "reports/allure-results")
    HTML_REPORT_DIR = os.getenv("HTML_REPORT_DIR", "reports")
    
    # Test Data Configuration
    TEST_DATA_PATH = os.getenv("TEST_DATA_PATH", "test_data")
    
    @classmethod
    def get_browser_options(cls) -> Dict[str, Any]:
        """Get browser-specific options"""
        return {
            "chrome": {
                "headless": cls.HEADLESS,
                "no_sandbox": True,
                "disable_dev_shm_usage": True,
                "disable_gpu": True,
                "window_size": "1920,1080"
            },
            "firefox": {
                "headless": cls.HEADLESS,
                "window_size": "1920,1080"
            },
            "edge": {
                "headless": cls.HEADLESS,
                "window_size": "1920,1080"
            }
        }
    
    @classmethod
    def get_urls(cls) -> Dict[str, str]:
        """Get application URLs"""
        return {
            "github_cli": f"{cls.BASE_URL}",
            "login": f"{cls.BASE_URL}/login",
            "dashboard": f"{cls.BASE_URL}/dashboard"
        }
