import os
import time
from datetime import datetime
from typing import Optional
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from utils.logger import logger
from config.settings import TestSettings

class ScreenshotCapture:
    """Utility class for capturing screenshots during test execution"""
    
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.screenshot_dir = "screenshots"
        self._ensure_screenshot_dir()
    
    def _ensure_screenshot_dir(self):
        """Create screenshot directory if it doesn't exist"""
        if not os.path.exists(self.screenshot_dir):
            os.makedirs(self.screenshot_dir)
            logger.info(f"Created screenshot directory: {self.screenshot_dir}")
    
    def capture_screenshot(self, name: str = None, element: Optional[WebElement] = None) -> str:
        """
        Capture a screenshot of the current page or specific element
        
        Args:
            name: Name for the screenshot file
            element: Specific element to capture (optional)
            
        Returns:
            Path to the captured screenshot file
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{name}_{timestamp}.png" if name else f"screenshot_{timestamp}.png"
            filepath = os.path.join(self.screenshot_dir, filename)
            
            if element:
                # Capture specific element
                self._capture_element_screenshot(element, filepath)
                logger.info(f"Element screenshot captured: {filepath}")
            else:
                # Capture full page
                self.driver.save_screenshot(filepath)
                logger.info(f"Full page screenshot captured: {filepath}")
            
            return filepath
            
        except Exception as e:
            logger.error(f"Failed to capture screenshot: {str(e)}")
            return ""
    
    def _capture_element_screenshot(self, element: WebElement, filepath: str):
        """Capture screenshot of a specific element"""
        try:
            # Scroll element into view
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(0.5)  # Allow scroll to complete
            
            # Get element location and size
            location = element.location
            size = element.size
            
            # Capture full page screenshot first
            temp_screenshot = os.path.join(self.screenshot_dir, "temp_screenshot.png")
            self.driver.save_screenshot(temp_screenshot)
            
            # Crop to element (this is a simplified approach)
            # In production, you might want to use PIL for proper cropping
            self.driver.save_screenshot(filepath)
            
            # Clean up temp file
            if os.path.exists(temp_screenshot):
                os.remove(temp_screenshot)
                
        except Exception as e:
            logger.error(f"Failed to capture element screenshot: {str(e)}")
            # Fallback to full page screenshot
            self.driver.save_screenshot(filepath)
    
    def capture_on_failure(self, test_name: str, error_message: str) -> str:
        """
        Capture screenshot when a test fails
        
        Args:
            test_name: Name of the failing test
            error_message: Error message from the test
            
        Returns:
            Path to the captured screenshot file
        """
        if not TestSettings.SCREENSHOT_ON_FAILURE:
            return ""
        
        try:
            # Clean test name for filename
            clean_test_name = test_name.replace(" ", "_").replace(":", "_")
            filename = f"FAILURE_{clean_test_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            filepath = os.path.join(self.screenshot_dir, filename)
            
            self.driver.save_screenshot(filepath)
            logger.info(f"Failure screenshot captured: {filepath}")
            
            # Log error details
            logger.error(f"Test '{test_name}' failed with error: {error_message}")
            
            return filepath
            
        except Exception as e:
            logger.error(f"Failed to capture failure screenshot: {str(e)}")
            return ""
    
    def capture_before_action(self, action_name: str) -> str:
        """
        Capture screenshot before performing an action
        
        Args:
            action_name: Name of the action being performed
            
        Returns:
            Path to the captured screenshot file
        """
        try:
            filename = f"BEFORE_{action_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            filepath = os.path.join(self.screenshot_dir, filename)
            
            self.driver.save_screenshot(filepath)
            logger.debug(f"Pre-action screenshot captured: {filepath}")
            
            return filepath
            
        except Exception as e:
            logger.error(f"Failed to capture pre-action screenshot: {str(e)}")
            return ""
    
    def capture_after_action(self, action_name: str) -> str:
        """
        Capture screenshot after performing an action
        
        Args:
            action_name: Name of the action that was performed
            
        Returns:
            Path to the captured screenshot file
        """
        try:
            filename = f"AFTER_{action_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            filepath = os.path.join(self.screenshot_dir, filename)
            
            self.driver.save_screenshot(filepath)
            logger.debug(f"Post-action screenshot captured: {filepath}")
            
            return filepath
            
        except Exception as e:
            logger.error(f"Failed to capture post-action screenshot: {str(e)}")
            return ""
