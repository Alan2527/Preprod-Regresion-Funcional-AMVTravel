import allure
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from helpers import safe_click, safe_send_keys
from pages.webadmin_category_page import WebAdminCategoryPage as P


@allure.feature("WebAdmin AMV Travel")
@allure.story("Crear Categoría y validar persistencia")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("""
Crea una categoría de hotel desde el WebAdmin y valida el flujo completo:
1. Navegación Menú -> Hoteles -> Categorías.
2. Click en Nuevo.
3. Carga del nombre (dinámico con fecha/hora), el orden y las 4 traducciones (ES/EN/PT/IT).
4. Guardado.
5. Validación de que la categoría recién creada aparece en la tabla.
""")
def test_crear_categoria(login_webadmin):
    driver = login_webadmin
    wait = WebDriverWait(driver, 45)

    # Nombre dinámico con fecha/hora de ejecución (único por corrida).
    ahora = datetime.now()
    nombre_categoria = f"Categoría Test Automático {ahora.strftime('%d/%m/%Y %H:%M:%S')}"

    # Traducciones por idioma (índice del control -> texto).
    traducciones = {
        0: "Este es un test automático",     # Español
        1: "This is an automatic test",      # English
        2: "Este é um teste automático",     # Portugués
        3: "Questo è un test automatico",    # Italiano
    }

    # ==========================================
    # 1-4. NAVEGACIÓN A CATEGORÍAS
    # ==========================================
    with allure.step("1 a 4. Menú Hoteles -> Categorías"):
        safe_click(wait, P.MENU_HOTELES)
        # El acordeón del menú tiene animación: esperar el submenú clickeable.
        wait.until(EC.element_to_be_clickable(P.SUBMENU_CATEGORIAS))
        safe_click(wait, P.SUBMENU_CATEGORIAS)
        wait.until(EC.url_contains("/administration/hotels/hotelcategories.aspx"))

    # ==========================================
    # 5-6. NUEVO
    # ==========================================
    with allure.step("5 y 6. Click en Nuevo y esperar el formulario"):
        safe_click(wait, P.BTN_NUEVO)
        wait.until(EC.visibility_of_element_located(P.TXT_NAME))

    # ==========================================
    # 7-8. NOMBRE Y ORDEN
    # ==========================================
    with allure.step("7 y 8. Cargar nombre y orden"):
        safe_send_keys(wait, P.TXT_NAME, nombre_categoria)
        safe_send_keys(wait, P.TXT_ORDER, "1")
        allure.attach(
            f"Nombre: {nombre_categoria}\nOrden: 1",
            "7_Nombre_Orden",
            allure.attachment_type.TEXT,
        )

    # ==========================================
    # 9-10. TRADUCCIONES (ES / EN / PT / IT)
    # ==========================================
    with allure.step("9 y 10. Cargar las 4 traducciones (ES/EN/PT/IT)"):
        for indice, texto in traducciones.items():
            safe_send_keys(wait, P.traduccion(indice), texto)
        allure.attach(driver.get_screenshot_as_png(), "10_Formulario_Completo", allure.attachment_type.PNG)

    # ==========================================
    # 11. GUARDAR
    # ==========================================
    with allure.step("11. Guardar"):
        safe_click(wait, P.BTN_GUARDAR)

    # ==========================================
    # 12. VALIDAR CATEGORÍA EN LA TABLA
    # ==========================================
    with allure.step("12. Validar que la categoría aparece en la tabla"):
        # Guardar dispara un postback async (UpdatePanel) que recarga la grilla:
        # esperar directamente la fila por el nombre completo cubre esa espera.
        wait.until(EC.presence_of_element_located(P.TABLA))
        fila = wait.until(EC.presence_of_element_located(P.fila_por_nombre(nombre_categoria)))
        assert fila is not None, f"La categoría '{nombre_categoria}' no aparece en la tabla."
        allure.attach(
            f"Categoría encontrada en la tabla: {nombre_categoria}",
            "12_Categoria_En_Tabla",
            allure.attachment_type.TEXT,
        )
        allure.attach(driver.get_screenshot_as_png(), "12_Validacion_Tabla", allure.attachment_type.PNG)
