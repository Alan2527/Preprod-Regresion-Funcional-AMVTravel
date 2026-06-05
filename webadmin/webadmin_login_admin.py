import pytest
import allure
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, ElementNotInteractableException


# =========================
# HELPERS ROBUSTOS
# =========================

def safe_click(wait, locator):
    for _ in range(5):
        try:
            elem = wait.until(EC.element_to_be_clickable(locator))
            elem.click()
            return
        except StaleElementReferenceException:
            time.sleep(2)
    raise Exception(f"No se pudo hacer click: {locator}")


def safe_send_keys(wait, locator, value):
    for _ in range(5):
        try:
            elem = wait.until(EC.visibility_of_element_located(locator))

            # Scroll al elemento
            wait._driver.execute_script("arguments[0].scrollIntoView(true);", elem)
            time.sleep(1)

            elem.clear()
            elem.send_keys(value)
            return

        except (StaleElementReferenceException, ElementNotInteractableException):
            try:
                # Fallback JS nativo si se bloquea
                elem = wait.until(EC.presence_of_element_located(locator))
                wait._driver.execute_script("arguments[0].value = arguments[1];", elem, value)
                return
            except:
                time.sleep(2)

    raise Exception(f"No se pudo escribir en: {locator}")


# =========================
# TEST
# =========================

@allure.feature("WebAdmin AMV Travel")
@allure.story("Login y validación del inicio del WebAdmin")
@allure.severity(allure.severity_level.BLOCKER)
@allure.description("""
Este caso de prueba valida el acceso al WebAdmin (panel de administración) y
el correcto renderizado de su pantalla de inicio.
1. Login en preprod.amv.travel/login.aspx con credenciales de administrador.
2. El sistema redirige a /online/; se navega manualmente a /administration/.
3. Se valida que el panel renderice correctamente: sidebar, menú lateral,
   perfil de usuario, badge QA, sección de reservas pendientes y su grilla.
""")
def test_webadmin_login_admin(driver):

    # Timeout holgado para el servidor de preprod
    wait = WebDriverWait(driver, 45)

    # ==========================================
    # 1. LOGIN
    # ==========================================
    with allure.step("1. Ingresar a preprod.amv.travel/login.aspx"):
        driver.get("https://preprod.amv.travel/login.aspx")
        wait.until(EC.visibility_of_element_located((By.NAME, "txtUser")))

    with allure.step("2. Escribir credenciales"):
        # Reutilizamos los GitHub Secrets si están disponibles; si no, usamos
        # las credenciales del entorno de preprod.
        usuario = os.environ.get("AMV_USER", "Pablo@amv.travel")
        password = os.environ.get("AMV_PASS", "amvtest123")

        if not usuario or not password:
            pytest.fail("Faltan las credenciales (AMV_USER / AMV_PASS) en el entorno.")

        safe_send_keys(wait, (By.NAME, "txtUser"), usuario)
        safe_send_keys(wait, (By.NAME, "txtPassword"), password)
        allure.attach(driver.get_screenshot_as_png(), "1_Credenciales", allure.attachment_type.PNG)

    with allure.step("3. Click en el botón Ingresar (input submit)"):
        safe_click(wait, (By.CSS_SELECTOR, "input[type='submit']"))
        # Esperamos a que el login procese y salga de la pantalla de login
        wait.until(lambda d: "login" not in d.current_url.lower())
        time.sleep(3)
        allure.attach(driver.get_screenshot_as_png(), "2_Post_Login", allure.attachment_type.PNG)
        allure.attach(
            f"URL tras el login: {driver.current_url}",
            "2_URL_Post_Login",
            allure.attachment_type.TEXT,
        )

    # ==========================================
    # 2. NAVEGAR AL WEBADMIN
    # ==========================================
    with allure.step("4. Navegar manualmente a /administration/"):
        driver.get("https://preprod.amv.travel/administration/")
        time.sleep(3)

        # Validamos que efectivamente estamos en el panel de administración
        try:
            wait.until(EC.url_contains("/administration"))
        except Exception:
            allure.attach(driver.get_screenshot_as_png(), "ERROR_4_no_administration", allure.attachment_type.PNG)
            pytest.fail(
                "No se pudo acceder al WebAdmin. "
                f"URL actual: {driver.current_url}. "
                "Posible sesión inválida o redirección al login."
            )
        allure.attach(driver.get_screenshot_as_png(), "4_WebAdmin_Inicio", allure.attachment_type.PNG)

    # ==========================================
    # 3. VALIDAR RENDERIZADO DEL INICIO
    # ==========================================
    with allure.step("5. Validar Sidebar y marca de la agencia"):
        sidebar = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.admin-sidebar")))
        assert sidebar.is_displayed(), "No se visualiza el sidebar del WebAdmin"

        agencia = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.agency-name")))
        assert "AMV. TRAVEL" in agencia.text.upper(), \
            f"El nombre de la agencia no es el esperado. Encontrado: '{agencia.text}'"
        allure.attach(driver.get_screenshot_as_png(), "5_Sidebar", allure.attachment_type.PNG)

    with allure.step("6. Validar menú lateral principal y sus secciones"):
        menu = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul#ctl00_ctrlMenu.sf-menu")))
        assert menu.is_displayed(), "No se visualiza el menú principal (sf-menu)"

        # Validamos que existan los ítems de menú clave del WebAdmin
        items_esperados = [
            "Principal", "Hoteles", "Servicios", "Circuitos", "Cruceros",
            "Agencias", "Cotizaciones", "Reservas", "Incentivos", "Contenidos", "Widget",
        ]
        textos_menu = [e.text.strip() for e in menu.find_elements(By.TAG_NAME, "span")]
        faltantes = [it for it in items_esperados if not any(it in t for t in textos_menu)]
        assert not faltantes, f"Faltan ítems esperados en el menú: {faltantes}"
        allure.attach(
            "Ítems de menú detectados:\n" + "\n".join(t for t in textos_menu if t),
            "6_Items_Menu",
            allure.attachment_type.TEXT,
        )

    with allure.step("7. Validar perfil de usuario (nombre y email)"):
        perfil = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.sidebar-user-profile")))
        nombre = perfil.find_element(By.CSS_SELECTOR, "span.user-name").text.strip()
        email = perfil.find_element(By.CSS_SELECTOR, "span.user-email").text.strip()

        assert "Pablo" in nombre, f"El nombre de usuario no es el esperado. Encontrado: '{nombre}'"
        assert "pablo@amv.travel" in email.lower(), \
            f"El email de usuario no es el esperado. Encontrado: '{email}'"
        allure.attach(
            f"Usuario logueado: {nombre} ({email})",
            "7_Perfil_Usuario",
            allure.attachment_type.TEXT,
        )

    with allure.step("8. Validar badge de entorno QA"):
        badge = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.qa-badge")))
        assert "QA" in badge.text.upper(), f"No se encontró el badge QA. Encontrado: '{badge.text}'"
        allure.attach(driver.get_screenshot_as_png(), "8_Badge_QA", allure.attachment_type.PNG)

    with allure.step("9. Validar sección 'Reservas pendientes' y su grilla"):
        # Título de la sección
        seccion = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.section-header div.title")))
        assert "Reservas pendientes" in seccion.text, \
            f"No se encontró la sección 'Reservas pendientes'. Encontrado: '{seccion.text}'"

        # Grilla de reservas
        grilla = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table#ctl00_cph1_gvBooks")))
        assert grilla.is_displayed(), "No se visualiza la grilla de reservas pendientes"

        # Validamos que la grilla tenga al menos una fila de datos (además del header)
        filas = grilla.find_elements(By.CSS_SELECTOR, "tr.rowstyle, tr.altrowstyle")
        assert len(filas) > 0, "La grilla de reservas pendientes no contiene filas de datos"

        allure.attach(
            f"Cantidad de filas (reservas) en la grilla: {len(filas)}",
            "9_Filas_Grilla",
            allure.attachment_type.TEXT,
        )
        allure.attach(driver.get_screenshot_as_png(), "9_Reservas_Pendientes", allure.attachment_type.PNG)

    with allure.step("10. Validar botón de Logout (cierre de sesión)"):
        logout = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.sidebar-logout-btn")))
        assert logout.get_attribute("href").endswith("/Logout.aspx"), \
            "El botón de logout no apunta a /Logout.aspx"
        allure.attach(driver.get_screenshot_as_png(), "10_Fin_Test_Exitoso", allure.attachment_type.PNG)
