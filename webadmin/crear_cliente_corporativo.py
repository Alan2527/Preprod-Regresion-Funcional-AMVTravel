import time
import allure
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from helpers import safe_click, safe_send_keys
from pages.webadmin_cliente_corporativo_page import WebAdminClienteCorporativoPage as P


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


def _sel_texto(driver, locator, texto):
    els = driver.find_elements(*locator)
    if els:
        try:
            Select(els[0]).select_by_visible_text(texto)
        except Exception:
            _sel_primera(driver, locator)


@allure.feature("WebAdmin AMV Travel")
@allure.story("Crear Cliente Corporativo y validar persistencia")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("""
Crea un Cliente Corporativo (Agencias → Clientes Corporativos → Nuevo), guarda y valida
la fila tras volver a la lista.
""")
def test_crear_cliente_corporativo(login_webadmin):
    driver = login_webadmin
    wait = WebDriverWait(driver, 45)

    ahora = datetime.now()
    sello = ahora.strftime('%d/%m/%Y %H:%M:%S')
    nombre = f"CliCorp Test {sello}"
    fecha = ahora.strftime('%d/%m/%Y')
    stamp = ahora.strftime('%d%m%Y%H%M%S')
    email = f"clicorptest{stamp}@gmail.com"

    with allure.step("1. Menú Agencias → Clientes Corporativos → Nuevo"):
        safe_click(wait, P.MENU_AGENCIAS)
        time.sleep(1)
        safe_click(wait, P.SUBMENU_CLIENTES_CORP)
        wait.until(EC.url_contains("/administration/corporate/corpcustomers.aspx"))
        safe_click(wait, P.BTN_NUEVO)
        wait.until(lambda d: "corpcustomerdetail.aspx" in d.current_url.lower())
        wait.until(EC.visibility_of_element_located(P.TXT_NAME))

    with allure.step("2. Cargar el form"):
        safe_send_keys(wait, P.TXT_NAME, nombre)
        safe_send_keys(wait, P.TXT_LASTNAME, "Automatico")
        safe_send_keys(wait, P.TXT_EMAIL, email)
        safe_send_keys(wait, P.TXT_USERNAME, f"clicorp{stamp}")
        safe_send_keys(wait, P.TXT_PASS, "SanJuan28@G")
        _sel_primera(driver, P.DD_CORP)
        _sel_texto(driver, P.DD_USERTYPE, "Cliente")
        _sel_texto(driver, P.DD_CURRENCY, "Dollar")
        cb = wait.until(EC.presence_of_element_located(P.CB_PUBLICADO))
        if not cb.is_selected():
            driver.execute_script("arguments[0].click();", cb)
        allure.attach(driver.get_screenshot_as_png(), "2_Formulario", allure.attachment_type.PNG)

    with allure.step("3. Guardar"):
        safe_click(wait, P.BTN_GUARDAR)
        time.sleep(2)

    with allure.step("4. Volver a la lista y validar la fila"):
        base = driver.current_url.split("/administration/")[0]
        driver.get(f"{base}/administration/corporate/corpcustomers.aspx")
        safe_send_keys(wait, P.TXT_SEARCH, f"CliCorp Test {fecha}")
        safe_click(wait, P.BTN_SEARCH)
        time.sleep(1)
        wait.until(EC.presence_of_element_located(P.TABLA))
        fila = wait.until(EC.presence_of_element_located(P.fila_por_nombre(sello)))
        assert fila is not None, f"El cliente corporativo '{nombre}' no aparece en la tabla."
        allure.attach(driver.get_screenshot_as_png(), "4_Validacion_Tabla", allure.attachment_type.PNG)
