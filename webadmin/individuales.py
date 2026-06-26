import time
import allure
from datetime import datetime, timedelta
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from helpers import safe_click, safe_send_keys
from pages.webadmin_cotizacion_individual_page import WebAdminCotizacionIndividualPage as P
from pages.cotizacion_helpers import sel_primera, sel_texto, set_fecha, validar_solapas


@allure.feature("WebAdmin AMV Travel")
@allure.story("Cotizaciones: crear Individual, validar Preview y persistencia")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("""
Crea una Cotización Individual (Cotizaciones → Individuales → Crear), guarda, valida que
las solapas (Detalle, Destinos, Hoteles, Servicios/Restaurantes, Cruceros) estén habilitadas
y no bloqueadas, abre el Preview en una pestaña nueva y valida que su contenido coincida con
el esperado (landmarks del itinerario), y valida la fila en la lista.
""")
def test_individuales(login_webadmin):
    driver = login_webadmin
    wait = WebDriverWait(driver, 45)

    ahora = datetime.now()
    sello = ahora.strftime('%d/%m/%Y %H:%M:%S')
    titulo = f"Cotiz Indiv Test {sello}"
    record = (ahora + timedelta(days=1)).strftime('%d/%m/%Y')

    with allure.step("1. Menú Cotizaciones → Individuales → Crear"):
        safe_click(wait, P.MENU_COTIZACIONES)
        time.sleep(1)
        safe_click(wait, P.SUBMENU_INDIVIDUALES)
        wait.until(EC.url_contains("/administration/budgets/defaultsingle.aspx"))
        safe_click(wait, P.BTN_NUEVO)
        wait.until(lambda d: "budgetsingle.aspx" in d.current_url.lower())
        wait.until(EC.visibility_of_element_located(P.TXT_REFERENCE))

    with allure.step("2. Cargar el Detalle de la cotización"):
        safe_send_keys(wait, P.TXT_REFERENCE, titulo)
        safe_send_keys(wait, P.TXT_TITLE, titulo)
        sel_primera(driver, P.DD_AGENCY)
        sel_primera(driver, P.DD_LANG)
        sel_texto(driver, P.DD_ITINERARY, "Argentina de Sur a Norte")
        set_fecha(driver, P.FECHA_RECORD, record)
        for loc in (P.CHK_PRESENTACION, P.CB_PUBLICADO):
            cb = wait.until(EC.presence_of_element_located(loc))
            if not cb.is_selected():
                driver.execute_script("arguments[0].click();", cb)
        allure.attach(driver.get_screenshot_as_png(), "2_Formulario", allure.attachment_type.PNG)

    with allure.step("3. Guardar"):
        safe_click(wait, P.BTN_GUARDAR)
        time.sleep(2)
        allure.attach(f"URL tras guardar: {driver.current_url}", "3_URL", allure.attachment_type.TEXT)

    with allure.step("4. Validar solapas habilitadas y no bloqueadas"):
        validar_solapas(driver, P.TAB_CONTAINER, P.SOLAPAS)
        allure.attach(driver.get_screenshot_as_png(), "4_Solapas", allure.attachment_type.PNG)

    with allure.step("5. Preview: abre pestaña nueva y validar contenido"):
        ventana_orig = driver.current_window_handle
        handles_antes = set(driver.window_handles)
        # El botón Preview (<a target=_blank>) a veces no pasa element_to_be_clickable;
        # lo clickeamos por JS sobre su presencia.
        prev = wait.until(EC.presence_of_element_located(P.BTN_PREVIEW))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", prev)
        driver.execute_script("arguments[0].click();", prev)
        # Esperar la nueva pestaña.
        wait.until(lambda d: len(d.window_handles) > len(handles_antes))
        nueva = [h for h in driver.window_handles if h not in handles_antes][0]
        driver.switch_to.window(nueva)
        wait.until(lambda d: "previewmailing" in d.current_url.lower())
        time.sleep(1)
        html = driver.page_source
        faltantes = [lm for lm in P.PREVIEW_LANDMARKS if lm.lower() not in html.lower()]
        allure.attach(driver.get_screenshot_as_png(), "5_Preview", allure.attachment_type.PNG)
        assert not faltantes, f"El preview no coincide con el esperado; faltan landmarks: {faltantes}"
        # Volver a la pestaña original.
        driver.close()
        driver.switch_to.window(ventana_orig)

    with allure.step("6. Volver a la lista de Individuales y validar la fila"):
        base = driver.current_url.split("/administration/")[0]
        driver.get(f"{base}/administration/budgets/defaultsingle.aspx")
        safe_send_keys(wait, P.TXT_SEARCH, f"Cotiz Indiv Test {ahora.strftime('%d/%m/%Y')}")
        safe_click(wait, P.BTN_SEARCH)
        time.sleep(1)
        wait.until(EC.presence_of_element_located(P.TABLA))
        fila = wait.until(EC.presence_of_element_located(P.fila_por_nombre(sello)))
        assert fila is not None, f"La cotización individual '{titulo}' no aparece en la tabla."
        allure.attach(driver.get_screenshot_as_png(), "6_Validacion_Tabla", allure.attachment_type.PNG)
