import time
import allure
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from helpers import safe_click, safe_send_keys
from pages.webadmin_crucero_simple_page import WebAdminCruceroSimplePage as P


@allure.feature("WebAdmin AMV Travel")
@allure.story("Crear Flota y validar persistencia")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("""
Crea una Flota desde el WebAdmin (Cruceros → Flotas → Nuevo) y valida:
1. Click en Nuevo → form inline (Nombre + Publicado).
2. Guardar.
3. En la MISMA pantalla, la flota recién creada aparece en la tabla.
""")
def test_crear_flota(login_webadmin):
    driver = login_webadmin
    wait = WebDriverWait(driver, 45)

    ahora = datetime.now()
    sello = ahora.strftime('%d/%m/%Y %H:%M:%S')
    nombre = f"Flota Test {sello}"
    fecha = ahora.strftime('%d/%m/%Y')

    with allure.step("1. Menú Cruceros → Flotas → Nuevo"):
        safe_click(wait, P.MENU_CRUCEROS)
        time.sleep(1)
        safe_click(wait, P.SUBMENU_FLOTAS)
        wait.until(EC.url_contains("/administration/cruises/cruisenavies.aspx"))
        safe_click(wait, P.BTN_NUEVO)
        wait.until(EC.visibility_of_element_located(P.TXT_NAME))

    with allure.step("2. Cargar nombre y Publicado"):
        safe_send_keys(wait, P.TXT_NAME, nombre)
        cb = wait.until(EC.presence_of_element_located(P.CB_PUBLICADO))
        if not cb.is_selected():
            driver.execute_script("arguments[0].click();", cb)
        allure.attach(driver.get_screenshot_as_png(), "2_Formulario", allure.attachment_type.PNG)

    with allure.step("3. Guardar"):
        safe_click(wait, P.BTN_GUARDAR)
        time.sleep(1)

    with allure.step("4. Validar que la flota aparece en la tabla (misma pantalla)"):
        safe_send_keys(wait, P.TXT_SEARCH, f"Flota Test {fecha}")
        safe_click(wait, P.BTN_SEARCH)
        time.sleep(1)
        wait.until(EC.presence_of_element_located(P.TABLA))
        fila = wait.until(EC.presence_of_element_located(P.fila_por_nombre(sello)))
        assert fila is not None, f"La flota '{nombre}' no aparece en la tabla."
        allure.attach(driver.get_screenshot_as_png(), "4_Validacion_Tabla", allure.attachment_type.PNG)
