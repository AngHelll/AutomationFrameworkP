from abc import ABC, abstractmethod
from typing import Optional, List
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utils.logger import logger
from utils.retry_mechanism import retry_on_exception, ElementRetry
from utils.screenshot_capture import ScreenshotCapture
from config.settings import TestSettings

class BasePage(ABC):
    """Base class for all page objects with common functionality"""
    
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, TestSettings.EXPLICIT_WAIT)
        self.retry = ElementRetry(
            max_attempts=TestSettings.RETRY_COUNT,
            delay=TestSettings.RETRY_DELAY
        )
        self.screenshot = ScreenshotCapture(driver)
        self.page_url = self._get_page_url()
    
    @abstractmethod
    def _get_page_url(self) -> str:
        """Return the URL for this page - must be implemented by subclasses"""
        pass
    
    @abstractmethod
    def is_page_loaded(self) -> bool:
        """Verify that the page has loaded correctly - must be implemented by subclasses"""
        pass
    
    def navigate_to_page(self) -> None:
        """Navigate to the page URL"""
        try:
            logger.log_page_navigation(self.page_url)
            self.driver.get(self.page_url)
            self.wait_for_page_load()
        except Exception as e:
            logger.error(f"Failed to navigate to {self.page_url}: {str(e)}")
            raise
    
    def wait_for_page_load(self, timeout: int = None) -> None:
        """Wait for the page to load completely"""
        timeout = timeout or TestSettings.EXPLICIT_WAIT
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            logger.debug(f"Page loaded successfully: {self.page_url}")
        except TimeoutException:
            logger.warning(f"Page load timeout after {timeout} seconds")
    
    @retry_on_exception()
    def find_element(self, by: By, value: str, timeout: int = None) -> WebElement:
        """
        Find a single element with retry mechanism
        
        Args:
            by: Locator strategy (By.ID, By.CLASS_NAME, etc.)
            value: Locator value
            timeout: Custom timeout in seconds
            
        Returns:
            WebElement if found
            
        Raises:
            NoSuchElementException if element not found
        """
        timeout = timeout or TestSettings.EXPLICIT_WAIT
        wait = WebDriverWait(self.driver, timeout)
        
        element = wait.until(EC.presence_of_element_located((by, value)))
        logger.log_element_action("Found element", f"{by}={value}")
        return element
    
    @retry_on_exception()
    def find_elements(self, by: By, value: str, timeout: int = None) -> List[WebElement]:
        """
        Find multiple elements with retry mechanism
        
        Args:
            by: Locator strategy
            value: Locator value
            timeout: Custom timeout in seconds
            
        Returns:
            List of WebElements
        """
        timeout = timeout or TestSettings.EXPLICIT_WAIT
        wait = WebDriverWait(self.driver, timeout)
        
        elements = wait.until(EC.presence_of_all_elements_located((by, value)))
        logger.log_element_action(f"Found {len(elements)} elements", f"{by}={value}")
        return elements
    
    def wait_for_element_visible(self, by: By, value: str, timeout: int = None) -> WebElement:
        """Wait for element to be visible"""
        timeout = timeout or TestSettings.EXPLICIT_WAIT
        wait = WebDriverWait(self.driver, timeout)
        
        element = wait.until(EC.visibility_of_element_located((by, value)))
        logger.log_element_action("Element became visible", f"{by}={value}")
        return element
    
    def wait_for_element_clickable(self, by: By, value: str, timeout: int = None) -> WebElement:
        """Wait for element to be clickable"""
        timeout = timeout or TestSettings.EXPLICIT_WAIT
        wait = WebDriverWait(self.driver, timeout)
        
        element = wait.until(EC.element_to_be_clickable((by, value)))
        logger.log_element_action("Element became clickable", f"{by}={value}")
        return element
    
    def click_element(self, by: By, value: str, timeout: int = None) -> None:
        """Click on an element with retry mechanism"""
        try:
            element = self.wait_for_element_clickable(by, value, timeout)
            self.screenshot.capture_before_action(f"click_{value}")
            
            element.click()
            logger.log_element_action("Clicked element", f"{by}={value}")
            
            self.screenshot.capture_after_action(f"click_{value}")
            
        except Exception as e:
            logger.error(f"Failed to click element {by}={value}: {str(e)}")
            self.screenshot.capture_on_failure("click_element", str(e))
            raise
    
    def input_text(self, by: By, value: str, text: str, timeout: int = None) -> None:
        """Input text into an element with retry mechanism"""
        try:
            element = self.wait_for_element_visible(by, value, timeout)
            self.screenshot.capture_before_action(f"input_{value}")
            
            element.clear()
            element.send_keys(text)
            logger.log_element_action(f"Input text '{text}'", f"{by}={value}")
            
            self.screenshot.capture_after_action(f"input_{value}")
            
        except Exception as e:
            logger.error(f"Failed to input text into {by}={value}: {str(e)}")
            self.screenshot.capture_on_failure("input_text", str(e))
            raise
    
    def get_element_text(self, by: By, value: str, timeout: int = None) -> str:
        """Get text from an element with retry mechanism"""
        try:
            element = self.wait_for_element_visible(by, value, timeout)
            text = element.text
            logger.log_element_action(f"Retrieved text: '{text}'", f"{by}={value}")
            return text
        except Exception as e:
            logger.error(f"Failed to get text from {by}={value}: {str(e)}")
            raise
    
    def is_element_present(self, by: By, value: str, timeout: int = 5) -> bool:
        """Check if element is present on the page"""
        try:
            self.find_element(by, value, timeout)
            return True
        except (NoSuchElementException, TimeoutException):
            return False
    
    def is_element_visible(self, by: By, value: str, timeout: int = 5) -> bool:
        """Check if element is visible on the page"""
        try:
            self.wait_for_element_visible(by, value, timeout)
            return True
        except (NoSuchElementException, TimeoutException):
            return False
    
    def scroll_to_element(self, by: By, value: str) -> None:
        """Scroll to a specific element"""
        try:
            element = self.find_element(by, value)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            logger.log_element_action("Scrolled to element", f"{by}={value}")
        except Exception as e:
            logger.error(f"Failed to scroll to element {by}={value}: {str(e)}")
            raise
    
    def get_page_title(self) -> str:
        """Get the current page title"""
        return self.driver.title
    
    def get_current_url(self) -> str:
        """Get the current page URL"""
        return self.driver.current_url
    
    def refresh_page(self) -> None:
        """Refresh the current page"""
        try:
            self.driver.refresh()
            self.wait_for_page_load()
            logger.info("Page refreshed successfully")
        except Exception as e:
            logger.error(f"Failed to refresh page: {str(e)}")
            raise
