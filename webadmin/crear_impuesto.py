import time
import allure
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from helpers import safe_click, safe_send_keys
from pages.webadmin_tax_page import WebAdminTaxPage as P


@allure.feature("WebAdmin AMV Travel")
@allure.story("Finanzas → Crear Impuesto (general) y validar persistencia")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("""
Crea un Impuesto general (Taxes.aspx): "Nuevo" abre un MODAL → Nombre dinámico +
Orden + Valor → Guardar → volver y validar la fila en gvTaxes por el sello.
""")
def test_crear_impuesto(login_webadmin):
    driver = login_webadmin
    wait = WebDriverWait(driver, 45)

    ahora = datetime.now()
    sello = ahora.strftime('%d/%m/%Y %H:%M:%S')
    PREFIJO = "Impuesto Test"
    nombre = f"{PREFIJO} {sello}"

    with allure.step("1. Menú Finanzas → Impuestos"):
        safe_click(wait, P.MENU_FINANZAS)
        time.sleep(1)
        safe_click(wait, P.SUBMENU)
        wait.until(EC.url_contains(P.URL_LISTA))

    with allure.step("2. 'Nuevo' → abre el modal"):
        safe_click(wait, P.BTN_NUEVO)
        wait.until(EC.visibility_of_element_located(P.TXT_NAME))

    with allure.step("3. Nombre + Orden + Valor"):
        safe_send_keys(wait, P.TXT_NAME, nombre)
        safe_send_keys(wait, P.TXT_ORDEN, "1")
        safe_send_keys(wait, P.TXT_VALOR, "0")
        allure.attach(driver.get_screenshot_as_png(), "3_Modal", allure.attachment_type.PNG)

    with allure.step("4. Guardar"):
        safe_click(wait, P.BTN_GUARDAR)
        time.sleep(1)

    with allure.step("5. Volver y validar la fila en gvTaxes por el sello"):
        origin = driver.current_url.split("/administration/")[0]
        driver.get(origin + P.URL_LISTA)
        wait.until(EC.presence_of_element_located(P.TABLA))
        time.sleep(1)
        fila = wait.until(EC.presence_of_element_located(P.fila_por_nombre(sello)))
        assert fila is not None, f"El Impuesto '{nombre}' no aparece en la tabla."
        allure.attach(driver.get_screenshot_as_png(), "5_Validacion", allure.attachment_type.PNG)
