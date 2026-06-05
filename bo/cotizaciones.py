import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.feature("Reservas BackOffice")
@allure.story("Validación de Bandeja de Entrada de Reservas")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("""
Este test valida la navegación y la estructura de la tabla de reservas en el BO:
1. Login administrativo.
2. Navegación mediante el menú lateral 'Reservas'.
3. Acceso a la Bandeja de Entrada (Inbox).
4. Validación estructural de los contenedores de la tabla.
""")
def test_validar_tabla_reservas_inbox(login_bo):
    driver = login_bo
    wait = WebDriverWait(driver, 15)

    # 2. Menú Lateral
    with allure.step("2. Clic en 'Cotizaciones' en el menú lateral"):
        # Buscamos el span con el texto exacto
        menu_reservas = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Reservas')]")))
        menu_reservas.click()
        
        # Captura para verificar que se desplegaron las opciones
        allure.attach(driver.get_screenshot_as_png(), name="Menu_Lateral_Desplegado", attachment_type=allure.attachment_type.PNG)

    # 3. Navegación a Inbox
    with allure.step("3. Clic en la opción Bandeja de Entrada (Inbox)"):
        # Localizamos por el href exacto solicitado
        link_inbox = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='https://preprod.bo.amv.travel/booking/files/inbox/20']")))
        link_inbox.click()

    # 4. Validaciones Estructurales
    with allure.step("4. Validar presencia de componentes de la tabla"):
        # Definimos los selectores de los componentes clave
        componentes = {
            "Título de página (page-title)": (By.CLASS_NAME, "page-title"),
            "Tarjeta principal (card bg-white)": (By.CSS_SELECTOR, "div.card.bg-white"),
            "Encabezado de tarjeta (card-header)": (By.CLASS_NAME, "card-header"),
            "Cuerpo de tarjeta (card-block)": (By.CLASS_NAME, "card-block")
        }

        for nombre, selector in componentes.items():
            try:
                elemento = wait.until(EC.presence_of_element_located(selector))
                assert elemento.is_displayed(), f"El componente '{nombre}' no es visible."
            except Exception:
                allure.attach(driver.get_screenshot_as_png(), name=f"Error_{nombre}", attachment_type=allure.attachment_type.PNG)
                pytest.fail(f"Falla estructural: No se encontró el elemento '{nombre}' en la pantalla de Reservas.")

        # Captura final con la tabla cargada
        allure.attach(driver.get_screenshot_as_png(), name="Inbox_Reservas_Validado", attachment_type=allure.attachment_type.PNG)
