import time
import allure
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from helpers import safe_click, safe_send_keys
from pages.webadmin_tour_page import escribir_quill
from pages.webadmin_foodtype_page import WebAdminFoodTypePage as P


@allure.feature("WebAdmin AMV Travel")
@allure.story("Ubicación → Crear Tipo de Comida y validar persistencia")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("""
Crea un Tipo de Comida desde el WebAdmin (foodtypesdetail.aspx) y valida el flujo:
1. Navegación Menú → Ubicación → Tipos de Comida.
2. "+ Agregar Nuevo" → detail aparte.
3. Carga de Nombre dinámico + Nombre localizado ES + Quill ES + Publicado.
4. Guardar.
5. Vuelta a la lista y validación de la fila por el sello (la lista no tiene buscador).
""")
def test_crear_tipo_comida(login_webadmin):
    driver = login_webadmin
    wait = WebDriverWait(driver, 45)

    ahora = datetime.now()
    sello = ahora.strftime('%d/%m/%Y %H:%M:%S')   # único, ASCII
    # Prefijo corto por si el nombre se trunca server-side (~50): 16 + 19 = 35 chars.
    PREFIJO = "Tipo Comida Test"
    nombre = f"{PREFIJO} {sello}"

    with allure.step("1. Menú Ubicación → Tipos de Comida"):
        safe_click(wait, P.MENU_UBICACION)
        time.sleep(1)  # animación del acordeón
        safe_click(wait, P.SUBMENU)
        wait.until(EC.url_contains(P.URL_LISTA))

    with allure.step("2. '+ Agregar Nuevo' → detail"):
        safe_click(wait, P.BTN_NUEVO)
        wait.until(EC.url_contains(P.URL_DETALLE))
        wait.until(EC.visibility_of_element_located(P.TXT_NAME))

    with allure.step("3. Cargar Nombre, localización ES (nombre + Quill) y Publicado"):
        safe_send_keys(wait, P.TXT_NAME, nombre)
        safe_send_keys(wait, P.NOMBRE_ES, nombre)
        escribir_quill(driver, wait, P.QUILL_ES, "Test automático")
        cb = wait.until(EC.presence_of_element_located(P.CB_PUBLICADO))
        if not cb.is_selected():
            driver.execute_script("arguments[0].click();", cb)
        allure.attach(driver.get_screenshot_as_png(), "3_Form_Completo", allure.attachment_type.PNG)

    with allure.step("4. Guardar"):
        safe_click(wait, P.BTN_GUARDAR)
        time.sleep(1)  # postback de guardado

    with allure.step("5. Volver a la lista y validar la fila por el sello"):
        origin = driver.current_url.split("/administration/")[0]
        driver.get(origin + P.URL_LISTA)
        wait.until(EC.presence_of_element_located(P.TABLA))
        time.sleep(1)
        fila = wait.until(EC.presence_of_element_located(P.fila_por_nombre(sello)))
        assert fila is not None, f"El Tipo de Comida '{nombre}' no aparece en la tabla."
        allure.attach(f"Tipo de Comida encontrado: {nombre}", "5_En_Tabla", allure.attachment_type.TEXT)
        allure.attach(driver.get_screenshot_as_png(), "5_Validacion_Tabla", allure.attachment_type.PNG)
