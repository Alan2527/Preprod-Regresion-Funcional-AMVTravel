"""
Page Object de la Bandeja de Entrada (Inbox) de Reservas del BackOffice.

Lo comparten los tests que validan la estructura del inbox (cotizaciones y
reservas), que solo difieren en la URL del inbox a abrir.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BoBookingInboxPage:
    # --- Locators ---
    MENU_RESERVAS = (By.XPATH, "//span[contains(text(), 'Reservas')]")

    # Componentes estructurales esperados en la pantalla del inbox.
    COMPONENTS = {
        "Título de página (page-title)": (By.CLASS_NAME, "page-title"),
        "Tarjeta principal (card bg-white)": (By.CSS_SELECTOR, "div.card.bg-white"),
        "Encabezado de tarjeta (card-header)": (By.CLASS_NAME, "card-header"),
        "Cuerpo de tarjeta (card-block)": (By.CLASS_NAME, "card-block"),
    }

    def __init__(self, driver, timeout=15):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def screenshot_png(self):
        return self.driver.get_screenshot_as_png()

    def open_menu_reservas(self):
        self.wait.until(EC.element_to_be_clickable(self.MENU_RESERVAS)).click()

    def open_inbox(self, inbox_url):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//a[@href='{inbox_url}']"))).click()

    def find_component(self, locator):
        """Devuelve el elemento si está presente (espera explícita); si no, lanza."""
        return self.wait.until(EC.presence_of_element_located(locator))
