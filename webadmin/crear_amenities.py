import allure
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from helpers import safe_click, safe_send_keys
from pages.webadmin_amenities_page import WebAdminAmenitiesPage as P


@allure.feature("WebAdmin AMV Travel")
@allure.story("Crear Amenitie y validar persistencia")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("""
Crea una amenitie desde el WebAdmin y valida el flujo completo:
1. Navegacion Menu -> Hoteles -> Amenities.
2. Click en Nuevo.
3. Carga del nombre (dinamico con fecha/hora) y las 4 traducciones (ES/EN/PT/IT).
4. Guardado.
5. Validacion de que la amenitie recien creada aparece en la tabla.
""")
def test_crear_amenitie(login_webadmin):
    driver = login_webadmin
    wait = WebDriverWait(driver, 45)

    # Nombre dinamico con fecha/hora de ejecucion (unico por corrida).
    ahora = datetime.now()
    nombre_amenitie = f"Amenitie Test Automatico {ahora.strftime('%d/%m/%Y %H:%M:%S')}"

    # Traducciones por idioma (indice del control -> texto).
    traducciones = {
        0: "Este es un test automatico",    # Espanol
        1: "This is an automatic test",     # English
        2: "Este e um teste automatico",    # Portugues
        3: "Questo e un test automatico",   # Italiano
    }

    # ==========================================
    # 1-4. NAVEGACION A AMENITIES
    # ==========================================
    with allure.step("1 a 4. Menu Hoteles -> Amenities"):
        safe_click(wait, P.MENU_HOTELES)
        # El acordeon del menu tiene animacion: dar tiempo antes del submenu.
        wait.until(EC.element_to_be_clickable(P.SUBMENU_AMENITIES))
        safe_click(wait, P.SUBMENU_AMENITIES)
        wait.until(EC.url_contains("/administration/types/amenities.aspx"))

    # ==========================================
    # 5. NUEVO
    # ==========================================
    with allure.step("5. Click en Nuevo y esperar el formulario"):
        safe_click(wait, P.BTN_NUEVO)
        wait.until(EC.visibility_of_element_located(P.TXT_NAME))

    # ==========================================
    # 6. NOMBRE
    # ==========================================
    with allure.step("6. Cargar el nombre de la amenitie"):
        safe_send_keys(wait, P.TXT_NAME, nombre_amenitie)
        allure.attach(
            f"Nombre: {nombre_amenitie}",
            "6_Nombre",
            allure.attachment_type.TEXT,
        )

    # ==========================================
    # 7-10. TRADUCCIONES (ES / EN / PT / IT)
    # ==========================================
    with allure.step("7 a 10. Cargar las 4 traducciones (ES/EN/PT/IT)"):
        for indice, texto in traducciones.items():
            safe_send_keys(wait, P.traduccion(indice), texto)
        allure.attach(driver.get_screenshot_as_png(), "10_Formulario_Completo", allure.attachment_type.PNG)

    # ==========================================
    # 11. GUARDAR
    # ==========================================
    with allure.step("11. Guardar"):
        safe_click(wait, P.BTN_GUARDAR)

    # ==========================================
    # 12. VALIDAR AMENITIE EN LA TABLA
    # ==========================================
    with allure.step("12. Validar que la amenitie aparece en la tabla"):
        # Guardar dispara un postback async (UpdatePanel) que recarga la grilla:
        # esperar directamente la fila por el nombre completo cubre esa espera.
        wait.until(EC.presence_of_element_located(P.TABLA))
        fila = wait.until(EC.presence_of_element_located(P.fila_por_nombre(nombre_amenitie)))
        assert fila is not None, f"La amenitie '{nombre_amenitie}' no aparece en la tabla."
        allure.attach(
            f"Amenitie encontrada en la tabla: {nombre_amenitie}",
            "12_Amenitie_En_Tabla",
            allure.attachment_type.TEXT,
        )
        allure.attach(driver.get_screenshot_as_png(), "12_Validacion_Tabla", allure.attachment_type.PNG)
