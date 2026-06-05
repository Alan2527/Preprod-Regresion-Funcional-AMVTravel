"""
Page Object del flujo de Ofertas (Oportunidades) en el sitio público.

Encapsula la pestaña de Ofertas, el ingreso de fecha, los selectores custom
(Tom Select) y las validaciones del acordeón y la tabla final.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class FrontOfertasPage:
    # --- Locators ---
    TAB_OFERTAS = (By.CSS_SELECTOR, "a[href='#tabOpportunity']")
    INPUT_FECHA = (By.ID, "txtOpportunityCalendar")
    BTN_SEARCH = (By.NAME, "ctl00$cphMainSlider$ctl00$ctrlOpportunitySearchControl$btnSearch")
    BTN_NEXT = (By.ID, "ctl00_cphMain_lnkNext")
    ACCORDION = (By.CLASS_NAME, "accordion-content")
    FINAL_TABLES = (By.CSS_SELECTOR, "table.table.table-bordered.table-striped")
    ACCORDION_DEFAULT_IMAGE = (By.XPATH, ".//div[contains(@style, 'no_image_86_0.png')]")
    ACCORDION_H6 = (By.CSS_SELECTOR, "h6.h6style")

    def __init__(self, driver, timeout=15):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.actions = ActionChains(driver)

    def screenshot_png(self):
        return self.driver.get_screenshot_as_png()

    # --- Acciones ---
    def open_tab(self):
        self.wait.until(EC.element_to_be_clickable(self.TAB_OFERTAS)).click()

    def set_date(self, fecha):
        campo = self.wait.until(EC.element_to_be_clickable(self.INPUT_FECHA))
        campo.clear()
        campo.send_keys(fecha)
        # Cerrar el calendario haciendo click fuera (sobre el body).
        body = self.driver.find_element(By.TAG_NAME, "body")
        self.actions.move_to_element_with_offset(body, 0, 0).click().perform()

    def search(self):
        self.wait.until(EC.element_to_be_clickable(self.BTN_SEARCH)).click()

    def select_tomselect(self, parent_class, valor):
        """Interactúa con un selector custom Tom Select, acotado a su contenedor."""
        control = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f".{parent_class} .ts-control")))
        control.click()
        # La espera por la opción clickeable ya cubre el render del dropdown (sin sleep fijo).
        xpath_opcion = f"//div[contains(@class, '{parent_class}')]//div[contains(@class, 'option') and text()='{valor}']"
        self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath_opcion))).click()

    def next_step(self):
        self.wait.until(EC.element_to_be_clickable(self.BTN_NEXT)).click()

    # --- Validaciones ---
    def accordion(self):
        return self.wait.until(EC.presence_of_element_located(self.ACCORDION))

    def accordion_has_default_image(self):
        return len(self.accordion().find_elements(*self.ACCORDION_DEFAULT_IMAGE)) > 0

    def accordion_has_h6(self):
        return len(self.accordion().find_elements(*self.ACCORDION_H6)) > 0

    def final_table_visible(self):
        return self.wait.until(
            lambda d: any(t.is_displayed() for t in d.find_elements(*self.FINAL_TABLES)),
            message="Ninguna tabla de resumen se hizo visible.",
        )
