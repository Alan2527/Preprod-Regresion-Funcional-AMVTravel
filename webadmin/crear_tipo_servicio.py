import time
import allure
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from helpers import safe_click, safe_send_keys
from pages.webadmin_tiposervicio_page import WebAdminTipoServicioPage as P


@allure.feature("WebAdmin AMV Travel")
@allure.story("Crear Tipo de servicio y validar persistencia")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("""
Crea un Tipo de servicio desde el WebAdmin (servicetypes.aspx) y valida el flujo:
1. Navegación Menú → Servicios → Tipos de servicio.
2. Click en "Nuevo" → se despliega el formulario inline.
3. Carga del nombre dinámico, las 4 traducciones (ES/EN/PT/IT), el orden y Publicado.
4. Guardar.
5. Búsqueda y validación de que el tipo de servicio recién creado aparece en la tabla.
""")
def test_crear_tipo_servicio(login_webadmin):
    driver = login_webadmin
    wait = WebDriverWait(driver, 45)

    ahora = datetime.now()
    sello = ahora.strftime('%d/%m/%Y %H:%M:%S')   # ASCII y único por corrida
    nombre_tipo = f"Tipo de Servicio Test Automático {sello}"

    # Traducciones por idioma (índice del control → texto).
    traducciones = {
        0: "Este es un test automático",     # Español
        1: "This is an automatic test",      # English
        2: "Este é um teste automático",     # Portugués
        3: "Questo è un test automatico",    # Italiano
    }

    # ──────────────────────────────────────────
    # 1. NAVEGACIÓN → TIPOS DE SERVICIO
    # ──────────────────────────────────────────
    with allure.step("1. Menú Servicios → Tipos de servicio"):
        safe_click(wait, P.MENU_SERVICIOS)
        time.sleep(1)  # animación acordeón del menú
        safe_click(wait, P.SUBMENU_TIPOS)
        wait.until(EC.url_contains("/administration/services/servicetypes.aspx"))

    # ──────────────────────────────────────────
    # 2. NUEVO (despliega el form inline)
    # ──────────────────────────────────────────
    with allure.step("2. Click en 'Nuevo' y esperar el formulario"):
        safe_click(wait, P.BTN_NUEVO)
        wait.until(EC.visibility_of_element_located(P.TXT_NAME))

    # ──────────────────────────────────────────
    # 3. NOMBRE, TRADUCCIONES Y ORDEN
    # ──────────────────────────────────────────
    with allure.step("3. Cargar nombre, traducciones (ES/EN/PT/IT) y orden"):
        safe_send_keys(wait, P.TXT_NAME, nombre_tipo)
        for indice, texto in traducciones.items():
            safe_send_keys(wait, P.traduccion(indice), texto)
        safe_send_keys(wait, P.TXT_ORDEN, "1")
        allure.attach(driver.get_screenshot_as_png(), "3_Formulario_Completo", allure.attachment_type.PNG)

    # ──────────────────────────────────────────
    # 4. PUBLICADO (dejar tildado)
    # ──────────────────────────────────────────
    with allure.step("4. Verificar Publicado tildado"):
        cb = wait.until(EC.presence_of_element_located(P.CB_PUBLICADO))
        if not cb.is_selected():
            driver.execute_script("arguments[0].click();", cb)

    # ──────────────────────────────────────────
    # 5. GUARDAR
    # ──────────────────────────────────────────
    with allure.step("5. Guardar"):
        safe_click(wait, P.BTN_GUARDAR)
        time.sleep(1)  # postback de guardado (recarga la lista)

    # ──────────────────────────────────────────
    # 6. BUSCAR Y VALIDAR EN LA TABLA
    # ──────────────────────────────────────────
    with allure.step("6. Buscar y validar que el tipo de servicio aparece en la tabla"):
        # Gotcha #1: buscar por el nombre SIN la hora (los ':' devuelven 0 resultados).
        nombre_sin_hora = f"Tipo de Servicio Test Automático {ahora.strftime('%d/%m/%Y')}"
        safe_send_keys(wait, P.TXT_SEARCH, nombre_sin_hora)
        safe_click(wait, P.BTN_SEARCH)
        time.sleep(1)  # postback de búsqueda
        wait.until(EC.presence_of_element_located(P.TABLA))
        fila = wait.until(EC.presence_of_element_located(P.fila_por_nombre(sello)))
        assert fila is not None, f"El tipo de servicio '{nombre_tipo}' no aparece en la tabla."
        allure.attach(
            f"Tipo de servicio encontrado en la tabla: {nombre_tipo}",
            "6_Tipo_En_Tabla",
            allure.attachment_type.TEXT,
        )
        allure.attach(driver.get_screenshot_as_png(), "6_Validacion_Tabla", allure.attachment_type.PNG)
