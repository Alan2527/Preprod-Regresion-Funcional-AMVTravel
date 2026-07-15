import time
import allure
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from helpers import safe_click, safe_send_keys
from pages.ubicacion_helpers import seleccionar
from pages.webadmin_district_page import WebAdminDistrictPage as P


@allure.feature("WebAdmin AMV Travel")
@allure.story("Ubicación → Crear Barrio (modal) y validar persistencia")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("""
Crea un Barrio desde el WebAdmin (types/districts.aspx): "Crear Barrio" abre un MODAL
→ Nombre dinámico + Ciudad → Guardar → buscar y validar la fila por el sello.
""")
def test_crear_barrio(login_webadmin):
    driver = login_webadmin
    wait = WebDriverWait(driver, 45)

    ahora = datetime.now()
    sello = ahora.strftime('%d/%m/%Y %H:%M:%S')
    PREFIJO = "Barrio Test"
    nombre = f"{PREFIJO} {sello}"

    with allure.step("1. Menú Ubicación → Barrios"):
        safe_click(wait, P.MENU_UBICACION)
        time.sleep(1)
        safe_click(wait, P.SUBMENU)
        wait.until(EC.url_contains(P.URL_LISTA))

    with allure.step("2. 'Crear Barrio' → abre el modal"):
        safe_click(wait, P.BTN_NUEVO)
        wait.until(EC.visibility_of_element_located(P.TXT_NAME))

    with allure.step("3. Nombre + Ciudad en el modal"):
        safe_send_keys(wait, P.TXT_NAME, nombre)
        ciudad = seleccionar(driver, wait, P.DD_CIUDAD)  # primera ciudad real
        allure.attach(f"Ciudad elegida: {ciudad}", "3_Ciudad", allure.attachment_type.TEXT)
        allure.attach(driver.get_screenshot_as_png(), "3_Modal", allure.attachment_type.PNG)

    with allure.step("4. Guardar"):
        safe_click(wait, P.BTN_GUARDAR)
        time.sleep(1)  # postback de guardado (recarga la lista)

    with allure.step("5. Buscar y validar la fila por el sello"):
        # Gotcha #1: buscar por nombre SIN la hora.
        safe_send_keys(wait, P.TXT_SEARCH, f"{PREFIJO} {ahora.strftime('%d/%m/%Y')}")
        safe_click(wait, P.BTN_SEARCH)
        time.sleep(1)
        wait.until(EC.presence_of_element_located(P.TABLA))
        fila = wait.until(EC.presence_of_element_located(P.fila_por_nombre(sello)))
        assert fila is not None, f"El Barrio '{nombre}' no aparece en la tabla."
        allure.attach(driver.get_screenshot_as_png(), "5_Validacion", allure.attachment_type.PNG)
