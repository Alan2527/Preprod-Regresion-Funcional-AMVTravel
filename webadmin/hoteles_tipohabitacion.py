import allure
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from helpers import safe_click, safe_send_keys
from pages.webadmin_roomtype_page import WebAdminRoomTypePage as P


@allure.feature("WebAdmin AMV Travel")
@allure.story("Crear Tipo de Habitación y validar persistencia")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("""
Crea un tipo de habitación desde el WebAdmin y valida el flujo completo:
1. Navegación Menú -> Hoteles -> Tipos de habitación.
2. Click en Nuevo.
3. Carga del nombre (dinámico con fecha/hora) y el detalle.
4. Dejar tildado Publicado.
5. Guardado.
6. Validación de que el tipo recién creado aparece en la tabla.
""")
def test_crear_tipo_de_habitacion(login_webadmin):
    driver = login_webadmin
    wait = WebDriverWait(driver, 45)

    # Nombre dinámico con fecha/hora de ejecución (único por corrida).
    ahora = datetime.now()
    nombre_tipo = f"Tipo De Habitación Test {ahora.strftime('%d/%m/%Y %H:%M:%S')}"
    detalle = "Este es un test automático"

    # ==========================================
    # 1-4. NAVEGACIÓN A TIPOS DE HABITACIÓN
    # ==========================================
    with allure.step("1 a 4. Menú Hoteles -> Tipos de habitación"):
        safe_click(wait, P.MENU_HOTELES)
        # El acordeón del menú tiene animación: esperar el submenú clickeable.
        wait.until(EC.element_to_be_clickable(P.SUBMENU_TIPOS_HAB))
        safe_click(wait, P.SUBMENU_TIPOS_HAB)
        wait.until(EC.url_contains("/administration/types/roomtypes.aspx"))

    # ==========================================
    # 5. NUEVO
    # ==========================================
    with allure.step("5. Click en Nuevo y esperar el formulario"):
        safe_click(wait, P.BTN_NUEVO)
        wait.until(EC.visibility_of_element_located(P.TXT_NAME))

    # ==========================================
    # 6-7. NOMBRE Y DETALLE
    # ==========================================
    with allure.step("6 y 7. Cargar nombre y detalle"):
        safe_send_keys(wait, P.TXT_NAME, nombre_tipo)
        safe_send_keys(wait, P.TXT_DETAIL, detalle)
        allure.attach(
            f"Nombre: {nombre_tipo}\nDetalle: {detalle}",
            "6_Nombre_Detalle",
            allure.attachment_type.TEXT,
        )

    # ==========================================
    # 8. PUBLICADO (dejar tildado)
    # ==========================================
    with allure.step("8. Dejar tildado Publicado"):
        cb = wait.until(EC.presence_of_element_located(P.CB_PUBLICADO))
        if not cb.is_selected():
            driver.execute_script("arguments[0].click();", cb)
        allure.attach(driver.get_screenshot_as_png(), "8_Formulario_Completo", allure.attachment_type.PNG)

    # ==========================================
    # 9. GUARDAR
    # ==========================================
    with allure.step("9. Guardar"):
        safe_click(wait, P.BTN_GUARDAR)

    # ==========================================
    # 10. VALIDAR TIPO EN LA TABLA
    # ==========================================
    with allure.step("10. Validar que el tipo de habitación aparece en la tabla"):
        # Guardar dispara un postback async (UpdatePanel) que recarga la grilla:
        # esperar directamente la fila por el nombre completo cubre esa espera.
        wait.until(EC.presence_of_element_located(P.TABLA))
        fila = wait.until(EC.presence_of_element_located(P.fila_por_nombre(nombre_tipo)))
        assert fila is not None, f"El tipo de habitación '{nombre_tipo}' no aparece en la tabla."
        allure.attach(
            f"Tipo de habitación encontrado en la tabla: {nombre_tipo}",
            "10_Tipo_En_Tabla",
            allure.attachment_type.TEXT,
        )
        allure.attach(driver.get_screenshot_as_png(), "10_Validacion_Tabla", allure.attachment_type.PNG)
