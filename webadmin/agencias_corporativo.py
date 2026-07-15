import time
import allure
import pytest
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from helpers import safe_click, safe_send_keys
from pages.webadmin_corporativo_page import WebAdminCorporativoPage as P
from pages.webadmin_tour_page import validar_solapas


def _sel_primera(driver, locator):
    els = driver.find_elements(*locator)
    if not els:
        return None
    sel = Select(els[0])
    for o in sel.options:
        if o.get_attribute("value"):
            sel.select_by_value(o.get_attribute("value"))
            return o.text
    return None


@pytest.mark.skip(reason="Flujo de creación de Corporativo roto en el admin (preprod) — pendiente del lado de la app")
@allure.feature("WebAdmin AMV Travel")
@allure.story("Crear Corporativo y validar persistencia")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("""
Crea un Corporativo (Agencias → Corporativo → Nuevo), guarda, valida las solapas
Detalle / Config. de productos, y valida la fila tras volver a la lista.
""")
def test_crear_corporativo(login_webadmin):
    driver = login_webadmin
    wait = WebDriverWait(driver, 45)

    ahora = datetime.now()
    sello = ahora.strftime('%d/%m/%Y %H:%M:%S')
    nombre = f"Corp Test {sello}"
    fecha = ahora.strftime('%d/%m/%Y')
    email = f"corptest{ahora.strftime('%d%m%Y%H%M%S')}@gmail.com"

    with allure.step("1. Menú Agencias → Corporativo → Nuevo"):
        safe_click(wait, P.MENU_AGENCIAS)
        time.sleep(1)
        safe_click(wait, P.SUBMENU_CORPORATIVO)
        wait.until(EC.url_contains("/administration/corporate/corpcompanies.aspx"))
        safe_click(wait, P.BTN_NUEVO)
        wait.until(lambda d: "corpdetail.aspx" in d.current_url.lower())
        wait.until(EC.visibility_of_element_located(P.TXT_NAME))

    with allure.step("2. Cargar el Detalle"):
        safe_send_keys(wait, P.TXT_NAME, nombre)
        safe_send_keys(wait, P.TXT_ADDRESS, "Calle Test 123")
        safe_send_keys(wait, P.TXT_COMMENT, "Test automático")
        safe_send_keys(wait, P.TXT_EMAIL, email)
        safe_send_keys(wait, P.TXT_PHONE, "1122334455")
        safe_send_keys(wait, P.TXT_REWARD, "0")
        _sel_primera(driver, P.DD_MARKET)
        _sel_primera(driver, P.DD_VENDOR)
        _sel_primera(driver, P.DD_CITIES)
        cb = wait.until(EC.presence_of_element_located(P.CB_PUBLICADO))
        if not cb.is_selected():
            driver.execute_script("arguments[0].click();", cb)
        allure.attach(driver.get_screenshot_as_png(), "2_Formulario", allure.attachment_type.PNG)

    with allure.step("3. Guardar"):
        safe_click(wait, P.BTN_GUARDAR)
        time.sleep(2)
        allure.attach(f"URL tras guardar: {driver.current_url}", "3_URL", allure.attachment_type.TEXT)

    with allure.step("4. Validar solapas: Detalle, Config. de productos"):
        validar_solapas(driver, P.TAB_CONTAINER, ["Detalle", "Config. de productos"], P.SOLAPAS)
        allure.attach(driver.get_screenshot_as_png(), "4_Solapas", allure.attachment_type.PNG)

    with allure.step("5. Volver a la lista y validar la fila"):
        base = driver.current_url.split("/administration/")[0]
        driver.get(f"{base}/administration/corporate/corpcompanies.aspx")
        safe_send_keys(wait, P.TXT_SEARCH, f"Corp Test {fecha}")
        safe_click(wait, P.BTN_SEARCH)
        time.sleep(1)
        wait.until(EC.presence_of_element_located(P.TABLA))
        fila = wait.until(EC.presence_of_element_located(P.fila_por_nombre(sello)))
        assert fila is not None, f"El corporativo '{nombre}' no aparece en la tabla."
        allure.attach(driver.get_screenshot_as_png(), "5_Validacion_Tabla", allure.attachment_type.PNG)
