import pytest
import allure
from pages.bo_booking_inbox_page import BoBookingInboxPage

INBOX_URL = "https://preprod.bo.amv.travel/booking/files/inbox/20"


@allure.feature("Reservas BackOffice")
@allure.story("Validación de Bandeja de Entrada de Reservas")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("""
Este test valida la navegación y la estructura de la tabla de reservas en el BO:
1. Login administrativo (fixture login_bo).
2. Navegación mediante el menú lateral 'Reservas'.
3. Acceso a la Bandeja de Entrada (Inbox).
4. Validación estructural de los contenedores de la tabla.
""")
def test_validar_tabla_reservas_inbox(login_bo):
    page = BoBookingInboxPage(login_bo)

    with allure.step("2. Abrir menú lateral 'Reservas'"):
        page.open_menu_reservas()
        allure.attach(page.screenshot_png(), name="Menu_Lateral_Desplegado", attachment_type=allure.attachment_type.PNG)

    with allure.step("3. Abrir Bandeja de Entrada (Inbox)"):
        page.open_inbox(INBOX_URL)

    with allure.step("4. Validar presencia de componentes de la tabla"):
        for nombre, selector in page.COMPONENTS.items():
            try:
                elemento = page.find_component(selector)
                assert elemento.is_displayed(), f"El componente '{nombre}' no es visible."
            except Exception:
                allure.attach(page.screenshot_png(), name=f"Error_{nombre}", attachment_type=allure.attachment_type.PNG)
                pytest.fail(f"Falla estructural: No se encontró el elemento '{nombre}' en la pantalla de Reservas.")

        allure.attach(page.screenshot_png(), name="Inbox_Reservas_Validado", attachment_type=allure.attachment_type.PNG)
