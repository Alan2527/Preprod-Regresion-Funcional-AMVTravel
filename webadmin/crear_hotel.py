import time
import allure
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from helpers import safe_click, safe_send_keys
from pages.webadmin_hotel_page import WebAdminHotelPage as P


@allure.feature("WebAdmin AMV Travel")
@allure.story("Crear Hotel y validar persistencia")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("""
Crea un hotel desde el WebAdmin y valida el flujo completo:
1. Navegación Menú → Hoteles → Adm. de Hoteles → Nuevo.
2. Carga de Información General, Configuración, Ubicación y Descripción.
3. Guardado y validación de la URL de detalle (id dinámico).
4. Validación de que las pestañas del detalle quedan habilitadas.
5. Búsqueda del hotel recién creado en la tabla de hoteles.
""")
def test_crear_hotel(login_webadmin):
    driver = login_webadmin
    wait = WebDriverWait(driver, 45)

    # Nombre y descripción dinámicos con fecha/hora de ejecución.
    ahora = datetime.now()
    nombre_hotel = f"Hotel Test Automático {ahora.strftime('%d-%m-%Y %H:%M:%S')}"
    descripcion = f"Test automático corrido el día {ahora.strftime('%d-%m-%Y')} a las {ahora.strftime('%H:%M:%S')}"

    # ==========================================
    # 1-4. NAVEGACIÓN Y NUEVO HOTEL
    # ==========================================
    with allure.step("1 y 2. Menú Hoteles → Adm. de Hoteles"):
        safe_click(wait, P.MENU_HOTELES)
        time.sleep(1)  # animación del acordeón del menú
        safe_click(wait, P.SUBMENU_ADM_HOTELES)
        wait.until(EC.url_contains("/administration/hotels/default.aspx"))

    with allure.step("3 y 4. Click en Nuevo y esperar formulario de detalle"):
        safe_click(wait, P.BTN_NUEVO)
        wait.until(EC.url_contains("/administration/hotels/detail.aspx"))
        wait.until(EC.visibility_of_element_located(P.TXT_NAME))

    # ==========================================
    # 5-9. INFORMACIÓN GENERAL
    # ==========================================
    with allure.step("5 a 9. Información General"):
        safe_send_keys(wait, P.TXT_NAME, nombre_hotel)
        Select(wait.until(EC.element_to_be_clickable(P.DD_CATEGORY))).select_by_value("5")
        safe_send_keys(wait, P.TXT_DISPLAY_ORDER, "1")
        Select(wait.until(EC.element_to_be_clickable(P.DD_BREAKFAST))).select_by_value("7")
        allure.attach(driver.get_screenshot_as_png(), "5_Informacion_General", allure.attachment_type.PNG)

    # ==========================================
    # 10-13. CONFIGURACIÓN Y OPCIONES
    # ==========================================
    with allure.step("10 a 13. Configuración y opciones"):
        # 11. Marcar todos los checkboxes (click por JS para evitar overlays de estilo)
        for cb in P.CHECKBOXES:
            el = wait.until(EC.presence_of_element_located(cb))
            if not el.is_selected():
                driver.execute_script("arguments[0].click();", el)

        safe_send_keys(wait, P.TXT_EMAIL_NOTI, "notif@gmail.com")
        safe_send_keys(wait, P.TXT_OBSERVATION, "Este es un test automático")
        allure.attach(driver.get_screenshot_as_png(), "11_Configuracion", allure.attachment_type.PNG)

    # ==========================================
    # 14-20. UBICACIÓN Y CONTACTO
    # ==========================================
    with allure.step("14 a 20. Ubicación y contacto"):
        safe_send_keys(wait, P.TXT_ADDRESS, "Avenida Test 123")
        Select(wait.until(EC.element_to_be_clickable(P.DD_CITY))).select_by_value("10259")
        time.sleep(1)  # el distrito suele depender de la ciudad (postback)
        Select(wait.until(EC.element_to_be_clickable(P.DD_DISTRICT))).select_by_value("1161")
        safe_send_keys(wait, P.TXT_EMAIL, "testauto@gmail.com")
        safe_send_keys(wait, P.TXT_WEB, "https://test.com.ar/")
        safe_send_keys(wait, P.TXT_ADMIN, "Administrator Test")
        allure.attach(driver.get_screenshot_as_png(), "15_Ubicacion_Contacto", allure.attachment_type.PNG)

    # ==========================================
    # 21-22. DESCRIPCIÓN (Editor Quill)
    # ==========================================
    with allure.step("21 y 22. Descripción del hotel"):
        editor = wait.until(EC.visibility_of_element_located(P.QL_EDITOR))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", editor)
        editor.click()
        editor.send_keys(descripcion)
        allure.attach(driver.get_screenshot_as_png(), "22_Descripcion", allure.attachment_type.PNG)

    # ==========================================
    # 23-24. GUARDAR Y ESPERAR DETALLE CON ID
    # ==========================================
    with allure.step("23 y 24. Guardar y esperar URL de detalle con id dinámico"):
        safe_click(wait, P.BTN_GUARDAR)
        # El id del hotel es dinámico: validamos el patrón detail.aspx?hotel=
        wait.until(EC.url_contains("detail.aspx?hotel="))
        allure.attach(
            f"URL tras guardar: {driver.current_url}",
            "24_URL_Detalle",
            allure.attachment_type.TEXT,
        )
        allure.attach(driver.get_screenshot_as_png(), "24_Hotel_Guardado", allure.attachment_type.PNG)

    # ==========================================
    # 25. VALIDAR PESTAÑAS HABILITADAS
    # ==========================================
    with allure.step("25. Validar que las pestañas del detalle estén habilitadas"):
        resultados = []
        for nombre_tab in P.TAB_NAMES:
            locator = P.tab_locator(nombre_tab)
            tab = wait.until(EC.element_to_be_clickable(locator))
            clases = (tab.get_attribute("class") or "").lower()
            assert "disabled" not in clases, f"La pestaña '{nombre_tab}' está bloqueada (class={clases})"
            assert tab.is_enabled(), f"La pestaña '{nombre_tab}' no está habilitada"
            resultados.append(f"Pestaña OK: {nombre_tab}")
        allure.attach("\n".join(resultados), "25_Pestanas", allure.attachment_type.TEXT)
        allure.attach(driver.get_screenshot_as_png(), "25_Pestanas_Habilitadas", allure.attachment_type.PNG)

    # ==========================================
    # 26-33. VALIDAR HOTEL EN LA TABLA
    # ==========================================
    with allure.step("27 a 29. Volver a Adm. de Hoteles"):
        safe_click(wait, P.MENU_HOTELES)
        time.sleep(1)
        safe_click(wait, P.SUBMENU_ADM_HOTELES)
        wait.until(EC.url_contains("/administration/hotels/default.aspx"))

    with allure.step("30 a 32. Buscar el hotel recién creado"):
        safe_send_keys(wait, P.TXT_SEARCH, nombre_hotel)
        safe_click(wait, P.BTN_SEARCH)
        wait.until(EC.url_contains("default.aspx?word="))

    with allure.step("33. Validar que el hotel aparece en la tabla"):
        wait.until(EC.visibility_of_element_located(P.TABLA))
        fila = wait.until(EC.presence_of_element_located(P.fila_por_nombre(nombre_hotel)))
        assert fila.is_displayed(), f"El hotel '{nombre_hotel}' no aparece en la tabla de resultados."
        allure.attach(
            f"Hotel encontrado en la tabla: {nombre_hotel}",
            "33_Hotel_En_Tabla",
            allure.attachment_type.TEXT,
        )
        allure.attach(driver.get_screenshot_as_png(), "33_Validacion_Tabla", allure.attachment_type.PNG)
