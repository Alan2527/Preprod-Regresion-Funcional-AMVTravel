import time
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from helpers import safe_click
from pages.webadmin_pais_page import WebAdminPaisPage as P


@allure.feature("WebAdmin AMV Travel")
@allure.story("Ubicación → Países: la tabla trae columnas y filas")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("""
Valida la pantalla Ubicación → Paises (types/country.aspx), de solo lectura:
1. Navegación desde el menú lateral.
2. La grilla `gvCountries` trae TODAS las columnas esperadas.
3. La grilla NO viene vacía (al menos una fila de datos).
4. El buscador está presente.
""")
def test_paises(login_webadmin):
    driver = login_webadmin
    wait = WebDriverWait(driver, 45)

    with allure.step("1. Menú Ubicación → Paises"):
        safe_click(wait, P.MENU_UBICACION)
        time.sleep(1)  # animación del acordeón
        safe_click(wait, P.SUBMENU_PAISES)
        wait.until(EC.url_contains(P.URL))

    with allure.step("2. Validar columnas de la grilla"):
        wait.until(EC.presence_of_element_located(P.TABLA))
        time.sleep(1)  # dar tiempo a que la GridView termine de poblarse
        columnas = [c.get_attribute("textContent").strip()
                    for c in driver.find_elements(*P.HEADERS)
                    if c.get_attribute("textContent").strip()]
        faltantes = [c for c in P.COLUMNAS_ESPERADAS if c not in columnas]
        assert not faltantes, f"Faltan columnas: {faltantes}. Encontradas: {columnas}"
        allure.attach(" | ".join(columnas), "Columnas", allure.attachment_type.TEXT)

    with allure.step("3. Validar que la grilla tiene filas"):
        filas = driver.find_elements(*P.FILAS)
        assert len(filas) > 0, "La grilla de Países vino vacía (sin filas)."
        allure.attach(f"Filas de datos: {len(filas)}", "Filas", allure.attachment_type.TEXT)
        allure.attach(driver.get_screenshot_as_png(), "Grilla_Paises", allure.attachment_type.PNG)

    with allure.step("4. Validar presencia del buscador"):
        assert driver.find_element(*P.TXT_SEARCH).is_displayed(), "No se ve el buscador"
