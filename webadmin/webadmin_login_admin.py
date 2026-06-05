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
3. Se valida (en un único paso) que el panel renderice correctamente lo que
   efectivamente se muestra en pantalla: sidebar, menú lateral, perfil de
   usuario, badge QA y la grilla de reservas.
""")
def test_webadmin_login_admin(driver):

    # Timeout holgado para el servidor de preprod
    wait = WebDriverWait(driver, 45)

    # ==========================================
    # 1. LOGIN
    # ==========================================
    with allure.step("1. Login en preprod.amv.travel/login.aspx"):
        driver.get("https://preprod.amv.travel/login.aspx")
        wait.until(EC.visibility_of_element_located((By.NAME, "txtUser")))

        # Reutilizamos los GitHub Secrets si están disponibles; si no, usamos
        # las credenciales del entorno de preprod.
        usuario = os.environ.get("AMV_USER", "Pablo@amv.travel")
        password = os.environ.get("AMV_PASS", "amvtest123")

        if not usuario or not password:
            pytest.fail("Faltan las credenciales (AMV_USER / AMV_PASS) en el entorno.")

        safe_send_keys(wait, (By.NAME, "txtUser"), usuario)
        safe_send_keys(wait, (By.NAME, "txtPassword"), password)
        safe_click(wait, (By.CSS_SELECTOR, "input[type='submit']"))

        # Esperamos a que el login procese y salga de la pantalla de login
        wait.until(lambda d: "login" not in d.current_url.lower())
        time.sleep(3)

    # ==========================================
    # 2. NAVEGAR AL WEBADMIN
    # ==========================================
    with allure.step("2. Navegar a /administration/"):
        driver.get("https://preprod.amv.travel/administration/")
        time.sleep(3)

        try:
            wait.until(EC.url_contains("/administration"))
        except Exception:
            allure.attach(driver.get_screenshot_as_png(), "ERROR_no_administration", allure.attachment_type.PNG)
            pytest.fail(
                "No se pudo acceder al WebAdmin. "
                f"URL actual: {driver.current_url}. "
                "Posible sesión inválida o redirección al login."
            )

    # ==========================================
    # 3. VALIDAR RENDERIZADO DEL INICIO (UN SOLO PASO, UNA SOLA CAPTURA)
    # ==========================================
    with allure.step("3. Validar renderizado del inicio del WebAdmin"):
        # Captura única del panel ya renderizado. Evitamos repetir screenshots
        # idénticos por cada validación: una sola imagen representa el estado.
        allure.attach(driver.get_screenshot_as_png(), "Inicio_WebAdmin", allure.attachment_type.PNG)

        resultados = []

        # --- URL ---
        assert "/administration" in driver.current_url, f"URL inesperada: {driver.current_url}"
        resultados.append(f"URL OK: {driver.current_url}")

        # --- Sidebar + nombre de la agencia ---
        sidebar = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.admin-sidebar")))
        assert sidebar.is_displayed(), "No se visualiza el sidebar del WebAdmin"
        agencia = sidebar.find_element(By.CSS_SELECTOR, "span.agency-name").get_attribute("textContent").strip()
        assert "AMV. TRAVEL" in agencia.upper(), \
            f"El nombre de la agencia no es el esperado. Encontrado: '{agencia}'"
        resultados.append(f"Sidebar y agencia OK: '{agencia}'")

        # --- Menú lateral con los ítems que se renderizan ---
        menu = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "ul#ctl00_ctrlMenu.sf-menu")))
        items_esperados = [
            "Principal", "Hoteles", "Servicios", "Circuitos", "Cruceros",
            "Agencias", "Cotizaciones", "Reservas", "Ubicación",
        ]
        # textContent lee el DOM renderizado sin depender de si el ítem quedó
        # dentro o fuera del viewport (scroll del sidebar).
        textos_menu = [s.get_attribute("textContent").strip() for s in menu.find_elements(By.TAG_NAME, "span")]
        faltantes = [it for it in items_esperados if not any(it in t for t in textos_menu)]
        assert not faltantes, f"Faltan ítems esperados en el menú: {faltantes}"
        resultados.append("Menú lateral con ítems clave OK")

        # --- Perfil de usuario (nombre + email) ---
        perfil = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.sidebar-user-profile")))
        nombre = perfil.find_element(By.CSS_SELECTOR, "span.user-name").get_attribute("textContent").strip()
        email = perfil.find_element(By.CSS_SELECTOR, "span.user-email").get_attribute("textContent").strip()
        assert "Pablo" in nombre, f"El nombre de usuario no es el esperado. Encontrado: '{nombre}'"
        assert "pablo@amv.travel" in email.lower(), \
            f"El email de usuario no es el esperado. Encontrado: '{email}'"
        resultados.append(f"Perfil de usuario OK: {nombre} ({email})")

        # --- Badge de entorno QA ---
        badge = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "span.qa-badge")))
        assert "QA" in badge.get_attribute("textContent").upper(), \
            f"No se encontró el badge QA. Encontrado: '{badge.get_attribute('textContent')}'"
        resultados.append("Badge QA OK")

        # --- Grilla de reservas (con al menos una fila de datos) ---
        grilla = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "table#ctl00_cph1_gvBooks")))
        filas = grilla.find_elements(By.CSS_SELECTOR, "tr.rowstyle, tr.altrowstyle")
        assert len(filas) > 0, "La grilla de reservas no contiene filas de datos"
        resultados.append(f"Grilla de reservas OK ({len(filas)} filas)")

        # --- Botón de Logout ---
        logout = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.sidebar-logout-btn")))
        assert logout.get_attribute("href").endswith("/Logout.aspx"), \
            "El botón de logout no apunta a /Logout.aspx"
        resultados.append("Botón de Logout OK")

        # Resumen de todas las validaciones en un único adjunto de texto.
        allure.attach("\n".join(resultados), "Validaciones realizadas", allure.attachment_type.TEXT)
