"""
Page Object de la pantalla de inicio del WebAdmin (/administration/).

Centraliza los selectores y expone métodos legibles para que el test no dependa
de los detalles del DOM. Si la UI cambia, se ajusta acá (un solo lugar) y no en
cada test.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WebAdminHomePage:
    # --- Locators ---
    SIDEBAR = (By.CSS_SELECTOR, "div.admin-sidebar")
    AGENCY_NAME = (By.CSS_SELECTOR, "span.agency-name")
    MENU = (By.CSS_SELECTOR, "ul#ctl00_ctrlMenu.sf-menu")
    USER_PROFILE = (By.CSS_SELECTOR, "div.sidebar-user-profile")
    USER_NAME = (By.CSS_SELECTOR, "span.user-name")
    USER_EMAIL = (By.CSS_SELECTOR, "span.user-email")
    QA_BADGE = (By.CSS_SELECTOR, "span.qa-badge")
    BOOKINGS_TABLE = (By.CSS_SELECTOR, "table#ctl00_cph1_gvBooks")
    BOOKINGS_ROWS = (By.CSS_SELECTOR, "tr.rowstyle, tr.altrowstyle")
    LOGOUT_BTN = (By.CSS_SELECTOR, "a.sidebar-logout-btn")

    def __init__(self, driver, timeout=45):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # --- Helpers internos ---
    def _text(self, locator):
        """Lee el textContent (DOM renderizado) sin depender del viewport."""
        return self.driver.find_element(*locator).get_attribute("textContent").strip()

    # --- Accesos / datos ---
    @property
    def current_url(self):
        return self.driver.current_url

    def screenshot_png(self):
        return self.driver.get_screenshot_as_png()

    def sidebar(self):
        return self.wait.until(EC.visibility_of_element_located(self.SIDEBAR))

    def agency_name(self):
        self.sidebar()
        return self._text(self.AGENCY_NAME)

    def menu_items(self):
        menu = self.wait.until(EC.visibility_of_element_located(self.MENU))
        return [s.get_attribute("textContent").strip() for s in menu.find_elements(By.TAG_NAME, "span")]

    def user_name(self):
        self.wait.until(EC.visibility_of_element_located(self.USER_PROFILE))
        return self._text(self.USER_NAME)

    def user_email(self):
        return self._text(self.USER_EMAIL)

    def qa_badge_text(self):
        return self.wait.until(EC.visibility_of_element_located(self.QA_BADGE)).get_attribute("textContent").strip()

    def bookings_rows(self):
        table = self.wait.until(EC.visibility_of_element_located(self.BOOKINGS_TABLE))
        return table.find_elements(*self.BOOKINGS_ROWS)

    def logout_href(self):
        return self.wait.until(EC.presence_of_element_located(self.LOGOUT_BTN)).get_attribute("href")
