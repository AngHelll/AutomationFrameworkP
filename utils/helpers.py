def take_screenshot(driver, test_name):
    """Guarda una captura de pantalla en caso de fallo."""
    driver.save_screenshot(f"reports/{test_name}.png")
