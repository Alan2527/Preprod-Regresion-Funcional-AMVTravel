import time
import allure
from datetime import datetime, timedelta
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from helpers import safe_click, safe_send_keys
from pages.webadmin_cotizacion_grupo_page import WebAdminCotizacionGrupoPage as P
from pages.cotizacion_helpers import sel_primera, sel_texto, set_fecha, validar_solapas


@allure.feature("WebAdmin AMV Travel")
@allure.story("Cotizaciones: crear Grupo y validar persistencia")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("""
Crea una Cotización de Grupo (Cotizaciones → Grupos → Crear), guarda, valida que las
solapas (Detalle de la cotización, Configuración, Destinos, Hoteles, Servicios/Restaurantes,
Salones, Gifts, Archivos) estén activas y disponibles, y valida la fila en la lista.
""")
def test_grupos(login_webadmin):
    driver = login_webadmin
    wait = WebDriverWait(driver, 45)

    ahora = datetime.now()
    sello = ahora.strftime('%d/%m/%Y %H:%M:%S')
    titulo = f"Cotiz Grupo Test {sello}"
    inicio = ahora.strftime('%d/%m/%Y')
    record = (ahora + timedelta(days=7)).strftime('%d/%m/%Y')

    with allure.step("1. Menú Cotizaciones → Grupos → Crear"):
        safe_click(wait, P.MENU_COTIZACIONES)
        time.sleep(1)
        safe_click(wait, P.SUBMENU_GRUPOS)
        wait.until(EC.url_contains("/administration/budgets/default.aspx"))
        safe_click(wait, P.BTN_NUEVO)
        wait.until(lambda d: "budgetdetail.aspx" in d.current_url.lower())
        wait.until(EC.visibility_of_element_located(P.TXT_REFERENCE))

    with allure.step("2. Cargar el Detalle de la cotización"):
        sel_primera(driver, P.DD_BRANCH)            # Sucursal (requerido)
        set_fecha(driver, P.FECHA_INICIO, inicio)
        set_fecha(driver, P.FECHA_RECORD, record)
        safe_send_keys(wait, P.TXT_REFERENCE, titulo)
        safe_send_keys(wait, P.TXT_TITLE, titulo)
        sel_primera(driver, P.DD_LANG)
        sel_texto(driver, P.DD_ITINERARY, "Argentina de Sur a Norte")
        sel_primera(driver, P.DD_AGENCY)
        time.sleep(1)                                # el agente puede recargar ejecutivos
        sel_primera(driver, P.DD_EXECUTIVE)
        safe_send_keys(wait, P.TXT_MARKUP, "0")
        safe_send_keys(wait, P.TXT_EXCHANGE, "950")
        safe_send_keys(wait, P.TXT_PAX, "10")
        safe_send_keys(wait, P.TXT_SGL, "5")
        safe_send_keys(wait, P.TXT_DBL, "1")
        safe_send_keys(wait, P.TXT_TPL, "1")
        cb = wait.until(EC.presence_of_element_located(P.CB_PUBLICADO))
        if not cb.is_selected():
            driver.execute_script("arguments[0].click();", cb)
        allure.attach(driver.get_screenshot_as_png(), "2_Formulario", allure.attachment_type.PNG)

    with allure.step("3. Guardar"):
        safe_click(wait, P.BTN_GUARDAR)
        time.sleep(2)
        allure.attach(f"URL tras guardar: {driver.current_url}", "3_URL", allure.attachment_type.TEXT)

    with allure.step("4. Validar solapas activas y disponibles"):
        validar_solapas(driver, P.TAB_CONTAINER, P.SOLAPAS)
        allure.attach(driver.get_screenshot_as_png(), "4_Solapas", allure.attachment_type.PNG)

    with allure.step("5. Volver a la lista de Grupos y validar la fila"):
        base = driver.current_url.split("/administration/")[0]
        driver.get(f"{base}/administration/budgets/default.aspx")
        safe_send_keys(wait, P.TXT_SEARCH, f"Cotiz Grupo Test {inicio}")
        safe_click(wait, P.BTN_SEARCH)
        time.sleep(1)
        wait.until(EC.presence_of_element_located(P.TABLA))
        fila = wait.until(EC.presence_of_element_located(P.fila_por_nombre(sello)))
        assert fila is not None, f"La cotización de grupo '{titulo}' no aparece en la tabla."
        allure.attach(driver.get_screenshot_as_png(), "5_Validacion_Tabla", allure.attachment_type.PNG)
