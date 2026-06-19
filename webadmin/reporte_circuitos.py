import time
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from helpers import safe_click
from pages.webadmin_reporte_circuitos_page import WebAdminReporteCircuitosPage as P


@allure.feature("WebAdmin AMV Travel")
@allure.story("Reporte de Circuitos: validar que la tabla tiene contenido")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("""
Valida el Reporte de Circuitos (Circuitos → Reporte Circuitos):
1. Navegación al reporte.
2. La tabla principal existe y NO viene vacía (tiene al menos una fila de datos).
""")
def test_reporte_circuitos(login_webadmin):
    driver = login_webadmin
    wait = WebDriverWait(driver, 45)

    with allure.step("1. Menú Circuitos → Reporte Circuitos"):
        safe_click(wait, P.MENU_CIRCUITOS)
        time.sleep(1)
        safe_click(wait, P.SUBMENU_REPORTE)
        wait.until(EC.url_contains("/administration/customtours/"))

    with allure.step("2. Validar que la tabla principal tiene contenido"):
        wait.until(EC.presence_of_element_located(P.TABLA))
        time.sleep(1)  # dar tiempo a que la grilla termine de poblarse
        filas = driver.find_elements(*P.FILAS)
        assert len(filas) > 0, "La tabla del Reporte de Circuitos vino vacía (sin filas)."
        allure.attach(f"Filas en el reporte: {len(filas)}", "2_Filas", allure.attachment_type.TEXT)
        allure.attach(driver.get_screenshot_as_png(), "2_Reporte_Tabla", allure.attachment_type.PNG)
