import allure
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from helpers import safe_click, safe_send_keys
from pages.webadmin_breakfast_page import WebAdminBreakfastPage as P


@allure.feature("WebAdmin AMV Travel")
@allure.story("Crear Tipo de Desayuno y validar persistencia")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("""
Crea un tipo de desayuno desde el WebAdmin y valida el flujo completo:
1. Navegación Menú -> Hoteles -> Desayuno.
2. Click en Nuevo.
3. Carga del nombre (dinámico con fecha/hora) y las 4 traducciones (ES/EN/PT/IT).
4. Dejar tildado Publicado.
5. Guardado.
6. Validación de que el desayuno recién creado aparece en la tabla.
""")
def test_crear_desayuno(login_webadmin):
    driver = login_webadmin
    wait = WebDriverWait(driver, 45)

    # Nombre dinámico con fecha/hora de ejecución (único por corrida).
    ahora = datetime.now()
    nombre_desayuno = f"Desayuno Test Automático {ahora.strftime('%d/%m/%Y %H:%M:%S')}"

    # Traducciones por idioma (índice del control -> texto).
    traducciones = {
        0: "Este es un test automático",     # Español
        1: "This is an automatic test",      # English
        2: "Este é um teste automático",     # Portugués
        3: "Questo è un test automatico",    # Italiano
    }

    # ==========================================
    # 1-4. NAVEGACIÓN A DESAYUNO
    # ==========================================
    with allure.step("1 a 4. Menú Hoteles -> Desayuno"):
        safe_click(wait, P.MENU_HOTELES)
        # El acordeón del menú tiene animación: esperar el submenú clickeable.
        wait.until(EC.element_to_be_clickable(P.SUBMENU_DESAYUNO))
        safe_click(wait, P.SUBMENU_DESAYUNO)
        wait.until(EC.url_contains("/administration/hotels/breakfasttypes.aspx"))

    # ==========================================
    # 5. NUEVO
    # ==========================================
    with allure.step("5. Click en Nuevo y esperar el formulario"):
        safe_click(wait, P.BTN_NUEVO)
        wait.until(EC.visibility_of_element_located(P.TXT_NAME))

    # ==========================================
    # 6. NOMBRE
    # ==========================================
    with allure.step("6. Cargar el nombre del desayuno"):
        safe_send_keys(wait, P.TXT_NAME, nombre_desayuno)
        allure.attach(
            f"Nombre: {nombre_desayuno}",
            "6_Nombre",
            allure.attachment_type.TEXT,
        )

    # ==========================================
    # 7-10. TRADUCCIONES (ES / EN / PT / IT)
    # ==========================================
    with allure.step("7 a 10. Cargar las 4 traducciones (ES/EN/PT/IT)"):
        for indice, texto in traducciones.items():
            safe_send_keys(wait, P.traduccion(indice), texto)

    # ==========================================
    # 11. PUBLICADO (dejar tildado)
    # ==========================================
    with allure.step("11. Dejar tildado Publicado"):
        cb = wait.until(EC.presence_of_element_located(P.CB_PUBLICADO))
        if not cb.is_selected():
            driver.execute_script("arguments[0].click();", cb)
        allure.attach(driver.get_screenshot_as_png(), "11_Formulario_Completo", allure.attachment_type.PNG)

    # ==========================================
    # 12. GUARDAR
    # ==========================================
    with allure.step("12. Guardar"):
        safe_click(wait, P.BTN_GUARDAR)

    # ==========================================
    # 13. VALIDAR DESAYUNO EN LA TABLA
    # ==========================================
    with allure.step("13. Validar que el desayuno aparece en la tabla"):
        # Guardar dispara un postback async (UpdatePanel) que recarga la grilla:
        # esperar directamente la fila por el nombre completo cubre esa espera.
        wait.until(EC.presence_of_element_located(P.TABLA))
        fila = wait.until(EC.presence_of_element_located(P.fila_por_nombre(nombre_desayuno)))
        assert fila is not None, f"El desayuno '{nombre_desayuno}' no aparece en la tabla."
        allure.attach(
            f"Desayuno encontrado en la tabla: {nombre_desayuno}",
            "13_Desayuno_En_Tabla",
            allure.attachment_type.TEXT,
        )
        allure.attach(driver.get_screenshot_as_png(), "13_Validacion_Tabla", allure.attachment_type.PNG)
