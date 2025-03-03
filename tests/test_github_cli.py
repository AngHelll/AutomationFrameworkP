import pytest
from pages.github_cli_page import GitHubCLIPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_github_cli_page_loads(driver):
    """Verify GitHub CLI page loads successfully"""
    driver.get("https://cli.github.com/")

    # Explicit wait to ensure the page is fully loaded
    WebDriverWait(driver, 10).until(EC.title_contains("GitHub CLI"))

    github_page = GitHubCLIPage(driver)

    assert github_page.is_page_loaded(), "GitHub CLI page did not load properly."

def test_main_header(driver):
    """Verify the main header text"""
    driver.get("https://cli.github.com/")
    github_page = GitHubCLIPage(driver)

    assert "Take GitHub to the command line" in github_page.get_main_header_text(), "Header text does not match."

def test_download_button_presence(driver):
    """Verify that the download button is visible"""
    driver.get("https://cli.github.com/")
    github_page = GitHubCLIPage(driver)

    assert github_page.is_download_button_present(), "Download button not found."
