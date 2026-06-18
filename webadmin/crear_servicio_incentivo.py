import time
import allure
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from helpers import safe_click, safe_send_keys
from pages.webadmin_servicio_incentivo_page import WebAdminServicioIncentivoPage as P


def _escribir_quill(driver, wait, locator, texto):
    """Escribe en un editor Quill (div.ql-editor contenteditable, no input)."""
    editor = wait.until(EC.visibility_of_element_located(locator))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", editor)
    editor.click()
    editor.send_keys(texto)


@allure.feature("WebAdmin AMV Travel")
@allure.story("Crear Servicio de incentivo y validar persistencia")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("""
Crea un Servicio de incentivo desde el WebAdmin (incentives/servicedetail.aspx) y valida:
1. Navegación Menú → Servicios → Servicios de incentivo → "+ Agregar Servicio".
2. Carga del nombre dinámico, Ciudad, Servicio Relacionado, Tipo, Destino, Orden,
   Destacado, Publicado y el Detalle de Incentivos (Nombre ES + Quill ES).
3. Guardar.
4. Validación de que el servicio recién creado aparece en la tabla.
""")
def test_crear_servicio_incentivo(login_webadmin):
    driver = login_webadmin
    wait = WebDriverWait(driver, 45)

    ahora = datetime.now()
    sello = ahora.strftime('%d/%m/%Y %H:%M:%S')   # fecha+hora de la corrida (ASCII, único)
    # Prefijo corto + sello (regla del truncado a ~50 chars).
    PREFIJO = "Serv Incentivo Test"   # 19 + sello (19) = 39 chars
    nombre_incentivo = f"{PREFIJO} {sello}"
    texto_quill = f"Test automático corrido el {sello}"

    # ──────────────────────────────────────────
    # 1. NAVEGACIÓN → SERVICIOS DE INCENTIVO → AGREGAR
    # ──────────────────────────────────────────
    with allure.step("1. Menú Servicios → Servicios de incentivo"):
        safe_click(wait, P.MENU_SERVICIOS)
        time.sleep(1)  # animación acordeón del menú
        safe_click(wait, P.SUBMENU_INCENTIVOS)
        wait.until(EC.url_contains("/administration/incentives/Servicedefault.aspx"))

    with allure.step("2. Click en '+ Agregar Servicio' y esperar el formulario"):
        safe_click(wait, P.BTN_AGREGAR)
        wait.until(EC.url_contains("/administration/incentives/servicedetail.aspx"))
        wait.until(EC.visibility_of_element_located(P.TXT_NAME))

    # ──────────────────────────────────────────
    # 3. DATOS PRINCIPALES
    # ──────────────────────────────────────────
    with allure.step("3. Ciudad (postback), luego Nombre, Servicio Relacionado, Tipo, Destino y Orden"):
        # ⚠ Ciudad (ddlCity) dispara AutoPostBack que recarga el form → se elige PRIMERO
        #   para no perder el resto de los campos en el postback.
        Select(wait.until(EC.element_to_be_clickable(P.DD_CITY))).select_by_visible_text("Cachi")
        time.sleep(1)
        # Esperar a que el servicio dependiente aparezca tras el postback de ciudad.
        wait.until(EC.presence_of_element_located(P.opcion_service("Experiencia Colomé")))
        # Ahora sí cargamos el resto (ya pasó el postback).
        safe_send_keys(wait, P.TXT_NAME, nombre_incentivo)
        Select(driver.find_element(*P.DD_SERVICE)).select_by_visible_text("Experiencia Colomé")
        Select(wait.until(EC.element_to_be_clickable(P.DD_TYPE))).select_by_visible_text("Excursión")
        Select(wait.until(EC.element_to_be_clickable(P.DD_DESTINATION))).select_by_visible_text("Buenos Aires")
        safe_send_keys(wait, P.TXT_ORDEN, "1")
        allure.attach(driver.get_screenshot_as_png(), "3_Datos_Principales", allure.attachment_type.PNG)

    # ──────────────────────────────────────────
    # 4. DESTACADO Y PUBLICADO (dejar tildados)
    # ──────────────────────────────────────────
    with allure.step("4. Destacado y Publicado tildados"):
        for loc in (P.CB_DESTACADO, P.CB_PUBLICADO):
            cb = wait.until(EC.presence_of_element_located(loc))
            if not cb.is_selected():
                driver.execute_script("arguments[0].click();", cb)

    # ──────────────────────────────────────────
    # 5. DETALLE DE INCENTIVOS (ES): Nombre + Quill
    # ──────────────────────────────────────────
    with allure.step("5. Detalle de Incentivos (ES): Nombre y Quill"):
        safe_send_keys(wait, P.DETALLE_NOMBRE_ES, nombre_incentivo)
        _escribir_quill(driver, wait, P.QUILL_ES, texto_quill)
        allure.attach(driver.get_screenshot_as_png(), "5_Detalle_Incentivos", allure.attachment_type.PNG)

    # ──────────────────────────────────────────
    # 6. GUARDAR
    # ──────────────────────────────────────────
    with allure.step("6. Guardar"):
        safe_click(wait, P.BTN_GUARDAR)
        time.sleep(2)  # postback de guardado
        allure.attach(f"URL tras guardar: {driver.current_url}", "6_URL_PostGuardado",
                      allure.attachment_type.TEXT)

    # ──────────────────────────────────────────
    # 7. VALIDAR EN LA TABLA
    # ──────────────────────────────────────────
    with allure.step("7. Validar que el servicio de incentivo aparece en la tabla"):
        # La lista no tiene buscador → re-navegamos a la lista fresca y validamos la fila.
        base = driver.current_url.split("/administration/")[0]
        driver.get(f"{base}/administration/incentives/Servicedefault.aspx")
        wait.until(EC.presence_of_element_located(P.TABLA))
        fila = wait.until(EC.presence_of_element_located(P.fila_por_nombre(sello)))
        assert fila is not None, f"El servicio de incentivo '{nombre_incentivo}' no aparece en la tabla."
        # Diagnóstico: adjuntar la fila COMPLETA (incluye el ID real) para verificar en preprod.
        try:
            row = fila.find_element(By.XPATH, "./ancestor::tr[1]")
            allure.attach(row.text, "7_Fila_Encontrada (ID + datos)", allure.attachment_type.TEXT)
        except Exception:
            pass
        allure.attach(
            f"Servicio de incentivo encontrado en la tabla: {nombre_incentivo}",
            "7_Incentivo_En_Tabla",
            allure.attachment_type.TEXT,
        )
        allure.attach(driver.get_screenshot_as_png(), "7_Validacion_Tabla", allure.attachment_type.PNG)
