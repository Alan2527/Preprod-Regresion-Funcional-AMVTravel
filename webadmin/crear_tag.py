import time
import allure
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from helpers import safe_click, safe_send_keys
from pages.webadmin_tag_page import WebAdminTagPage as P


@allure.feature("WebAdmin AMV Travel")
@allure.story("Crear Tag y validar persistencia")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("""
Crea un Tag de Servicios desde el WebAdmin y valida el flujo completo:
1. Navegación Menú → Servicios → Tags.
2. Click en "Nuevo" → se abre el modal "Agregar nuevo tag".
3. Carga del nombre dinámico (con fecha/hora) y Guardar.
4. Búsqueda en la lista y validación de que el tag recién creado aparece en la tabla.
""")
def test_crear_tag(login_webadmin):
    driver = login_webadmin
    wait = WebDriverWait(driver, 45)

    ahora = datetime.now()
    sello = ahora.strftime('%d/%m/%Y %H:%M:%S')   # ASCII y único por corrida
    nombre_tag = f"Tag Test Automático {sello}"

    # ──────────────────────────────────────────
    # 1. NAVEGACIÓN → TAGS
    # ──────────────────────────────────────────
    with allure.step("1. Menú Servicios → Tags"):
        safe_click(wait, P.MENU_SERVICIOS)
        time.sleep(1)  # animación acordeón del menú
        safe_click(wait, P.SUBMENU_TAGS)
        wait.until(EC.url_contains("/administration/services/tags.aspx"))

    # ──────────────────────────────────────────
    # 2. ABRIR EL MODAL "AGREGAR NUEVO TAG"
    # ──────────────────────────────────────────
    with allure.step("2. Click en 'Nuevo' y esperar el modal"):
        safe_click(wait, P.BTN_NUEVO)
        # El ModalPopupExtender muestra el panel; esperamos a que el input sea visible.
        wait.until(EC.visibility_of_element_located(P.TXT_NAME))

    # ──────────────────────────────────────────
    # 3. CARGAR NOMBRE
    # ──────────────────────────────────────────
    with allure.step("3. Cargar el nombre del tag"):
        safe_send_keys(wait, P.TXT_NAME, nombre_tag)
        allure.attach(driver.get_screenshot_as_png(), "3_Tag_Nombre", allure.attachment_type.PNG)

    # ──────────────────────────────────────────
    # 4. GUARDAR
    # ──────────────────────────────────────────
    with allure.step("4. Guardar"):
        safe_click(wait, P.BTN_GUARDAR)
        time.sleep(1)  # postback de guardado (recarga la lista)

    # ──────────────────────────────────────────
    # 5. BUSCAR Y VALIDAR EN LA TABLA
    # ──────────────────────────────────────────
    with allure.step("5. Buscar y validar que el tag aparece en la tabla"):
        # Gotcha #1: buscar por el nombre SIN la hora (los ':' devuelven 0 resultados).
        nombre_sin_hora = f"Tag Test Automático {ahora.strftime('%d/%m/%Y')}"
        safe_send_keys(wait, P.TXT_SEARCH, nombre_sin_hora)
        safe_click(wait, P.BTN_SEARCH)
        time.sleep(1)  # postback de búsqueda
        # 'presence' (no 'visibility'): el wrapper JS puede ocultar la tabla.
        wait.until(EC.presence_of_element_located(P.TABLA))
        # La fila exacta se valida por el sello completo (con hora), que está en el <td>.
        fila = wait.until(EC.presence_of_element_located(P.fila_por_nombre(sello)))
        assert fila is not None, f"El tag '{nombre_tag}' no aparece en la tabla."
        allure.attach(
            f"Tag encontrado en la tabla: {nombre_tag}",
            "5_Tag_En_Tabla",
            allure.attachment_type.TEXT,
        )
        allure.attach(driver.get_screenshot_as_png(), "5_Validacion_Tabla", allure.attachment_type.PNG)
