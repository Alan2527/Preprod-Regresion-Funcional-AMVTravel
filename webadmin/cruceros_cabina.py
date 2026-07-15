import time
import allure
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from helpers import safe_click, safe_send_keys
from pages.webadmin_cabina_page import WebAdminCabinaPage as P
from pages.webadmin_tour_page import escribir_quill, validar_solapas


@allure.feature("WebAdmin AMV Travel")
@allure.story("Crear Cabina y validar persistencia")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("""
Crea una Cabina desde el WebAdmin (Cruceros → Cabinas → Nuevo) y valida:
1. Apertura del formulario (detail.aspx).
2. Carga del Detalle (nombre, crucero, moneda, min rate, capacidad, tipo, publicado, Quill).
3. Guardar y validar solapas habilitadas: Detalle/Imagenes/Tarifas.
4. Volver a la lista de Cabinas y validar la fila.
""")
def test_crear_cabina(login_webadmin):
    driver = login_webadmin
    wait = WebDriverWait(driver, 45)

    ahora = datetime.now()
    sello = ahora.strftime('%d/%m/%Y %H:%M:%S')
    nombre = f"Cabina Test {sello}"
    texto_quill = f"Test automático corrido el {sello}"
    fecha = ahora.strftime('%d/%m/%Y')

    with allure.step("1. Menú Cruceros → Cabinas → Nuevo"):
        safe_click(wait, P.MENU_CRUCEROS)
        time.sleep(1)
        safe_click(wait, P.SUBMENU_CABINAS)
        wait.until(EC.url_contains("/administration/cruisecabs/default.aspx"))
        safe_click(wait, P.BTN_NUEVO)
        wait.until(lambda d: "detail.aspx" in d.current_url.lower())
        wait.until(EC.visibility_of_element_located(P.TXT_NAME))

    with allure.step("2. Cargar el Detalle"):
        safe_send_keys(wait, P.TXT_NAME, nombre)
        Select(wait.until(EC.element_to_be_clickable(P.DD_CRUISE))).select_by_visible_text("Crucero Antarpply")
        Select(wait.until(EC.element_to_be_clickable(P.DD_CURRENCY))).select_by_visible_text("Dollar")
        safe_send_keys(wait, P.TXT_MIN_RATE, "0")
        safe_send_keys(wait, P.TXT_CAPACIDAD, "4")
        Select(wait.until(EC.element_to_be_clickable(P.DD_TYPE))).select_by_visible_text("A Stella")
        cb = wait.until(EC.presence_of_element_located(P.CB_PUBLICADO))
        if not cb.is_selected():
            driver.execute_script("arguments[0].click();", cb)
        safe_send_keys(wait, P.NOMBRE_DESC_ES, nombre)
        escribir_quill(driver, wait, P.QUILL_ES, texto_quill)
        allure.attach(driver.get_screenshot_as_png(), "2_Formulario_Completo", allure.attachment_type.PNG)

    with allure.step("3. Guardar"):
        safe_click(wait, P.BTN_GUARDAR)
        time.sleep(2)
        allure.attach(f"URL tras guardar: {driver.current_url}", "3_URL", allure.attachment_type.TEXT)

    with allure.step("4. Validar solapas habilitadas: Detalle, Imagenes, Tarifas"):
        validar_solapas(driver, P.TAB_CONTAINER, ["Detalle", "Imagenes", "Tarifas"], P.SOLAPAS)
        allure.attach(driver.get_screenshot_as_png(), "4_Solapas", allure.attachment_type.PNG)

    with allure.step("5. Volver a la lista de Cabinas y validar la fila"):
        base = driver.current_url.split("/administration/")[0]
        driver.get(f"{base}/administration/cruisecabs/default.aspx")
        safe_send_keys(wait, P.TXT_SEARCH, f"Cabina Test {fecha}")
        safe_click(wait, P.BTN_SEARCH)
        time.sleep(1)
        wait.until(EC.presence_of_element_located(P.TABLA))
        fila = wait.until(EC.presence_of_element_located(P.fila_por_nombre(sello)))
        assert fila is not None, f"La cabina '{nombre}' no aparece en la tabla."
        allure.attach(driver.get_screenshot_as_png(), "5_Validacion_Tabla", allure.attachment_type.PNG)
