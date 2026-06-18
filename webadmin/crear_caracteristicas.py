import time
import allure
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from helpers import safe_click, safe_send_keys
from pages.webadmin_caracteristica_page import WebAdminCaracteristicaPage as P


@allure.feature("WebAdmin AMV Travel")
@allure.story("Crear Característica y validar persistencia")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("""
Crea una Característica desde el WebAdmin (charasteristicsadmin.aspx) y valida el flujo:
1. Navegación Menú → Servicios → Caracteristicas.
2. Click en "Nuevo" → se despliega el formulario inline.
3. Carga del Nombre (4 idiomas), Detalle (4 idiomas), Orden y Publicado.
4. Guardar.
5. Búsqueda y validación de que la característica recién creada aparece en la tabla.
""")
def test_crear_caracteristicas(login_webadmin):
    driver = login_webadmin
    wait = WebDriverWait(driver, 45)

    ahora = datetime.now()
    sello = ahora.strftime('%d/%m/%Y %H:%M:%S')   # fecha+hora de la corrida (ASCII, único)
    # Prefijo corto: la app trunca el nombre a ~50 chars → así el sello completo persiste.
    PREFIJO = "Caract Test"   # 11 + sello (19) = 30 chars
    nombre_es = f"{PREFIJO} {sello}"

    # Nombre por idioma: ES con el sello (único), resto "test" (como en el form real).
    nombres = {0: nombre_es, 1: "test", 2: "test", 3: "test"}
    # Detalle por idioma (todos requeridos): ES con sello, resto "test".
    detalles = {0: f"Detalle {sello}", 1: "test", 2: "test", 3: "test"}

    # ──────────────────────────────────────────
    # 1. NAVEGACIÓN → CARACTERISTICAS
    # ──────────────────────────────────────────
    with allure.step("1. Menú Servicios → Caracteristicas"):
        safe_click(wait, P.MENU_SERVICIOS)
        time.sleep(1)  # animación acordeón del menú
        safe_click(wait, P.SUBMENU_CARACTERISTICAS)
        wait.until(EC.url_contains("/administration/services/charasteristicsadmin.aspx"))

    # ──────────────────────────────────────────
    # 2. NUEVO (despliega el form inline)
    # ──────────────────────────────────────────
    with allure.step("2. Click en 'Nuevo' y esperar el formulario"):
        safe_click(wait, P.BTN_NUEVO)
        wait.until(EC.visibility_of_element_located(P.nombre(0)))

    # ──────────────────────────────────────────
    # 3. NOMBRE (4 idiomas), DETALLE (4 idiomas) y ORDEN
    # ──────────────────────────────────────────
    with allure.step("3. Cargar Nombre (ES/EN/PT/IT), Detalle (ES/EN/PT/IT) y orden"):
        for indice, texto in nombres.items():
            safe_send_keys(wait, P.nombre(indice), texto)
        for indice, texto in detalles.items():
            safe_send_keys(wait, P.detalle(indice), texto)
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
    with allure.step("6. Buscar y validar que la característica aparece en la tabla"):
        # Gotcha #1: buscar por el nombre SIN la hora (los ':' devuelven 0 resultados).
        nombre_sin_hora = f"{PREFIJO} {ahora.strftime('%d/%m/%Y')}"
        safe_send_keys(wait, P.TXT_SEARCH, nombre_sin_hora)
        safe_click(wait, P.BTN_SEARCH)
        time.sleep(1)  # postback de búsqueda
        wait.until(EC.presence_of_element_located(P.TABLA))
        fila = wait.until(EC.presence_of_element_located(P.fila_por_nombre(sello)))
        assert fila is not None, f"La característica '{nombre_es}' no aparece en la tabla."
        allure.attach(
            f"Característica encontrada en la tabla: {nombre_es}",
            "6_Caracteristica_En_Tabla",
            allure.attachment_type.TEXT,
        )
        allure.attach(driver.get_screenshot_as_png(), "6_Validacion_Tabla", allure.attachment_type.PNG)
