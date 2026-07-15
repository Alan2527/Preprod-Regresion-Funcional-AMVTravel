import time
import allure
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from helpers import safe_click, safe_send_keys
from pages.ubicacion_helpers import seleccionar
from pages.webadmin_tour_page import escribir_quill
from pages.webadmin_restaurant_page import WebAdminRestaurantPage as P


@allure.feature("WebAdmin AMV Travel")
@allure.story("Ubicación → Crear Restaurante y validar persistencia")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("""
Crea un Restaurante (restaurants/detail.aspx): Nombre dinámico + Ciudad (postback) +
Orden + Nombre/Descripción ES (Quill) + Publicado → Guardar → buscar y validar la
fila por el sello.
⚠ Best-effort: ddCity tiene ~700 opciones y dispara postback; probable iteración.
""")
def test_crear_restaurante(login_webadmin):
    driver = login_webadmin
    wait = WebDriverWait(driver, 45)

    ahora = datetime.now()
    sello = ahora.strftime('%d/%m/%Y %H:%M:%S')
    PREFIJO = "Restaurante Test"
    nombre = f"{PREFIJO} {sello}"

    with allure.step("1. Menú Ubicación → Restaurantes"):
        safe_click(wait, P.MENU_UBICACION)
        time.sleep(1)
        safe_click(wait, P.SUBMENU)
        wait.until(EC.url_contains(P.URL_LISTA))

    with allure.step("2. '+ Agregar Nuevo' → detail"):
        safe_click(wait, P.BTN_NUEVO)
        wait.until(EC.url_contains(P.URL_DETALLE))
        wait.until(EC.visibility_of_element_located(P.TXT_NAME))

    with allure.step("3. Nombre + Ciudad (postback) + Orden + Nombre/Desc ES + Publicado"):
        safe_send_keys(wait, P.TXT_NAME, nombre)
        ciudad = seleccionar(driver, wait, P.DD_CIUDAD, "Cachi", postback=True)
        safe_send_keys(wait, P.TXT_ORDEN, "1")
        safe_send_keys(wait, P.NOMBRE_ES, nombre)
        escribir_quill(driver, wait, P.QUILL_ES, "Test automático")
        cb = wait.until(EC.presence_of_element_located(P.CB_PUBLICADO))
        if not cb.is_selected():
            driver.execute_script("arguments[0].click();", cb)
        allure.attach(f"Ciudad elegida: {ciudad}", "3_Ciudad", allure.attachment_type.TEXT)
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
        assert fila is not None, f"El Restaurante '{nombre}' no aparece en la tabla."
        allure.attach(driver.get_screenshot_as_png(), "5_Validacion", allure.attachment_type.PNG)
