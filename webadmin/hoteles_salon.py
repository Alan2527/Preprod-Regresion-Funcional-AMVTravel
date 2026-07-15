import time
import allure
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from helpers import safe_click, safe_send_keys
from pages.webadmin_salon_page import WebAdminSalonPage as P


def _escribir_quill(driver, wait, locator, texto):
    """Escribe en un editor Quill (div.ql-editor contenteditable, no es input).
    Hace foco con click y tipea; el text-change de Quill sincroniza el hidden."""
    editor = wait.until(EC.visibility_of_element_located(locator))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", editor)
    editor.click()
    editor.send_keys(texto)


@allure.feature("WebAdmin AMV Travel")
@allure.story("Crear Salón y validar persistencia")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("""
Crea un salón (meeting salon) desde el WebAdmin y valida el flujo completo:
1. Navegación Menú -> Hoteles -> Salones -> Nuevo.
2. Selección de Ciudad (dispara postback que recarga los Hoteles).
3. Carga de nombre dinámico, capacidad (200) y orden.
4. Selección del Hotel dependiente de la ciudad.
5. Dejar tildado Publicado y Guardar.
6. Validación de que el salón recién creado aparece en la tabla.
""")
def test_crear_salon(login_webadmin):
    driver = login_webadmin
    wait = WebDriverWait(driver, 45)

    # Nombre dinámico con fecha/hora de ejecución (único por corrida).
    ahora = datetime.now()
    sello = ahora.strftime('%d/%m/%Y %H:%M:%S')   # ASCII y único por corrida
    nombre_salon = f"Salón Test Automático {sello}"

    # ==========================================
    # 1-4. NAVEGACIÓN A SALONES -> NUEVO
    # ==========================================
    with allure.step("1 a 4. Menú Hoteles -> Salones -> Nuevo"):
        safe_click(wait, P.MENU_HOTELES)
        wait.until(EC.element_to_be_clickable(P.SUBMENU_SALONES))
        safe_click(wait, P.SUBMENU_SALONES)
        wait.until(EC.url_contains("/administration/meetingsalons"))
        safe_click(wait, P.BTN_NUEVO)
        wait.until(EC.url_contains("detail.aspx"))
        # El TabContainer arranca oculto (visibility:hidden) y el JS lo muestra:
        # esperar a que el primer campo sea visible antes de interactuar.
        wait.until(EC.visibility_of_element_located(P.DD_CITY))

    # ==========================================
    # 5. CIUDAD (dispara postback que recarga los hoteles)
    # ==========================================
    with allure.step("5. Seleccionar Ciudad 'Cachi | Argentina' (postback)"):
        Select(wait.until(EC.element_to_be_clickable(P.DD_CITY))).select_by_visible_text("Cachi | Argentina")
        time.sleep(1)  # el onchange dispara un postback (full) que recarga hoteles
        # Esperar a que el hotel dependiente aparezca en el select recargado.
        wait.until(EC.presence_of_element_located(P.hotel_option("Hosteria Cachi")))

    # ==========================================
    # 6-8. NOMBRE, CAPACIDAD Y ORDEN
    # ==========================================
    with allure.step("6 a 8. Cargar nombre, capacidad (200) y orden"):
        safe_send_keys(wait, P.TXT_NAME, nombre_salon)
        safe_send_keys(wait, P.TXT_CAPACITY, "200")
        safe_send_keys(wait, P.TXT_ORDER, "1")
        allure.attach(
            f"Nombre: {nombre_salon}\nCapacidad: 200\nOrden: 1",
            "6_Datos",
            allure.attachment_type.TEXT,
        )

    # ==========================================
    # 9. HOTEL (dependiente de la ciudad)
    # ==========================================
    with allure.step("9. Seleccionar Hotel 'Hosteria Cachi'"):
        opt = wait.until(EC.presence_of_element_located(P.hotel_option("Hosteria Cachi")))
        Select(driver.find_element(*P.DD_HOTEL)).select_by_value(opt.get_attribute("value"))
        allure.attach(driver.get_screenshot_as_png(), "9_Formulario_Completo", allure.attachment_type.PNG)

    # ==========================================
    # 10. DESCRIPCIÓN Y ESPECIFICACIONES (editores Quill, pestaña ES)
    # ==========================================
    with allure.step("10. Cargar Descripción y Especificaciones (ES)"):
        # "Nombre" localizado del bloque Descripción (input normal).
        safe_send_keys(wait, P.DESC_NOMBRE_ES, nombre_salon)
        # Editores enriquecidos (Quill): se tipea en el div.ql-editor.
        _escribir_quill(driver, wait, P.DESC_QUILL_ES,
                        "Nuestro compromiso: servicio especializado y experiencias a medida. Test automatico.")
        _escribir_quill(driver, wait, P.ESP_QUILL_ES,
                        "Capacidad para 200 personas. Salon completo 240 m2. Servicio de Coffee Break. Test automatico.")
        allure.attach(driver.get_screenshot_as_png(), "10_Descripcion_Especificaciones", allure.attachment_type.PNG)

    # ==========================================
    # 11. PUBLICADO (dejar tildado)
    # ==========================================
    with allure.step("11. Dejar tildado Publicado"):
        cb = wait.until(EC.presence_of_element_located(P.CB_PUBLICADO))
        if not cb.is_selected():
            driver.execute_script("arguments[0].click();", cb)

    # ==========================================
    # 12. GUARDAR
    # ==========================================
    with allure.step("12. Guardar"):
        safe_click(wait, P.BTN_GUARDAR)
        time.sleep(1)  # dar tiempo al postback de guardado

    # ==========================================
    # 13. VOLVER A LA LISTA DE SALONES
    # ==========================================
    with allure.step("13. Volver a la lista de Salones"):
        # El alta guarda y queda en detail.aspx (no tiene tabla). En esa pantalla el
        # menú "Hoteles" ya está ABIERTO, así que clickeamos directo el span "Salones"
        # (NO el padre, que colapsaría el acordeón y ocultaría el submenú).
        safe_click(wait, P.SUBMENU_SALONES)
        # Esperar a que cargue la lista (meetingsalons/), distinta de detail.aspx.
        wait.until(lambda d: "/administration/meetingsalons/" in d.current_url
                   and "detail.aspx" not in d.current_url)

    # ==========================================
    # 14. VALIDAR SALÓN EN LA TABLA
    # ==========================================
    with allure.step("14. Validar que el salón aparece en la tabla"):
        wait.until(EC.presence_of_element_located(P.TABLA))
        # Buscamos por el sello de fecha/hora (ASCII y único por corrida) para evitar
        # problemas de acentos / normalizacion Unicode al matchear el texto del td.
        fila = wait.until(EC.presence_of_element_located(P.fila_por_nombre(sello)))
        assert fila is not None, f"El salón '{nombre_salon}' no aparece en la tabla."
        allure.attach(
            f"Salón encontrado en la tabla: {nombre_salon}",
            "14_Salon_En_Tabla",
            allure.attachment_type.TEXT,
        )
        allure.attach(driver.get_screenshot_as_png(), "14_Validacion_Tabla", allure.attachment_type.PNG)
