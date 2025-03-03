from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class GitHubCLIPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)  # Wait for elements to load

    def is_page_loaded(self):
        """Verify the page title"""
        return "GitHub CLI" in self.driver.title

    def get_main_header_text(self):
        """Get the main header text from the page"""
        header = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        return header.text

    def is_download_button_present(self):
        """Check if the 'Download for Windows' button is present"""
        try:
            self.wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Download for Windows")))
            return True
        except:
            return False