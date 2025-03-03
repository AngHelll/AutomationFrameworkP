import pytest
from config.browser_setup import get_driver

def pytest_addoption(parser):
    """Permite seleccionar el navegador desde la línea de comandos."""
    parser.addoption("--browser", action="store", default="chrome", help="Navegador a utilizar")

@pytest.fixture
def driver(request):
    """Fixture para inicializar y cerrar el WebDriver."""
    browser = request.config.getoption("--browser")
    driver = get_driver(browser)
    driver.get("https://example.com/login")  # URL de prueba
    yield driver
    driver.quit()
