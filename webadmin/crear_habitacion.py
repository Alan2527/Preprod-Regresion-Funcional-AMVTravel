import time
import allure
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from helpers import safe_click, safe_send_keys
from pages.webadmin_room_page import WebAdminRoomPage as P


@allure.feature("WebAdmin AMV Travel")
@allure.story("Crear Habitación y validar persistencia")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("""
Crea una habitación desde el WebAdmin y valida el flujo completo:
1. Navegación Menú → Hoteles → Adm. de Habitaciones → Nuevo.
2. Carga de datos (nombre, hotel, capacidad, tipo, checkboxes).
3. Guardado y validación de la URL de detalle (id dinámico).
4. Validación de que las pestañas del detalle quedan habilitadas.
5. Búsqueda de la habitación recién creada en la tabla.
""")
def test_crear_habitacion(login_webadmin):
    driver = login_webadmin
    wait = WebDriverWait(driver, 45)

    # Nombre dinámico con fecha/hora de ejecución.
    ahora = datetime.now()
    nombre_hab = f"Habitación test automático {ahora.strftime('%d-%m-%Y %H:%M:%S')}"
    # Para buscar usamos el nombre SIN la hora: los ':' rompen el buscador del
    # WebAdmin. Con la fecha alcanza para que la tabla aparezca; luego validamos
    # la fila exacta por el nombre completo.
    nombre_busqueda = f"Habitación test automático {ahora.strftime('%d-%m-%Y')}"

    # ==========================================
    # 1-6. NAVEGACIÓN Y NUEVA HABITACIÓN
    # ==========================================
    with allure.step("1 y 2. Menú Hoteles → Adm. de Habitaciones"):
        safe_click(wait, P.MENU_HOTELES)
        time.sleep(1)  # animación del acordeón del menú
        safe_click(wait, P.SUBMENU_ADM_HAB)
        wait.until(EC.url_contains("/administration/rooms/default.aspx"))

    with allure.step("3 a 5. Click en Nuevo y esperar formulario de detalle"):
        safe_click(wait, P.BTN_NUEVO)
        wait.until(EC.url_contains("/administration/rooms/detail.aspx"))
        wait.until(EC.visibility_of_element_located(P.TXT_NAME))

    # ==========================================
    # 6-13. CARGA DEL FORMULARIO
    # ==========================================
    with allure.step("6 y 7. Nombre y Hotel"):
        safe_send_keys(wait, P.TXT_NAME, nombre_hab)
        Select(wait.until(EC.element_to_be_clickable(P.DD_HOTEL))).select_by_value("15474")
        time.sleep(1)  # seleccionar hotel puede disparar un postback
        allure.attach(driver.get_screenshot_as_png(), "6_Nombre_Hotel", allure.attachment_type.PNG)

    with allure.step("8 a 10. Capacidad, cama extra y tipo de habitación"):
        safe_send_keys(wait, P.TXT_CAPACIDAD, "4")

        # 9. Cama extra (checkbox) -> dejar tildado
        cb_extra = wait.until(EC.presence_of_element_located(P.CB_EXTRA_BED))
        if not cb_extra.is_selected():
            driver.execute_script("arguments[0].click();", cb_extra)

        Select(wait.until(EC.element_to_be_clickable(P.DD_ROOM_TYPE))).select_by_value("1")
        allure.attach(driver.get_screenshot_as_png(), "8_Capacidad_Tipo", allure.attachment_type.PNG)

    with allure.step("11 a 13. Marcar Publicado / Residentes / No residentes"):
        for cb in (P.CB_PUBLICADO, P.CB_FOR_RESIDENTS, P.CB_FOR_NON_RESIDENTS):
            el = wait.until(EC.presence_of_element_located(cb))
            if not el.is_selected():
                driver.execute_script("arguments[0].click();", el)
        allure.attach(driver.get_screenshot_as_png(), "11_Checkboxes", allure.attachment_type.PNG)

    # ==========================================
    # 14-15. EDADES DE MENORES (DESACTIVADO: roto en la app)
    # ==========================================
    # with allure.step("14 y 15. Edades de menores (Desde/Hasta)"):
    #     safe_send_keys(wait, P.DP_KIDS_FROM, "2")
    #     safe_send_keys(wait, P.DP_KIDS_TO, "12")

    # ==========================================
    # 16-17. GUARDAR Y ESPERAR DETALLE CON ID
    # ==========================================
    with allure.step("16 y 17. Guardar y esperar URL de detalle con id dinámico"):
        safe_click(wait, P.BTN_GUARDAR)
        # El id de la habitación es dinámico: validamos el patrón detail.aspx?room=
        wait.until(EC.url_contains("detail.aspx?room="))
        allure.attach(
            f"URL tras guardar: {driver.current_url}",
            "17_URL_Detalle",
            allure.attachment_type.TEXT,
        )
        allure.attach(driver.get_screenshot_as_png(), "17_Habitacion_Guardada", allure.attachment_type.PNG)

    # ==========================================
    # 18. VALIDAR PESTAÑAS HABILITADAS
    # ==========================================
    with allure.step("18. Validar que las pestañas del detalle estén habilitadas"):
        resultados = []
        for nombre_tab in P.TAB_NAMES:
            tab = wait.until(EC.element_to_be_clickable(P.tab_locator(nombre_tab)))
            clases = (tab.get_attribute("class") or "").lower()
            assert "disabled" not in clases, f"La pestaña '{nombre_tab}' está bloqueada (class={clases})"
            assert tab.is_enabled(), f"La pestaña '{nombre_tab}' no está habilitada"
            resultados.append(f"Pestaña OK: {nombre_tab}")
        allure.attach("\n".join(resultados), "18_Pestanas", allure.attachment_type.TEXT)
        allure.attach(driver.get_screenshot_as_png(), "18_Pestanas_Habilitadas", allure.attachment_type.PNG)

    # ==========================================
    # 19-24. VALIDAR HABITACIÓN EN LA TABLA
    # ==========================================
    with allure.step("19 a 21. Volver a Adm. de Habitaciones"):
        safe_click(wait, P.MENU_HOTELES)
        time.sleep(1)
        safe_click(wait, P.SUBMENU_ADM_HAB)
        wait.until(EC.url_contains("/administration/rooms/default.aspx"))

    with allure.step("22 y 23. Buscar la habitación recién creada"):
        safe_send_keys(wait, P.TXT_SEARCH, nombre_busqueda)
        safe_click(wait, P.BTN_SEARCH)
        wait.until(EC.url_contains("default.aspx?word="))

    with allure.step("24. Validar que la habitación aparece en la tabla"):
        wait.until(EC.presence_of_element_located(P.TABLA))
        fila = wait.until(EC.presence_of_element_located(P.fila_por_nombre(nombre_hab)))
        assert fila is not None, f"La habitación '{nombre_hab}' no aparece en la tabla de resultados."
        allure.attach(
            f"Habitación encontrada en la tabla: {nombre_hab}",
            "24_Habitacion_En_Tabla",
            allure.attachment_type.TEXT,
        )
        allure.attach(driver.get_screenshot_as_png(), "24_Validacion_Tabla", allure.attachment_type.PNG)
