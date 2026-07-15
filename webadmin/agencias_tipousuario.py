import time
import allure
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from helpers import safe_click, safe_send_keys
from pages.webadmin_tipo_usuario_page import WebAdminTipoUsuarioPage as P


@allure.feature("WebAdmin AMV Travel")
@allure.story("Crear Tipo de Usuario y validar persistencia")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("""
Crea un Tipo de Usuario (Agencias → Tipos de Usuario → Nuevo, form inline) y valida la
fila en la misma pantalla.
""")
def test_crear_tipo_usuario(login_webadmin):
    driver = login_webadmin
    wait = WebDriverWait(driver, 45)

    ahora = datetime.now()
    sello = ahora.strftime('%d/%m/%Y %H:%M:%S')
    nombre = f"TipoUsr Test {sello}"
    fecha = ahora.strftime('%d/%m/%Y')

    with allure.step("1. Menú Agencias → Tipos de Usuario → Nuevo"):
        safe_click(wait, P.MENU_AGENCIAS)
        time.sleep(1)
        safe_click(wait, P.SUBMENU_TIPOS_USUARIO)
        wait.until(EC.url_contains("/administration/types/usertypes.aspx"))
        safe_click(wait, P.BTN_NUEVO)
        wait.until(EC.visibility_of_element_located(P.TXT_NAME))

    with allure.step("2. Cargar nombre, detalle y Publicado"):
        safe_send_keys(wait, P.TXT_NAME, nombre)
        safe_send_keys(wait, P.TXT_DETAIL, "Test automático")
        cb = wait.until(EC.presence_of_element_located(P.CB_PUBLICADO))
        if not cb.is_selected():
            driver.execute_script("arguments[0].click();", cb)

    with allure.step("3. Guardar"):
        safe_click(wait, P.BTN_GUARDAR)
        time.sleep(1)

    with allure.step("4. Validar la fila en la tabla (misma pantalla)"):
        safe_send_keys(wait, P.TXT_SEARCH, f"TipoUsr Test {fecha}")
        safe_click(wait, P.BTN_SEARCH)
        time.sleep(1)
        wait.until(EC.presence_of_element_located(P.TABLA))
        fila = wait.until(EC.presence_of_element_located(P.fila_por_nombre(sello)))
        assert fila is not None, f"El tipo de usuario '{nombre}' no aparece en la tabla."
        allure.attach(driver.get_screenshot_as_png(), "4_Validacion_Tabla", allure.attachment_type.PNG)
