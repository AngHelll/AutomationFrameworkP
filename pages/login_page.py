from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def is_page_loaded(self):
        """Verify the page title."""
        return "Example Domain" in self.driver.title

    def get_main_header_text(self):
        """Retrieve the main header text."""
        header = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        return header.text

    def is_paragraph_present(self):
        """Check if the paragraph text is displayed."""
        paragraph = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "p")))
        return paragraph.is_displayed()

    def is_more_info_link_present(self):
        """Check if the 'More information...' link is present."""
        return len(self.driver.find_elements(By.LINK_TEXT, "More information...")) > 0
