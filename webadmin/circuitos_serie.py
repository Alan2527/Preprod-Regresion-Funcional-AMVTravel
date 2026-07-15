import time
import allure
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from helpers import safe_click, safe_send_keys
from pages.webadmin_serie_page import WebAdminSeriePage as P
from pages.webadmin_tour_page import escribir_quill, validar_solapas


@allure.feature("WebAdmin AMV Travel")
@allure.story("Crear Serie (Circuitos) y validar persistencia")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("""
Crea una Serie desde el WebAdmin (Circuitos → Series) y valida:
1. Navegación y apertura del formulario (Detail.aspx).
2. Carga del Detalle (nombre dinámico, orden, publicado, Nombre y Descripción ES).
3. Guardar y validar que las solapas Detalle/Paquetes/Salidas/Tarifas/Cupos estén habilitadas.
4. Volver a la lista de Series y validar que la serie recién creada aparece.
""")
def test_crear_serie(login_webadmin):
    driver = login_webadmin
    wait = WebDriverWait(driver, 45)

    ahora = datetime.now()
    sello = ahora.strftime('%d/%m/%Y %H:%M:%S')
    nombre = f"Serie Test {sello}"
    texto_quill = f"Test automático corrido el {sello}"
    fecha = ahora.strftime('%d/%m/%Y')

    with allure.step("1. Menú Circuitos → Series → Crear"):
        safe_click(wait, P.MENU_CIRCUITOS)
        time.sleep(1)
        safe_click(wait, P.SUBMENU_SERIES)
        wait.until(EC.url_contains("/administration/series/"))
        safe_click(wait, P.BTN_NUEVO)
        wait.until(lambda d: "detail.aspx" in d.current_url.lower())
        wait.until(EC.visibility_of_element_located(P.TXT_NAME))

    with allure.step("2. Cargar el Detalle (nombre, orden, publicado, Nombre y Descripción ES)"):
        safe_send_keys(wait, P.TXT_NAME, nombre)
        safe_send_keys(wait, P.TXT_ORDEN, "1")
        cb = wait.until(EC.presence_of_element_located(P.CB_PUBLICADO))
        if not cb.is_selected():
            driver.execute_script("arguments[0].click();", cb)
        safe_send_keys(wait, P.NOMBRE_DESC_ES, nombre)
        escribir_quill(driver, wait, P.QUILL_ES, texto_quill)
        allure.attach(driver.get_screenshot_as_png(), "2_Formulario_Completo", allure.attachment_type.PNG)

    with allure.step("3. Guardar"):
        safe_click(wait, P.BTN_GUARDAR)
        time.sleep(2)
        allure.attach(f"URL tras guardar: {driver.current_url}", "3_URL", allure.attachment_type.TEXT)

    with allure.step("4. Validar solapas habilitadas: Detalle, Paquetes, Salidas, Tarifas, Cupos"):
        validar_solapas(driver, P.TAB_CONTAINER,
                        ["Detalle", "Paquetes", "Salidas", "Tarifas", "Cupos"], P.SOLAPAS)
        allure.attach(driver.get_screenshot_as_png(), "4_Solapas", allure.attachment_type.PNG)

    with allure.step("5. Volver a la lista de Series y validar la fila"):
        base = driver.current_url.split("/administration/")[0]
        driver.get(f"{base}/administration/series/")
        safe_send_keys(wait, P.TXT_SEARCH, f"Serie Test {fecha}")
        safe_click(wait, P.BTN_SEARCH)
        time.sleep(1)
        wait.until(EC.presence_of_element_located(P.TABLA))
        fila = wait.until(EC.presence_of_element_located(P.fila_por_nombre(sello)))
        assert fila is not None, f"La serie '{nombre}' no aparece en la tabla."
        allure.attach(driver.get_screenshot_as_png(), "5_Validacion_Tabla", allure.attachment_type.PNG)
