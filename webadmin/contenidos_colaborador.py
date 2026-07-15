import time
import allure
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from helpers import safe_click, safe_send_keys
from pages.ubicacion_helpers import seleccionar
from pages.webadmin_collaborator_page import WebAdminCollaboratorPage as P


@allure.feature("WebAdmin AMV Travel")
@allure.story("Contenidos → Crear Colaborador y validar persistencia")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("""
Crea un Colaborador (collaborators/detail.aspx): Nombre dinámico + Apellido + Puesto +
Área + Email único + Teléfono + Sucursal + Publicado → Guardar → validar la fila por
el sello.
⚠ Best-effort: la lista no tiene buscador y pagina; probable ajuste tras la 1ª corrida.
""")
def test_crear_colaborador(login_webadmin):
    driver = login_webadmin
    wait = WebDriverWait(driver, 45)

    ahora = datetime.now()
    sello = ahora.strftime('%d/%m/%Y %H:%M:%S')
    PREFIJO = "Colab Test"
    nombre = f"{PREFIJO} {sello}"
    email = "colab" + ahora.strftime('%d%m%Y%H%M%S') + "@test.com"

    with allure.step("1. Menú Contenidos → Colaboradores"):
        safe_click(wait, P.MENU_CONTENIDOS)
        time.sleep(1)
        safe_click(wait, P.SUBMENU)
        wait.until(EC.url_contains(P.URL_LISTA))

    with allure.step("2. 'Nuevo' → detail"):
        safe_click(wait, P.BTN_NUEVO)
        wait.until(EC.url_contains(P.URL_DETALLE))
        wait.until(EC.visibility_of_element_located(P.TXT_NAME))

    with allure.step("3. Completar datos del colaborador"):
        safe_send_keys(wait, P.TXT_NAME, nombre)
        safe_send_keys(wait, P.TXT_LASTNAME, "Apellido Test")
        safe_send_keys(wait, P.TXT_JOB, "Puesto Test")
        safe_send_keys(wait, P.TXT_AREA, "Area Test")
        safe_send_keys(wait, P.TXT_EMAIL, email)
        safe_send_keys(wait, P.TXT_PHONE, "1122334455")
        seleccionar(driver, wait, P.DD_SUCURSAL)
        cb = wait.until(EC.presence_of_element_located(P.CB_PUBLICADO))
        if not cb.is_selected():
            driver.execute_script("arguments[0].click();", cb)
        allure.attach(driver.get_screenshot_as_png(), "3_Form", allure.attachment_type.PNG)

    with allure.step("4. Guardar"):
        safe_click(wait, P.BTN_GUARDAR)
        time.sleep(1)

    with allure.step("5. Volver a la lista y validar la fila por el sello"):
        origin = driver.current_url.split("/administration/")[0]
        driver.get(origin + P.URL_LISTA)
        wait.until(EC.presence_of_element_located(P.TABLA))
        time.sleep(1)
        fila = wait.until(EC.presence_of_element_located(P.fila_por_nombre(sello)))
        assert fila is not None, f"El Colaborador '{nombre}' no aparece en la tabla."
        allure.attach(driver.get_screenshot_as_png(), "5_Validacion", allure.attachment_type.PNG)
