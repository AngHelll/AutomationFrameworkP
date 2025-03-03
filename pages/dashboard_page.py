from selenium.webdriver.common.by import By

class DashboardPage:
    def __init__(self, driver):
        self.driver = driver
        self.welcome_message = (By.ID, "welcome")  # Supongamos que hay un mensaje de bienvenida en el dashboard

    def is_dashboard_loaded(self):
        """Verifica si el Dashboard cargó correctamente tras el login."""
        return len(self.driver.find_elements(*self.welcome_message)) > 0
