import time
import allure
from datetime import datetime, timedelta
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from helpers import safe_click, safe_send_keys
from pages.webadmin_tour_page import (
    WebAdminTourPage as P, llenar_tour, validar_solapas,
)


@allure.feature("WebAdmin AMV Travel")
@allure.story("Crear Oportunidad (Circuitos) y validar persistencia")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("""
Crea una Oportunidad desde el WebAdmin (Circuitos → Oportunidades) y valida:
1. Navegación y apertura del formulario (detail.aspx).
2. Carga de los campos del Detalle (nombre dinámico, vigencia, tarifas, etc.).
3. Guardar y validar solapas habilitadas: Detalle/Imagenes/Destinos + Agencias.
   (Oportunidades NO tiene solapa Videos; en su lugar tiene Agencias.)
4. Volver a la lista y validar que la oportunidad recién creada aparece.
""")
def test_crear_oportunidad(login_webadmin):
    driver = login_webadmin
    wait = WebDriverWait(driver, 45)

    ahora = datetime.now()
    sello = ahora.strftime('%d/%m/%Y %H:%M:%S')
    nombre = f"Oport Test {sello}"
    texto_quill = f"Test automático corrido el {sello}"
    fecha_desde = ahora.strftime('%d/%m/%Y')
    fecha_hasta = (ahora + timedelta(days=180)).strftime('%d/%m/%Y')

    with allure.step("1. Menú Circuitos → Oportunidades → Crear"):
        safe_click(wait, P.MENU_CIRCUITOS)
        time.sleep(1)
        safe_click(wait, P.SUBMENU_OPORTUNIDADES)
        wait.until(EC.url_contains("/administration/opportunities/"))
        safe_click(wait, P.BTN_NUEVO)
        wait.until(lambda d: "detail.aspx" in d.current_url.lower())
        wait.until(EC.visibility_of_element_located(P.TXT_NAME))

    with allure.step("2. Cargar los campos del Detalle"):
        llenar_tour(driver, wait, nombre, texto_quill, fecha_desde, fecha_hasta)
        allure.attach(driver.get_screenshot_as_png(), "2_Formulario_Completo", allure.attachment_type.PNG)

    with allure.step("3. Guardar"):
        safe_click(wait, P.BTN_GUARDAR)
        time.sleep(2)
        allure.attach(f"URL tras guardar: {driver.current_url}", "3_URL", allure.attachment_type.TEXT)

    with allure.step("4. Validar solapas habilitadas: Detalle, Imagenes, Destinos, Agencias"):
        validar_solapas(driver, P.TAB_CONTAINER,
                        ["Detalle", "Imagenes", "Destinos", "Agencias"], P.SOLAPAS)
        allure.attach(driver.get_screenshot_as_png(), "4_Solapas", allure.attachment_type.PNG)

    with allure.step("5. Volver a la lista de Oportunidades y validar la fila"):
        base = driver.current_url.split("/administration/")[0]
        driver.get(f"{base}/administration/opportunities/default.aspx")
        safe_send_keys(wait, P.TXT_SEARCH, f"Oport Test {fecha_desde}")
        safe_click(wait, P.BTN_SEARCH)
        time.sleep(1)
        wait.until(EC.presence_of_element_located(P.TABLA))
        fila = wait.until(EC.presence_of_element_located(P.fila_por_nombre(sello)))
        assert fila is not None, f"La oportunidad '{nombre}' no aparece en la tabla."
        allure.attach(driver.get_screenshot_as_png(), "5_Validacion_Tabla", allure.attachment_type.PNG)
