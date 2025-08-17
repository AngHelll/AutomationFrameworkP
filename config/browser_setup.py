from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.common.exceptions import WebDriverException
from utils.logger import logger
from config.settings import TestSettings

class BrowserManager:
    """Manages browser initialization and configuration"""
    
    @staticmethod
    def get_driver(browser: str = None) -> webdriver.Remote:
        """
        Initialize WebDriver with latest version and proper configuration
        
        Args:
            browser: Browser type (chrome, firefox, edge)
            
        Returns:
            Configured WebDriver instance
            
        Raises:
            ValueError: If browser type is not supported
            WebDriverException: If driver initialization fails
        """
        browser = browser or TestSettings.BROWSER
        
        try:
            logger.info(f"Initializing {browser} browser driver")
            
            if browser == "chrome":
                driver = BrowserManager._setup_chrome_driver()
            elif browser == "firefox":
                driver = BrowserManager._setup_firefox_driver()
            elif browser == "edge":
                driver = BrowserManager._setup_edge_driver()
            else:
                raise ValueError(f"Unsupported browser: {browser}")
            
            # Apply common driver settings
            BrowserManager._apply_common_settings(driver)
            
            logger.info(f"Successfully initialized {browser} browser driver")
            return driver
            
        except Exception as e:
            logger.error(f"Failed to initialize {browser} browser driver: {str(e)}")
            raise WebDriverException(f"Browser initialization failed: {str(e)}")
    
    @staticmethod
    def _setup_chrome_driver() -> webdriver.Chrome:
        """Setup Chrome driver with optimized options"""
        try:
            options = webdriver.ChromeOptions()
            browser_options = TestSettings.get_browser_options()["chrome"]
            
            # Apply configuration from settings
            if browser_options["headless"]:
                options.add_argument("--headless")
            
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument(f"--window-size={browser_options['window_size']}")
            
            # Additional performance optimizations
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-plugins")
            options.add_argument("--disable-images")  # Optional: disable images for faster loading
            options.add_argument("--disable-javascript")  # Optional: disable JS for faster loading
            
            # Set user agent
            options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
            
            # Download and setup ChromeDriver
            chrome_service = ChromeService(ChromeDriverManager().install())
            
            driver = webdriver.Chrome(service=chrome_service, options=options)
            logger.debug("Chrome driver setup completed successfully")
            return driver
            
        except Exception as e:
            logger.error(f"Chrome driver setup failed: {str(e)}")
            raise
    
    @staticmethod
    def _setup_firefox_driver() -> webdriver.Firefox:
        """Setup Firefox driver with optimized options"""
        try:
            options = webdriver.FirefoxOptions()
            browser_options = TestSettings.get_browser_options()["firefox"]
            
            # Apply configuration from settings
            if browser_options["headless"]:
                options.add_argument("--headless")
            
            options.add_argument(f"--width={browser_options['window_size'].split(',')[0]}")
            options.add_argument(f"--height={browser_options['window_size'].split(',')[1]}")
            
            # Additional Firefox optimizations
            options.set_preference("dom.webdriver.enabled", False)
            options.set_preference("useAutomationExtension", False)
            options.set_preference("general.useragent.override", 
                                 "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0")
            
            # Download and setup GeckoDriver
            firefox_service = FirefoxService(GeckoDriverManager().install())
            
            driver = webdriver.Firefox(service=firefox_service, options=options)
            logger.debug("Firefox driver setup completed successfully")
            return driver
            
        except Exception as e:
            logger.error(f"Firefox driver setup failed: {str(e)}")
            raise
    
    @staticmethod
    def _setup_edge_driver() -> webdriver.Edge:
        """Setup Edge driver with optimized options"""
        try:
            options = webdriver.EdgeOptions()
            browser_options = TestSettings.get_browser_options()["edge"]
            
            # Apply configuration from settings
            if browser_options["headless"]:
                options.add_argument("--headless")
            
            options.add_argument(f"--window-size={browser_options['window_size']}")
            
            # Additional Edge optimizations
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-plugins")
            options.add_argument("--disable-images")
            options.add_argument("--disable-javascript")
            
            # Download and setup EdgeDriver
            edge_service = EdgeService(EdgeChromiumDriverManager().install())
            
            driver = webdriver.Edge(service=edge_service, options=options)
            logger.debug("Edge driver setup completed successfully")
            return driver
            
        except Exception as e:
            logger.error(f"Edge driver setup failed: {str(e)}")
            raise
    
    @staticmethod
    def _apply_common_settings(driver: webdriver.Remote) -> None:
        """Apply common settings to all browser drivers"""
        try:
            # Set implicit wait
            driver.implicitly_wait(TestSettings.IMPLICIT_WAIT)
            
            # Maximize window (if not headless)
            if not TestSettings.HEADLESS:
                driver.maximize_window()
            
            # Set page load timeout
            driver.set_page_load_timeout(TestSettings.EXPLICIT_WAIT)
            
            # Set script timeout
            driver.set_script_timeout(TestSettings.EXPLICIT_WAIT)
            
            logger.debug("Common driver settings applied successfully")
            
        except Exception as e:
            logger.warning(f"Failed to apply some common settings: {str(e)}")
    
    @staticmethod
    def get_driver_info(driver: webdriver.Remote) -> dict:
        """Get information about the current driver"""
        try:
            return {
                "browser_name": driver.name,
                "browser_version": driver.capabilities.get("browserVersion", "Unknown"),
                "driver_version": driver.capabilities.get("chrome", {}).get("chromedriverVersion", "Unknown"),
                "platform": driver.capabilities.get("platformName", "Unknown"),
                "window_size": driver.get_window_size()
            }
        except Exception as e:
            logger.warning(f"Failed to get driver info: {str(e)}")
            return {}

# Backward compatibility function
def get_driver(browser: str = "chrome") -> webdriver.Remote:
    """Legacy function for backward compatibility"""
    return BrowserManager.get_driver(browser)
