import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

@pytest.mark.parametrize("username, password", [
    ("admin", "admin123"),
    ("user1", "user123"),
    ("testuser", "testpass")
])
def test_login_success(driver, username, password):
    """Test successful login with multiple users."""
    login_page = LoginPage(driver)
    login_page.login(username, password)

    dashboard_page = DashboardPage(driver)
    assert dashboard_page.is_dashboard_loaded(), "Dashboard did not load correctly."

@pytest.mark.parametrize("username, password", [
    ("user", "wrongpass"),
    ("", "admin123"),
    ("admin", "")
])
def test_login_failure(driver, username, password):
    """Test login failure scenarios."""
    login_page = LoginPage(driver)
    login_page.login(username, password)

    error_message = driver.find_element(*login_page.error_message).text
    assert "Invalid credentials" in error_message, "Expected error message not displayed."
