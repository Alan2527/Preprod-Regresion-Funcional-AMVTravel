import pytest
import allure
from datetime import datetime, timedelta
from pages.front_ofertas_page import FrontOfertasPage


@allure.feature("Ofertas")
@allure.story("Nuevo flujo E2E: Búsqueda de Oferta a 7 días y validación de UI")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("""
Este caso de prueba cubre el flujo End-to-End (E2E) de la cotización de un circuito (Oferta):
1. Login silencioso (fixture) y navegación a la pestaña de Ofertas.
2. Ingreso de fecha dinámica (hoy + 7 días) y cierre del calendario.
3. Uso de los selectores para parámetros de viaje y habitación.
4. Validación de la estructura HTML.
5. Avance a la pantalla final y validación visual de la tabla de cotizaciones.
""")
def test_ofertas(logged_in_driver):
    page = FrontOfertasPage(logged_in_driver)

    try:
        with allure.step("1 a 5. Navegar, ingresar fecha y buscar"):
            page.open_tab()
            fecha_oferta = (datetime.now() + timedelta(days=7)).strftime("%d/%m/%Y")
            page.set_date(fecha_oferta)
            page.search()
            allure.attach(page.screenshot_png(), name="1_Busqueda_Realizada", attachment_type=allure.attachment_type.PNG)

        with allure.step("6 a 9. Seleccionar parámetros de viaje (4) y tipo de habitación (4)"):
            page.select_tomselect("container-travel-paremeters", "4")
            page.select_tomselect("container-type-room-paremeter", "4")
            allure.attach(page.screenshot_png(), name="2_Parametros_Seleccionados", attachment_type=allure.attachment_type.PNG)

        with allure.step("10 y 11. Avanzar y validar contenido del acordeón (Imagen y H6)"):
            page.next_step()
            assert page.accordion_has_default_image(), "Validación fallida: No se encontró la imagen default."
            assert page.accordion_has_h6(), "Validación fallida: No se encontró el tag <h6>."
            allure.attach(page.screenshot_png(), name="3_Acordeon_Validado", attachment_type=allure.attachment_type.PNG)

        with allure.step("12 y 13. Avanzar y validar VISUALMENTE la existencia de la tabla final"):
            page.next_step()
            page.final_table_visible()
            allure.attach(page.screenshot_png(), name="4_Tabla_Final_Validada", attachment_type=allure.attachment_type.PNG)

    except Exception as e:
        allure.attach(page.screenshot_png(), name="Fallo_en_Ofertas", attachment_type=allure.attachment_type.PNG)
        pytest.fail(f"El test falló durante la ejecución: {str(e)}")
