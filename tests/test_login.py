import pytest
from pages.login_page import LoginPage

def test_example_page_loads(driver):
    """Verify the Example Domain page loads successfully."""
    driver.get("https://example.com/")
    example_page = LoginPage(driver)

    assert example_page.is_page_loaded(), "Example Domain page did not load properly."

def test_main_header(driver):
    """Verify the main header text."""
    driver.get("https://example.com/")
    example_page = LoginPage(driver)

    assert "Example Domain" in example_page.get_main_header_text(), "Header text does not match."

def test_paragraph_is_present(driver):
    """Verify the paragraph text is visible."""
    driver.get("https://example.com/")
    example_page = LoginPage(driver)

    assert example_page.is_paragraph_present(), "Paragraph text is not displayed."

def test_more_info_link(driver):
    """Verify that the 'More information...' link is visible."""
    driver.get("https://example.com/")
    example_page = LoginPage(driver)

    assert example_page.is_more_info_link_present(), "More information link not found."
