import allure
from pages.webadmin_home_page import WebAdminHomePage


@allure.feature("WebAdmin AMV Travel")
@allure.story("Login y validación del inicio del WebAdmin")
@allure.severity(allure.severity_level.BLOCKER)
@allure.description("""
Valida el acceso al WebAdmin (panel de administración) y el correcto renderizado
de su pantalla de inicio. El login y la navegación a /administration/ los resuelve
la fixture `login_webadmin`. Los selectores viven en el Page Object
`WebAdminHomePage`. Aquí se valida (en un único paso) lo que efectivamente se
muestra en pantalla: sidebar, menú lateral, perfil de usuario, badge QA y la
grilla de reservas.
""")
def test_webadmin_login_admin(login_webadmin):
    page = WebAdminHomePage(login_webadmin)

    with allure.step("Validar renderizado del inicio del WebAdmin"):
        # Captura única del panel ya renderizado: evitamos repetir screenshots
        # idénticos por cada validación.
        allure.attach(page.screenshot_png(), "Inicio_WebAdmin", allure.attachment_type.PNG)

        resultados = []

        # --- URL ---
        assert "/administration" in page.current_url, f"URL inesperada: {page.current_url}"
        resultados.append(f"URL OK: {page.current_url}")

        # --- Sidebar + nombre de la agencia ---
        assert page.sidebar().is_displayed(), "No se visualiza el sidebar del WebAdmin"
        agencia = page.agency_name()
        assert "CLIMBS" in agencia.upper(), \
            f"El nombre de la agencia no es el esperado. Encontrado: '{agencia}'"
        resultados.append(f"Sidebar y agencia OK: '{agencia}'")

        # --- Menú lateral con los ítems que se renderizan ---
        items_esperados = [
            "Principal", "Hoteles", "Servicios", "Circuitos", "Cruceros",
            "Agencias", "Cotizaciones", "Reservas", "Ubicación",
        ]
        textos_menu = page.menu_items()
        faltantes = [it for it in items_esperados if not any(it in t for t in textos_menu)]
        assert not faltantes, f"Faltan ítems esperados en el menú: {faltantes}"
        resultados.append("Menú lateral con ítems clave OK")

        # --- Perfil de usuario (nombre + email) ---
        nombre = page.user_name()
        email = page.user_email()
        assert "Pablo" in nombre, f"El nombre de usuario no es el esperado. Encontrado: '{nombre}'"
        assert "pablo@amv.travel" in email.lower(), \
            f"El email de usuario no es el esperado. Encontrado: '{email}'"
        resultados.append(f"Perfil de usuario OK: {nombre} ({email})")

        # --- Badge de entorno QA ---
        badge = page.qa_badge_text()
        assert "QA" in badge.upper(), f"No se encontró el badge QA. Encontrado: '{badge}'"
        resultados.append("Badge QA OK")

        # --- Grilla de reservas (con al menos una fila de datos) ---
        filas = page.bookings_rows()
        assert len(filas) > 0, "La grilla de reservas no contiene filas de datos"
        resultados.append(f"Grilla de reservas OK ({len(filas)} filas)")

        # --- Botón de Logout ---
        assert page.logout_href().endswith("/Logout.aspx"), \
            "El botón de logout no apunta a /Logout.aspx"
        resultados.append("Botón de Logout OK")

        allure.attach("\n".join(resultados), "Validaciones realizadas", allure.attachment_type.TEXT)
