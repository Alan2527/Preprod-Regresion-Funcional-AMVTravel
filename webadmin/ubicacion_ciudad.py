import time
import allure
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from helpers import safe_click, safe_send_keys
from pages.ubicacion_helpers import seleccionar
from pages.webadmin_city_page import WebAdminCityPage as P


@allure.feature("WebAdmin AMV Travel")
@allure.story("Ubicación → Crear Ciudad y validar persistencia")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("""
Crea una Ciudad (cities/detail.aspx): Nombre dinámico + País + Orden + Publicado →
Guardar → buscar y validar la fila por el sello.
""")
def test_crear_ciudad(login_webadmin):
    driver = login_webadmin
    wait = WebDriverWait(driver, 45)

    ahora = datetime.now()
    sello = ahora.strftime('%d/%m/%Y %H:%M:%S')
    PREFIJO = "Ciudad Test"
    nombre = f"{PREFIJO} {sello}"

    with allure.step("1. Menú Ubicación → Ciudades"):
        safe_click(wait, P.MENU_UBICACION)
        time.sleep(1)
        safe_click(wait, P.SUBMENU)
        wait.until(EC.url_contains(P.URL_LISTA))

    with allure.step("2. 'Crear Ciudad' → detail"):
        safe_click(wait, P.BTN_NUEVO)
        wait.until(EC.url_contains(P.URL_DETALLE))
        wait.until(EC.visibility_of_element_located(P.TXT_NAME))

    with allure.step("3. Nombre + País + Orden + Publicado"):
        safe_send_keys(wait, P.TXT_NAME, nombre)
        pais = seleccionar(driver, wait, P.DD_PAIS, "Argentina", postback=True)
        safe_send_keys(wait, P.TXT_ORDEN, "1")
        cb = wait.until(EC.presence_of_element_located(P.CB_PUBLICADO))
        if not cb.is_selected():
            driver.execute_script("arguments[0].click();", cb)
        allure.attach(f"País elegido: {pais}", "3_Pais", allure.attachment_type.TEXT)
        allure.attach(driver.get_screenshot_as_png(), "3_Form", allure.attachment_type.PNG)

    with allure.step("4. Guardar"):
        safe_click(wait, P.BTN_GUARDAR)
        time.sleep(1)

    with allure.step("5. Volver a la lista, buscar y validar la fila"):
        origin = driver.current_url.split("/administration/")[0]
        driver.get(origin + P.URL_LISTA)
        safe_send_keys(wait, P.TXT_SEARCH, f"{PREFIJO} {ahora.strftime('%d/%m/%Y')}")
        safe_click(wait, P.BTN_SEARCH)
        time.sleep(1)
        wait.until(EC.presence_of_element_located(P.TABLA))
        fila = wait.until(EC.presence_of_element_located(P.fila_por_nombre(sello)))
        assert fila is not None, f"La Ciudad '{nombre}' no aparece en la tabla."
        allure.attach(driver.get_screenshot_as_png(), "5_Validacion", allure.attachment_type.PNG)
