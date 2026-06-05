import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@allure.feature("WebAdmin AMV Travel")
@allure.story("Login y validación del inicio del WebAdmin")
@allure.severity(allure.severity_level.BLOCKER)
@allure.description("""
Valida el acceso al WebAdmin (panel de administración) y el correcto renderizado
de su pantalla de inicio. El login y la navegación a /administration/ los resuelve
la fixture `login_webadmin`. Aquí se valida (en un único paso) lo que efectivamente
se muestra en pantalla: sidebar, menú lateral, perfil de usuario, badge QA y la
grilla de reservas.
""")
def test_webadmin_login_admin(login_webadmin):
    driver = login_webadmin
    wait = WebDriverWait(driver, 45)

    with allure.step("Validar renderizado del inicio del WebAdmin"):
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

        allure.attach("\n".join(resultados), "Validaciones realizadas", allure.attachment_type.TEXT)
