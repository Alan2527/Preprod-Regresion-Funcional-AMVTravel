import time
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from helpers import safe_click
from pages.webadmin_reservas_page import WebAdminReservasPage as P


def _leer_columnas(driver):
    """Devuelve los textos (trim) de la fila de encabezado de la grilla."""
    celdas = driver.find_elements(*P.HEADERS)
    return [c.get_attribute("textContent").strip() for c in celdas if c.get_attribute("textContent").strip()]


def _validar_grilla(driver, wait):
    """Valida que la grilla exista, traiga las columnas esperadas y tenga filas."""
    # gotcha #2: la grilla va envuelta por JS → usar presence (no visibility).
    wait.until(EC.presence_of_element_located(P.TABLA))
    time.sleep(1)  # dar tiempo a que la GridView termine de poblarse

    columnas = _leer_columnas(driver)
    faltantes = [c for c in P.COLUMNAS_ESPERADAS if c not in columnas]
    assert not faltantes, f"Faltan columnas en la grilla: {faltantes}. Encontradas: {columnas}"

    filas = driver.find_elements(*P.FILAS)
    assert len(filas) > 0, "La grilla de reservas vino vacía (sin filas)."

    allure.attach(" | ".join(columnas), "Columnas", allure.attachment_type.TEXT)
    allure.attach(f"Filas de datos: {len(filas)}", "Filas", allure.attachment_type.TEXT)
    allure.attach(driver.get_screenshot_as_png(), "Grilla", allure.attachment_type.PNG)
    return filas


@allure.feature("WebAdmin AMV Travel")
@allure.story("Reservas: Adm. de Reservas trae columnas y filas")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("""
Valida la pantalla Reservas → Adm. de Reservas (booking/default.aspx):
1. Navegación desde el menú lateral.
2. La grilla `gvBooks` trae TODAS las columnas esperadas.
3. La grilla NO viene vacía (al menos una fila de datos).
4. Los controles de filtro por rango de fechas están presentes.
""")
def test_reservas_admin(login_webadmin):
    driver = login_webadmin
    wait = WebDriverWait(driver, 45)

    with allure.step("1. Menú Reservas → Adm. de Reservas"):
        safe_click(wait, P.MENU_RESERVAS)
        time.sleep(1)  # animación del acordeón
        safe_click(wait, P.SUBMENU_ADM)
        wait.until(EC.url_contains(P.URL_ADM))

    with allure.step("2. Validar columnas y contenido de la grilla"):
        _validar_grilla(driver, wait)

    with allure.step("3. Validar controles de filtro por rango de fechas"):
        assert driver.find_element(*P.FILTRO_DESDE).is_displayed(), "No se ve el filtro 'Desde'"
        assert driver.find_element(*P.FILTRO_HASTA).is_displayed(), "No se ve el filtro 'Hasta'"
        assert driver.find_element(*P.BTN_FILTRAR).is_displayed(), "No se ve el botón 'Filtrar'"


@allure.feature("WebAdmin AMV Travel")
@allure.story("Reservas: Canceladas trae columnas y filas")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("""
Valida la pantalla Reservas → Canceladas (booking/defaultcancel.aspx):
1. Navegación desde el menú lateral.
2. La grilla `gvBooks` trae TODAS las columnas esperadas.
3. La grilla NO viene vacía (al menos una fila de datos).
""")
def test_reservas_canceladas(login_webadmin):
    driver = login_webadmin
    wait = WebDriverWait(driver, 45)

    with allure.step("1. Menú Reservas → Canceladas"):
        safe_click(wait, P.MENU_RESERVAS)
        time.sleep(1)  # animación del acordeón
        safe_click(wait, P.SUBMENU_CANCELADAS)
        wait.until(EC.url_contains(P.URL_CANCELADAS))

    with allure.step("2. Validar columnas y contenido de la grilla"):
        _validar_grilla(driver, wait)
