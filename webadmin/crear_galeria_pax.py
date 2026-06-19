import time
import allure
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from helpers import safe_click, safe_send_keys
from pages.webadmin_galeria_pax_page import WebAdminGaleriaPaxPage as P


def _sel_primera(driver, locator):
    """Selecciona la primera opción real (value no vacío) de un <select>."""
    sel = Select(driver.find_element(*locator))
    for o in sel.options:
        if o.get_attribute("value"):
            sel.select_by_value(o.get_attribute("value"))
            return o.text
    return None


@allure.feature("WebAdmin AMV Travel")
@allure.story("Crear Galería de Pax y validar persistencia")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("""
Crea una Galería de Pax (Agencias → Galerías de Pax → Agregar Nueva) y valida la fila
en la tabla tras volver a la lista.
""")
def test_crear_galeria_pax(login_webadmin):
    driver = login_webadmin
    wait = WebDriverWait(driver, 45)

    ahora = datetime.now()
    sello = ahora.strftime('%d/%m/%Y %H:%M:%S')
    nombre = f"Galeria Test {sello}"
    fecha = ahora.strftime('%d/%m/%Y')

    with allure.step("1. Menú Agencias → Galerías de Pax → Agregar Nueva"):
        safe_click(wait, P.MENU_AGENCIAS)
        time.sleep(1)
        safe_click(wait, P.SUBMENU_GALERIAS)
        wait.until(EC.url_contains("/administration/agencies/passengergalleries.aspx"))
        safe_click(wait, P.BTN_NUEVO)
        wait.until(lambda d: "passengergallerydetail.aspx" in d.current_url.lower())
        wait.until(EC.visibility_of_element_located(P.TXT_DETAIL))

    with allure.step("2. Cargar el form"):
        safe_send_keys(wait, P.TXT_DETAIL, nombre)
        _sel_primera(driver, P.DD_AGENCIES)
        el = driver.find_elements(*P.FECHA)
        if el:
            driver.execute_script(
                "arguments[0].value=arguments[1];"
                "arguments[0].dispatchEvent(new Event('change',{bubbles:true}));", el[0], fecha)
        cb = wait.until(EC.presence_of_element_located(P.CB_PUBLICADO))
        if not cb.is_selected():
            driver.execute_script("arguments[0].click();", cb)
        allure.attach(driver.get_screenshot_as_png(), "2_Formulario", allure.attachment_type.PNG)

    with allure.step("3. Guardar"):
        safe_click(wait, P.BTN_GUARDAR)
        time.sleep(2)

    with allure.step("4. Volver a la lista y validar la fila"):
        base = driver.current_url.split("/administration/")[0]
        driver.get(f"{base}/administration/agencies/passengergalleries.aspx")
        wait.until(EC.presence_of_element_located(P.TABLA))
        fila = wait.until(EC.presence_of_element_located(P.fila_por_nombre(sello)))
        assert fila is not None, f"La galería '{nombre}' no aparece en la tabla."
        allure.attach(driver.get_screenshot_as_png(), "4_Validacion_Tabla", allure.attachment_type.PNG)
