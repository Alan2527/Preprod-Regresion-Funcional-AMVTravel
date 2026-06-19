import time
import allure
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from helpers import safe_click, safe_send_keys
from pages.webadmin_agencia_page import WebAdminAgenciaPage as A
from pages.webadmin_usuario_page import WebAdminUsuarioPage as U
from pages.webadmin_tour_page import escribir_quill


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
            return
        except Exception:
            _sel_primera(driver, locator)


def _check(driver, wait, locator, on=True):
    cb = wait.until(EC.presence_of_element_located(locator))
    if cb.is_selected() != on:
        driver.execute_script("arguments[0].click();", cb)


@allure.feature("WebAdmin AMV Travel")
@allure.story("Crear Agencia (2 pasos) y validar persistencia")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("""
Crea una Agencia (Agencias → Adm. de Agencias → Crear agencia): llena el form de agencia,
guarda, confirma el modal con "Sí", llena el form del usuario admin, guarda, y valida la
agencia en la tabla.
⚠ Flujo de 2 pasos con modales (best-effort): el modal "Sí" se ubica por texto y puede
requerir ajustes según el comportamiento real.
""")
def test_crear_agencia(login_webadmin):
    driver = login_webadmin
    wait = WebDriverWait(driver, 45)

    ahora = datetime.now()
    sello = ahora.strftime('%d/%m/%Y %H:%M:%S')
    stamp = ahora.strftime('%d%m%Y%H%M%S')
    nombre = f"Agencia Test {sello}"
    fecha = ahora.strftime('%d/%m/%Y')
    email = f"agentest{stamp}@gmail.com"

    # ── PASO 1: form de Agencia ───────────────────────────────────────────────
    with allure.step("1. Menú Agencias → Adm. de Agencias → Crear agencia"):
        safe_click(wait, A.MENU_AGENCIAS)
        time.sleep(1)
        safe_click(wait, A.SUBMENU_ADM_AGENCIAS)
        wait.until(EC.url_contains("/administration/agencies/"))
        safe_click(wait, A.BTN_NUEVO)
        wait.until(lambda d: "detail.aspx" in d.current_url.lower())
        wait.until(EC.visibility_of_element_located(A.TXT_NAME))

    with allure.step("2. Llenar el form de Agencia"):
        safe_send_keys(wait, A.TXT_NAME, nombre)
        safe_send_keys(wait, A.TXT_TABNAME, "Oportunidades")
        safe_send_keys(wait, A.TXT_ADDRESS, "Calle Test 123")
        safe_send_keys(wait, A.TXT_EMAIL, email)
        safe_send_keys(wait, A.TXT_PHONE, "1122334455")
        safe_send_keys(wait, A.TXT_COMMENT, "Test automático")
        _sel_primera(driver, A.DD_VENDOR)
        _sel_primera(driver, A.DD_MARKET)
        _sel_primera(driver, A.DD_CITIES)
        _check(driver, wait, A.CB_PUBLICADO, on=True)
        escribir_quill(driver, wait, A.QUILL_ES, "Test automático")
        allure.attach(driver.get_screenshot_as_png(), "2_Form_Agencia", allure.attachment_type.PNG)

    with allure.step("3. Guardar y confirmar el modal con 'Sí'"):
        safe_click(wait, A.BTN_GUARDAR)
        time.sleep(2)
        try:
            safe_click(wait, A.MODAL_SI)
        except Exception:
            allure.attach("No apareció el modal 'Sí' (o ya redirigió).",
                          "3_Modal", allure.attachment_type.TEXT)
        time.sleep(2)
        allure.attach(driver.get_screenshot_as_png(), "3_PostModal", allure.attachment_type.PNG)

    # ── PASO 2: form del Usuario admin (CustomerTabContainer) ─────────────────
    with allure.step("4. Llenar el form del usuario admin"):
        wait.until(EC.visibility_of_element_located(U.TXT_USERNAME))
        safe_send_keys(wait, U.TXT_USERNAME, f"ageadmin{stamp}")
        _check(driver, wait, U.CHK_ENABLE_PASS, on=True)
        time.sleep(1)
        pw = driver.find_elements(*U.TXT_PASS)
        if pw:
            driver.execute_script("arguments[0].value=arguments[1];"
                                  "arguments[0].dispatchEvent(new Event('change',{bubbles:true}));",
                                  pw[0], "SanJuan28@G")
        bcp = driver.find_elements(*U.BTN_CONFIRM_PASS)
        if bcp and bcp[0].is_displayed():
            driver.execute_script("arguments[0].click();", bcp[0])
            time.sleep(1)
        _check(driver, wait, U.CB_PUBLICADO, on=True)
        _sel_texto(driver, U.DD_USERTYPE, "Cliente")
        safe_send_keys(wait, U.TXT_NAME, f"Admin {sello}")
        safe_send_keys(wait, U.TXT_LASTNAME, "Automatico")
        safe_send_keys(wait, U.TXT_EMAIL, email)
        _sel_texto(driver, U.DD_COUNTRY, "España")
        _sel_texto(driver, U.DD_CURRENCY, "Dollar")
        allure.attach(driver.get_screenshot_as_png(), "4_Form_Usuario", allure.attachment_type.PNG)

    with allure.step("5. Guardar el usuario (modal de email)"):
        safe_click(wait, U.BTN_GUARDAR_EMAIL)
        time.sleep(1)
        try:
            wait.until(EC.visibility_of_element_located(U.TXT_MODAL_EMAIL))
            safe_send_keys(wait, U.TXT_MODAL_EMAIL, email)
            ve = driver.find_elements(*U.TXT_MODAL_VENDOR_EML)
            if ve:
                safe_send_keys(wait, U.TXT_MODAL_VENDOR_EML, email)
            safe_click(wait, U.BTN_MODAL_CONFIRM)
        except Exception:
            allure.attach("No apareció el modal de email del usuario.",
                          "5_Modal", allure.attachment_type.TEXT)
        time.sleep(2)

    with allure.step("6. Volver a la lista de Agencias y validar la fila"):
        base = driver.current_url.split("/administration/")[0]
        driver.get(f"{base}/administration/agencies/")
        safe_send_keys(wait, A.TXT_SEARCH, f"Agencia Test {fecha}")
        safe_click(wait, A.BTN_SEARCH)
        time.sleep(1)
        wait.until(EC.presence_of_element_located(A.TABLA))
        fila = wait.until(EC.presence_of_element_located(A.fila_por_nombre(sello)))
        assert fila is not None, f"La agencia '{nombre}' no aparece en la tabla."
        allure.attach(driver.get_screenshot_as_png(), "6_Validacion_Tabla", allure.attachment_type.PNG)
