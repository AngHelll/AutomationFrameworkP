import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage  # Creamos esta clase para verificar el Dashboard

@pytest.mark.parametrize("username, password", [
    ("admin", "admin123"),  # Caso válido con Admin
    ("user1", "user123"),   # Caso válido con otro usuario
    ("testuser", "testpass") # Otro usuario válido
])
def test_login_success(driver, username, password):
    """Prueba de login exitoso con diferentes usuarios válidos."""
    login_page = LoginPage(driver)
    login_page.login(username, password)

    dashboard_page = DashboardPage(driver)
    assert dashboard_page.is_dashboard_loaded(), "El Dashboard no se cargó correctamente."

@pytest.mark.parametrize("username, password", [
    ("user", "wrongpass"),  # Contraseña incorrecta
    ("", "admin123"),       # Usuario vacío
    ("admin", ""),          # Contraseña vacía
])
def test_login_failure(driver, username, password):
    """Prueba diferentes combinaciones de login fallidas."""
    login_page = LoginPage(driver)
    login_page.login(username, password)

    error_message = driver.find_element(*login_page.error_message).text
    assert "Invalid credentials" in error_message, "No se mostró el mensaje de error esperado."
