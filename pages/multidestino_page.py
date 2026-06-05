"""
Page Object del flujo de reserva Multidestino (sitio público).
Centraliza selectores del paquete, itinerario, datos de vuelo/pasajero y el
helper de espera de fin de carga.
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MultidestinoPage:
    # --- Navegación / búsqueda ---
    LINK_MULTIDESTINO = (By.XPATH, "//a[@href='/online/tourall.aspx?country=10&city=5000&tour=0&resident=false']")
    INPUT_BUSCADOR = (By.XPATH, "//input[@placeholder='Buscador de paquetes']")
    BTN_BUSCAR = (By.CSS_SELECTOR, "a.pink-btn")

    # --- Resultado ---
    CARD = (By.CSS_SELECTOR, "div.customize-card")
    CARD_IMG = (By.CSS_SELECTOR, "div.customize-image-view")
    CARD_DETALLES = (By.CSS_SELECTOR, "div.tours-details-content-left")
    BTN_COTIZAR = (By.CSS_SELECTOR, "a.update-cart-btn.apreload.pink-btn.custom-tourall-cotization")

    # --- Configuración ---
    INPUT_FECHA = (By.CSS_SELECTOR, "input.coustomtour-form-date")
    DD_PAX = (By.ID, "ctl00_cphMain_ddPax")
    DD_SGL = (By.ID, "ctl00_cphMain_ddSGL")
    DD_DBL = (By.ID, "ctl00_cphMain_ddDBL")
    DD_TPL = (By.CSS_SELECTOR, "select[id$='ddTPL']")
    BTN_CALCULAR = (By.CSS_SELECTOR, "a.pink-btn.apreload")

    # --- Itinerario ---
    SERVICIOS_NO_DISP = (By.XPATH, "//h6[contains(@class, 'serviceTotalh6') and contains(translate(text(), 'NO DISPONIBLE', 'no disponible'), 'no disponible')]")
    BTN_ADD_SERVICIO = (By.ID, "ctl00_cphMain_lvDestinations_ctrl0_lvServicesAdd_ctrl0_lnkAddServiceDefinitivo")
    TABLA_SERVICIOS_AGREGADO = (By.XPATH, '//*[@id="updData"]/div[4]/div[6]/table')
    TERCER_PRECIO = (By.XPATH, "(//h6[contains(@class, 'h6style') and contains(@class, 'serviceTotalh6')])[3]")
    TERCER_IDIOMA = (By.XPATH, "(//select[contains(@id, 'ddServiceLanguage')])[3]")
    BTN_RESERVAR = (By.ID, "ctl00_cphMain_lvTotales_ctrl0_lnkReservar")

    # --- Datos vuelo / pasajero ---
    BTN_SAVE_BOOK = (By.NAME, "ctl00$cphMain$btnSaveBook")
    INPUT_VUELO = (By.XPATH, "//input[contains(@name, 'txtNumFlightData')]")
    INPUT_HORA = (By.XPATH, "//input[contains(@name, 'txtDepartureTimeData')]")
    INPUT_OBS = (By.XPATH, "//input[contains(@name, 'txtCommentData')]")
    INPUT_NOMBRE = (By.XPATH, "//input[contains(@name, 'txtName')]")
    INPUT_APELLIDO = (By.XPATH, "//input[contains(@name, 'txtSurname') or contains(@name, 'txtSurName')]")
    CHK_TERMINOS = (By.ID, "ctl00_cphMain_cbxTermsAndConditions")

    def __init__(self, driver, timeout=20):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def esperar_fin_de_carga(self):
        """Espera a que desaparezcan los modales/loaders de carga."""
        try:
            self.wait.until(EC.invisibility_of_element_located((
                By.XPATH,
                "//*[contains(translate(text(), 'CARGANDO', 'cargando'), 'cargando') "
                "or contains(@class, 'loader') or contains(@class, 'spinner') or @id='UpdateProgress1']"
            )))
            time.sleep(1)  # Breve pausa estabilizadora
        except Exception:
            pass
