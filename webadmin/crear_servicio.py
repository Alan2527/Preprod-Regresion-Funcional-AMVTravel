import time
import allure
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from helpers import safe_click, safe_send_keys
from pages.webadmin_servicio_page import WebAdminServicioPage as P


def _escribir_quill(driver, wait, locator, texto):
    """Escribe en un editor Quill (div.ql-editor contenteditable)."""
    editor = wait.until(EC.visibility_of_element_located(locator))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", editor)
    editor.click()
    editor.send_keys(texto)


def _tomselect_add(driver, select_id, *textos):
    """Selecciona opciones en un TomSelect multiselect usando la API JS del widget."""
    for texto in textos:
        driver.execute_script("""
            var sel = document.getElementById(arguments[0]);
            var ts = sel && sel.tomselect;
            if (!ts) return;
            var opt = [...sel.options].find(o => o.text.trim().includes(arguments[1]));
            if (opt) ts.addItem(opt.value, true);
        """, select_id, texto)


@allure.feature("WebAdmin AMV Travel")
@allure.story("Crear Servicio y validar persistencia")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("""
Crea un servicio (Excursión) desde el WebAdmin y valida el flujo completo:
1. Navegación Menú → Servicios → Adm. de servicios → Crear servicio.
2. Carga de todos los campos: nombre dinámico, tipo Excursión, ciudad Cachi,
   orden, observaciones, publicado, emails, vidriera, idiomas, tags,
   opcionales, edades, cancelable, horas antes, y 6 editores Quill (ES).
3. Guardado y validación de la URL de detalle con id dinámico.
4. Validación de que las pestañas del detalle estén habilitadas (sin disabled).
5. Regreso a Adm. de servicios y validación de la fila en la tabla.
""")
def test_crear_servicio(login_webadmin):
    driver = login_webadmin
    wait = WebDriverWait(driver, 45)

    ahora = datetime.now()
    sello = ahora.strftime('%d/%m/%Y %H:%M:%S')
    nombre_servicio = f"Servicio Test Automático {sello}"
    texto_quill = (f"Test automático corrido el día "
                   f"{ahora.strftime('%d/%m/%Y')} a las {ahora.strftime('%H:%M:%S')}")

    # ──────────────────────────────────────────
    # 1-2. NAVEGACIÓN → CREAR SERVICIO
    # ──────────────────────────────────────────
    with allure.step("1. Menú Servicios → Adm. de servicios"):
        safe_click(wait, P.MENU_SERVICIOS)
        time.sleep(1)  # animación acordeón del menú
        safe_click(wait, P.SUBMENU_ADM_SERVICIOS)
        wait.until(EC.url_contains("/administration/services/default.aspx"))

    with allure.step("2. Click en Crear servicio y esperar formulario"):
        safe_click(wait, P.BTN_CREAR)
        wait.until(lambda d: "services/detail.aspx" in d.current_url.lower())
        wait.until(EC.visibility_of_element_located(P.TXT_NAME))

    # ──────────────────────────────────────────
    # 3-7. DATOS PRINCIPALES
    # ──────────────────────────────────────────
    with allure.step("3 a 7. Nombre, Tipo, Ciudad, Orden y Observaciones"):
        safe_send_keys(wait, P.TXT_NAME, nombre_servicio)
        Select(wait.until(EC.element_to_be_clickable(P.DD_TYPE))).select_by_visible_text("Excursión")
        Select(wait.until(EC.element_to_be_clickable(P.DD_CITY))).select_by_visible_text("Cachi")
        time.sleep(1)  # ddlCities puede disparar postback
        safe_send_keys(wait, P.TXT_ORDEN, "2")
        safe_send_keys(wait, P.TXT_COMMENT, "Este es un test automático")
        allure.attach(driver.get_screenshot_as_png(), "3_Datos_Principales", allure.attachment_type.PNG)

    # ──────────────────────────────────────────
    # 8. PUBLICADO (dejar tildado)
    # ──────────────────────────────────────────
    with allure.step("8. Verificar Publicado tildado"):
        cb = wait.until(EC.presence_of_element_located(P.CB_PUBLICADO))
        if not cb.is_selected():
            driver.execute_script("arguments[0].click();", cb)

    # ──────────────────────────────────────────
    # 9-10. EMAILS
    # ──────────────────────────────────────────
    with allure.step("9 y 10. Email servicio y Email extra"):
        safe_send_keys(wait, P.TXT_EMAIL_SERVICIO, "testauto@gmail.com")
        # txtEmailNoti tiene readonly en el DOM → se fuerza vía JS
        elem_extra = wait.until(EC.presence_of_element_located(P.TXT_EMAIL_EXTRA))
        driver.execute_script(
            "var el=arguments[0]; el.removeAttribute('readonly'); el.removeAttribute('disabled');"
            "el.value=arguments[1];"
            "el.dispatchEvent(new Event('input',{bubbles:true}));"
            "el.dispatchEvent(new Event('change',{bubbles:true}));",
            elem_extra, "testauto2@gmail.com"
        )

    # ──────────────────────────────────────────
    # 11. MOSTRAR EN VIDRIERA
    # ──────────────────────────────────────────
    with allure.step("11. Marcar Mostrar en vidriera"):
        cb = wait.until(EC.presence_of_element_located(P.CB_VIDRIERA))
        if not cb.is_selected():
            driver.execute_script("arguments[0].click();", cb)

    # ──────────────────────────────────────────
    # 12. IDIOMA (TomSelect multiselect)
    # ──────────────────────────────────────────
    with allure.step("12. Idioma: Español y English"):
        _tomselect_add(driver, P.LB_LANGUAGES_ID, "Español", "English")
        allure.attach(driver.get_screenshot_as_png(), "12_Idioma", allure.attachment_type.PNG)

    # ──────────────────────────────────────────
    # 13. TAGS (TomSelect, id="lbTags")
    # ──────────────────────────────────────────
    with allure.step("13. Tags: Test"):
        _tomselect_add(driver, P.LB_TAGS_ID, "Test")

    # ──────────────────────────────────────────
    # 14-15. OPCIONALES
    # ──────────────────────────────────────────
    with allure.step("14 y 15. Opcional Regular y Opcional Privado"):
        for loc in (P.CB_OPCIONAL_REG, P.CB_OPCIONAL_PRIV):
            cb = wait.until(EC.presence_of_element_located(loc))
            if not cb.is_selected():
                driver.execute_script("arguments[0].click();", cb)

    # ──────────────────────────────────────────
    # 16-20. EDADES, CANCELABLE Y HORAS
    # ──────────────────────────────────────────
    with allure.step("16 a 20. Edades, Gratis hasta, Cancelable y Horas antes"):
        safe_send_keys(wait, P.TXT_EDAD_DESDE,   "1")
        safe_send_keys(wait, P.TXT_EDAD_HASTA,   "17")
        safe_send_keys(wait, P.TXT_GRATIS_HASTA, "4")
        cb = wait.until(EC.presence_of_element_located(P.CB_CANCELABLE))
        if not cb.is_selected():
            driver.execute_script("arguments[0].click();", cb)
        safe_send_keys(wait, P.TXT_HORAS_ANTES, "24")
        allure.attach(driver.get_screenshot_as_png(), "16_Edades_Cancel", allure.attachment_type.PNG)

    # ──────────────────────────────────────────
    # 21-26. EDITORES QUILL (pestaña ES = ctl00)
    # ──────────────────────────────────────────
    with allure.step("21 a 26. Quill: Introducción, Detalle, Nombre y Descripción, "
                     "Política de Cancelación, Punto de Encuentro, Punto de Destino"):
        _escribir_quill(driver, wait, P.QUILL_INTRO,     texto_quill)
        _escribir_quill(driver, wait, P.QUILL_DETALLE,   texto_quill)
        safe_send_keys(wait, P.QUILL_NAMEDESC_NOMBRE, texto_quill)
        _escribir_quill(driver, wait, P.QUILL_NAMEDESC_DESC, texto_quill)
        _escribir_quill(driver, wait, P.QUILL_POLITICA,  texto_quill)
        _escribir_quill(driver, wait, P.QUILL_ENCUENTRO, texto_quill)
        _escribir_quill(driver, wait, P.QUILL_DESTINO,   texto_quill)
        allure.attach(driver.get_screenshot_as_png(), "21_Quill_Editors", allure.attachment_type.PNG)

    # ──────────────────────────────────────────
    # 27. GUARDAR
    # ──────────────────────────────────────────
    with allure.step("27. Guardar y esperar URL de detalle con id dinámico"):
        safe_click(wait, P.BTN_GUARDAR)
        time.sleep(1)
        wait.until(lambda d: "detail.aspx?service=" in d.current_url.lower())
        allure.attach(
            f"URL tras guardar: {driver.current_url}",
            "27_URL_Detalle",
            allure.attachment_type.TEXT,
        )
        allure.attach(driver.get_screenshot_as_png(), "27_Servicio_Guardado", allure.attachment_type.PNG)

    # ──────────────────────────────────────────
    # 28. VALIDAR PESTAÑAS HABILITADAS
    # ──────────────────────────────────────────
    with allure.step("28. Validar pestañas del detalle habilitadas"):
        time.sleep(1)
        disabled_tabs = driver.find_elements(
            By.CSS_SELECTOR,
            "[id*='ServiciosTabContainer'] .ajax__tab_disabled",
        )
        assert not disabled_tabs, (
            f"Hay {len(disabled_tabs)} pestaña(s) bloqueada(s) en el detalle del servicio."
        )
        allure.attach(driver.get_screenshot_as_png(), "28_Pestanas_Habilitadas", allure.attachment_type.PNG)

    # ──────────────────────────────────────────
    # 29-31. VOLVER A LA LISTA Y VALIDAR
    # ──────────────────────────────────────────
    with allure.step("29 y 30. Volver a Adm. de servicios"):
        # Desde detail.aspx el menú ya está expandido → clickear directo el submenú.
        safe_click(wait, P.SUBMENU_ADM_SERVICIOS)
        wait.until(lambda d: "/administration/services/default.aspx" in d.current_url
                   and "Detail.aspx" not in d.current_url)

    with allure.step("31. Validar que el servicio aparece en la tabla"):
        # Usamos 'presence' (no 'visibility'): el wrapper JS puede ocultar la tabla.
        wait.until(EC.presence_of_element_located(P.TABLA))
        fila = wait.until(EC.presence_of_element_located(P.fila_por_nombre(sello)))
        assert fila is not None, f"El servicio '{nombre_servicio}' no aparece en la tabla."
        allure.attach(
            f"Servicio encontrado en la tabla: {nombre_servicio}",
            "31_Servicio_En_Tabla",
            allure.attachment_type.TEXT,
        )
        allure.attach(driver.get_screenshot_as_png(), "31_Validacion_Tabla", allure.attachment_type.PNG)
