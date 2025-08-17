from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.settings import TestSettings
import logging

logger = logging.getLogger(__name__)

class GitHubCLIPage(BasePage):
    """Page Object for GitHub CLI page"""
    
    # Page locators - centralized for easy maintenance
    LOCATORS = {
        'main_header': (By.TAG_NAME, "h1"),
        'download_windows_button': (By.LINK_TEXT, "Download for Windows"),
        'download_mac_button': (By.LINK_TEXT, "Download for macOS"),
        'download_linux_button': (By.LINK_TEXT, "Download for Linux"),
        'install_instructions': (By.CLASS_NAME, "install-instructions"),
        'cli_documentation': (By.LINK_TEXT, "Documentation"),
        'github_repo_link': (By.LINK_TEXT, "GitHub"),
        'search_box': (By.NAME, "q"),
        'navigation_menu': (By.TAG_NAME, "nav"),  # Changed from class to tag
        'hero_section': (By.TAG_NAME, "header"),  # Changed from class to tag
        'feature_list': (By.CLASS_NAME, "features")
    }
    
    def _get_page_url(self) -> str:
        """Return the GitHub CLI page URL"""
        return TestSettings.get_urls()["github_cli"]
    
    def is_page_loaded(self) -> bool:
        """Verify the GitHub CLI page has loaded correctly"""
        try:
            # Check page title
            title_contains_cli = "GitHub CLI" in self.get_page_title()
            
            # Check if main header is present and visible
            header_visible = self.is_element_visible(*self.LOCATORS['main_header'])
            
            # Check if at least one download button is present (Windows button exists)
            download_button_present = self.is_element_present(*self.LOCATORS['download_windows_button'])
            
            # Check if navigation is present
            nav_present = self.is_element_present(*self.LOCATORS['navigation_menu'])
            
            return title_contains_cli and header_visible and download_button_present and nav_present
            
        except Exception as e:
            logger.error(f"Failed to verify page load: {str(e)}")
            return False
    
    def get_main_header_text(self) -> str:
        """Get the main header text from the page"""
        try:
            return self.get_element_text(*self.LOCATORS['main_header'])
        except Exception as e:
            logger.error(f"Failed to get main header text: {str(e)}")
            raise
    
    def is_download_button_present(self, platform: str = "windows") -> bool:
        """
        Check if the download button for a specific platform is present
        
        Args:
            platform: Platform to check (windows, mac, linux)
            
        Returns:
            True if button is present and visible, False otherwise
        """
        try:
            platform_locators = {
                "windows": self.LOCATORS['download_windows_button'],
                "mac": self.LOCATORS['download_mac_button'],
                "linux": self.LOCATORS['download_linux_button']
            }
            
            if platform not in platform_locators:
                logger.warning(f"Unsupported platform: {platform}")
                return False
            
            locator = platform_locators[platform]
            return self.is_element_visible(*locator)
            
        except Exception as e:
            logger.error(f"Failed to check download button for {platform}: {str(e)}")
            return False
    
    def click_download_button(self, platform: str = "windows") -> bool:
        """
        Click the download button for a specific platform
        
        Args:
            platform: Platform to download for (windows, mac, linux)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            platform_locators = {
                "windows": self.LOCATORS['download_windows_button'],
                "mac": self.LOCATORS['download_mac_button'],
                "linux": self.LOCATORS['download_linux_button']
            }
            
            if platform not in platform_locators:
                logger.warning(f"Unsupported platform: {platform}")
                return False
            
            locator = platform_locators[platform]
            self.click_element(*locator)
            logger.info(f"Successfully clicked download button for {platform}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to click download button for {platform}: {str(e)}")
            return False
    
    def get_install_instructions(self) -> str:
        """Get the installation instructions text"""
        try:
            if self.is_element_present(*self.LOCATORS['install_instructions']):
                return self.get_element_text(*self.LOCATORS['install_instructions'])
            return ""
        except Exception as e:
            logger.error(f"Failed to get install instructions: {str(e)}")
            return ""
    
    def navigate_to_documentation(self) -> bool:
        """Navigate to the CLI documentation page"""
        try:
            self.click_element(*self.LOCATORS['cli_documentation'])
            logger.info("Successfully navigated to CLI documentation")
            return True
        except Exception as e:
            logger.error(f"Failed to navigate to documentation: {str(e)}")
            return False
    
    def search_for_content(self, query: str) -> bool:
        """
        Search for content using the search box
        
        Args:
            query: Search query string
            
        Returns:
            True if search was successful, False otherwise
        """
        try:
            if self.is_element_present(*self.LOCATORS['search_box']):
                self.input_text(*self.LOCATORS['search_box'], query)
                logger.info(f"Successfully searched for: {query}")
                return True
            else:
                logger.warning("Search box not found on page")
                return False
        except Exception as e:
            logger.error(f"Failed to search for content: {str(e)}")
            return False
    
    def get_feature_list(self) -> list:
        """Get list of features displayed on the page"""
        try:
            if self.is_element_present(*self.LOCATORS['feature_list']):
                feature_elements = self.find_elements(*self.LOCATORS['feature_list'])
                features = [elem.text for elem in feature_elements if elem.text.strip()]
                logger.info(f"Found {len(features)} features on the page")
                return features
            return []
        except Exception as e:
            logger.error(f"Failed to get feature list: {str(e)}")
            return []
    
    def is_navigation_menu_visible(self) -> bool:
        """Check if the navigation menu is visible"""
        try:
            return self.is_element_visible(*self.LOCATORS['navigation_menu'])
        except Exception as e:
            logger.error(f"Failed to check navigation menu visibility: {str(e)}")
            return False
    
    def wait_for_page_elements(self, timeout: int = None) -> bool:
        """
        Wait for all critical page elements to be loaded
        
        Args:
            timeout: Custom timeout in seconds
            
        Returns:
            True if all elements are loaded, False otherwise
        """
        try:
            timeout = timeout or TestSettings.EXPLICIT_WAIT
            
            # Wait for main header
            self.wait_for_element_visible(*self.LOCATORS['main_header'], timeout)
            
            # Wait for navigation (header)
            self.wait_for_element_visible(*self.LOCATORS['navigation_menu'], timeout)
            
            # Wait for at least one download button (Windows button exists)
            windows_button = self.is_element_present(*self.LOCATORS['download_windows_button'], 5)
            
            if windows_button:
                logger.info("All critical page elements loaded successfully")
                return True
            else:
                logger.warning("Download button not found after timeout")
                return False
                
        except Exception as e:
            logger.error(f"Failed to wait for page elements: {str(e)}")
            return False