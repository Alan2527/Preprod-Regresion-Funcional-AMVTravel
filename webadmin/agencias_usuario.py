import time
import allure
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from helpers import safe_click, safe_send_keys
from pages.webadmin_usuario_page import WebAdminUsuarioPage as P


def _sel_primera(driver, locator):
    """Selecciona la primera opción REAL de un <select>, salteando placeholders
    ('' / '-5' / '0' como 'Seleccione...')."""
    els = driver.find_elements(*locator)
    if not els:
        return None
    sel = Select(els[0])
    for o in sel.options:
        v = o.get_attribute("value")
        if v and v not in ("-5", "0"):
            sel.select_by_value(v)
            o2 = sel.first_selected_option
            driver.execute_script("arguments[0].dispatchEvent(new Event('change',{bubbles:true}));", els[0])
            return o2.text
    return None


def _sel_texto(driver, locator, texto):
    els = driver.find_elements(*locator)
    if els:
        try:
            Select(els[0]).select_by_visible_text(texto)
            return
        except Exception:
            _sel_primera(driver, locator)


def _sel_agencia(driver, wait, locator):
    """ddlAgencies es un <select> nativo con OnChange='ddlAgenciesChange()'. Selecciona la
    primera opción real por JS y dispara el change para que la app registre la agencia
    (si no, el guardado tira 'DEBE SELECCIONAR AGENCIA')."""
    wait.until(lambda d: len(d.find_element(*locator).find_elements(By.TAG_NAME, "option")) > 1)
    el = driver.find_element(*locator)
    # ⚠ El placeholder "Seleccione..." tiene value="-5" (no vacío): hay que saltearlo y
    #   elegir la primera AGENCIA real (value entero positivo).
    return driver.execute_script("""
        var s=arguments[0];
        for(var i=0;i<s.options.length;i++){
            var v=s.options[i].value;
            if(v && v!=="-5" && v!=="0" && parseInt(v,10)>0){
                s.selectedIndex=i;
                s.dispatchEvent(new Event('change',{bubbles:true}));
                if(typeof ddlAgenciesChange==='function'){try{ddlAgenciesChange();}catch(e){}}
                return s.options[i].text;
            }
        }
        return null;""", el)


def _check(driver, wait, locator, on=True):
    cb = wait.until(EC.presence_of_element_located(locator))
    if cb.is_selected() != on:
        driver.execute_script("arguments[0].click();", cb)


@allure.feature("WebAdmin AMV Travel")
@allure.story("Crear Usuario y validar persistencia")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("""
Crea un Usuario (Agencias → Usuarios → Nuevo) con los datos de la captura:
nombre de usuario, password manual, Tipo=Cliente, Nombre/Apellido/Email, Agencia, País=España,
Moneda=Dollar, Mostrar Markup. Guarda vía "Guardar y enviar email" → modal de confirmación,
y valida la fila tras volver a la lista.
⚠ Flujo con modales (best-effort): puede requerir ajustes según comportamiento real.
""")
def test_crear_usuario(login_webadmin):
    driver = login_webadmin
    wait = WebDriverWait(driver, 45)

    ahora = datetime.now()
    sello = ahora.strftime('%d/%m/%Y %H:%M:%S')
    stamp = ahora.strftime('%d%m%Y%H%M%S')
    nombre = f"Test {sello}"
    apellido = f"Automatico {sello}"
    email = f"usuariotestauto{stamp}@gmail.com"
    username = f"usrtest{stamp}"
    fecha = ahora.strftime('%d/%m/%Y')

    with allure.step("1. Menú Agencias → Usuarios → Nuevo"):
        safe_click(wait, P.MENU_AGENCIAS)
        time.sleep(1)
        safe_click(wait, P.SUBMENU_USUARIOS)
        wait.until(EC.url_contains("/administration/customers/"))
        safe_click(wait, P.BTN_NUEVO)
        wait.until(lambda d: "detail.aspx" in d.current_url.lower())
        wait.until(EC.visibility_of_element_located(P.TXT_USERNAME))

    with allure.step("2. Acceso: usuario, password manual, tipo, publicado"):
        safe_send_keys(wait, P.TXT_USERNAME, username)
        _check(driver, wait, P.CHK_ENABLE_PASS, on=True)   # Habilitar password manual
        time.sleep(1)
        pw = driver.find_elements(*P.TXT_PASS)
        if pw:
            driver.execute_script("arguments[0].value=arguments[1];"
                                  "arguments[0].dispatchEvent(new Event('change',{bubbles:true}));",
                                  pw[0], "SanJuan28@G")
        # Si aparece el popup de confirmación de password, aceptarlo.
        bcp = driver.find_elements(*P.BTN_CONFIRM_PASS)
        if bcp and bcp[0].is_displayed():
            driver.execute_script("arguments[0].click();", bcp[0])
            time.sleep(1)
        _check(driver, wait, P.CB_PUBLICADO, on=True)
        _sel_texto(driver, P.DD_USERTYPE, "Cliente")

    with allure.step("3. Datos personales y configuración"):
        safe_send_keys(wait, P.TXT_NAME, nombre)
        safe_send_keys(wait, P.TXT_LASTNAME, apellido)
        safe_send_keys(wait, P.TXT_EMAIL, email)
        _sel_agencia(driver, wait, P.DD_AGENCIES)
        _sel_texto(driver, P.DD_COUNTRY, "España")
        _sel_texto(driver, P.DD_CURRENCY, "Dollar")
        _check(driver, wait, P.CB_SHOWMARKUP, on=True)
        allure.attach(driver.get_screenshot_as_png(), "3_Formulario", allure.attachment_type.PNG)

    with allure.step("4. Guardar y enviar email → modal 'Datos del email'"):
        safe_click(wait, P.BTN_GUARDAR_EMAIL)
        # Modal: Cliente/Vendedor vienen prefilled; sólo hay que elegir el Responsable
        # comercial (requerido) y Confirmar.
        wait.until(EC.visibility_of_element_located(P.DD_SALES_MANAGER))
        _sel_primera(driver, P.DD_SALES_MANAGER)
        allure.attach(driver.get_screenshot_as_png(), "4_Modal", allure.attachment_type.PNG)
        safe_click(wait, P.BTN_MODAL_CONFIRM)
        time.sleep(2)
        allure.attach(driver.get_screenshot_as_png(), "4_PostGuardado", allure.attachment_type.PNG)

    with allure.step("5. Volver a la lista, poner Estado=TODOS y validar la fila"):
        # ⚠ La lista viene filtrada por Estado="Pendiente Validación"; hay que ponerlo en
        #   TODOS para que aparezca el usuario recién creado (Cliente/Activo).
        base = driver.current_url.split("/administration/")[0]
        driver.get(f"{base}/administration/customers/")
        Select(wait.until(EC.element_to_be_clickable(P.DD_STATUS))).select_by_value("")
        safe_click(wait, P.BTN_SEARCH)
        time.sleep(1)
        wait.until(EC.presence_of_element_located(P.TABLA))
        fila = wait.until(EC.presence_of_element_located(P.fila_por_nombre(sello)))
        assert fila is not None, f"El usuario '{nombre}' no aparece en la tabla."
        allure.attach(driver.get_screenshot_as_png(), "5_Validacion_Tabla", allure.attachment_type.PNG)
