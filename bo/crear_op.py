import pytest
import allure
import os
import time
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
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
            time.sleep(1)
    raise Exception(f"No se pudo hacer click: {locator}")


def safe_send_keys(wait, locator, value):
    for _ in range(5):
        try:
            elem = wait.until(EC.visibility_of_element_located(locator))

            # Scroll al elemento
            wait._driver.execute_script("arguments[0].scrollIntoView(true);", elem)
            time.sleep(0.5)

            elem.clear()
            elem.send_keys(value)
            return

        except (StaleElementReferenceException, ElementNotInteractableException):
            try:
                # 🔥 fallback JS
                elem = wait.until(EC.presence_of_element_located(locator))
                wait._driver.execute_script("arguments[0].value = arguments[1];", elem, value)
                return
            except:
                time.sleep(1)

    raise Exception(f"No se pudo escribir en: {locator}")


def wait_table_rows(wait, table_id):
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f"{table_id} tbody tr")))


# =========================
# TEST
# =========================

@allure.feature("Administración BackOffice")
@allure.story("Crear Orden de Pago")
@allure.severity(allure.severity_level.CRITICAL)
def test_crear_orden_pago(driver):

    wait = WebDriverWait(driver, 25)

    # ==========================================
    # 1. LOGIN
    # ==========================================
    with allure.step("1. Login"):
        driver.get("https://preprod.bo.amv.travel/login")

        user = os.environ.get("AMV_USER")
        password = os.environ.get("BO_PASS")

        if not user or not password:
            pytest.fail("Faltan variables de entorno")

        safe_send_keys(wait, (By.ID, "txtUser"), user)
        safe_send_keys(wait, (By.ID, "txtPassword"), password)
        safe_click(wait, (By.ID, "btnLogin"))

        wait.until(EC.url_contains("/main"))
        allure.attach(driver.get_screenshot_as_png(), "1_Login", allure.attachment_type.PNG)

    # ==========================================
    # 2. NAVEGACIÓN (Administración)
    # ==========================================
    with allure.step("2. Click en Administración"):
        safe_click(wait, (By.XPATH, "//span[contains(text(), 'Administración')]"))
        allure.attach(driver.get_screenshot_as_png(), "2_Administracion", allure.attachment_type.PNG)

    # ==========================================
    # 3. IR A ORDENES DE PAGO
    # ==========================================
    with allure.step("3. Ir a PayOrders"):
        safe_click(wait, (By.XPATH, "//a[contains(@href, '/administration/payorders')]"))
        allure.attach(driver.get_screenshot_as_png(), "3_PayOrders", allure.attachment_type.PNG)

    # ==========================================
    # 4. NUEVO (Payorder/0)
    # ==========================================
    with allure.step("4. Click en Nueva Orden de Pago"):
        safe_click(wait, (By.XPATH, "//a[contains(@href, '/administration/payorder/0')]"))
        allure.attach(driver.get_screenshot_as_png(), "4_Nueva_OP", allure.attachment_type.PNG)

    # ==========================================
    # 5. ABRIR MODAL PROVEEDOR
    # ==========================================
    with allure.step("5. Abrir modal proveedor"):
        safe_click(wait, (By.ID, "btnSupplier"))
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='search']")))
        allure.attach(driver.get_screenshot_as_png(), "5_Modal_Proveedor", allure.attachment_type.PNG)

    # ==========================================
    # 6. BUSCAR PROVEEDOR
    # ==========================================
    with allure.step("6. Buscar MAX BAIRES"):
        search = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='search']")))
        search.clear()
        search.send_keys("MAX BAIRES")
        allure.attach(driver.get_screenshot_as_png(), "6_Busqueda_Proveedor", allure.attachment_type.PNG)

    # ==========================================
    # 7. SELECCIONAR PROVEEDOR
    # ==========================================
    with allure.step("7. Seleccionar fila del proveedor"):
        fila_proveedor = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "sorting_1")))
        driver.execute_script("arguments[0].click();", fila_proveedor)
        time.sleep(3)  # Esperamos a que impacte el PostBack y cargue la sucursal por defecto
        allure.attach(driver.get_screenshot_as_png(), "7_Proveedor_Seleccionado", allure.attachment_type.PNG)

    # ==========================================
    # 8. PAYMENT REF (Value='40')
    # ==========================================
    with allure.step("8. Seleccionar Payment Ref (Value='40')"):
        Select(wait.until(EC.element_to_be_clickable((By.NAME, "ctl00$cphMain$ddPaymentRefs"))))\
            .select_by_value("40")
        allure.attach(driver.get_screenshot_as_png(), "8_PaymentRef", allure.attachment_type.PNG)

    # ==========================================
    # 9. MONEDA (Currency Value='10')
    # ==========================================
    with allure.step("9. Seleccionar Moneda (Value='10')"):
        Select(wait.until(EC.element_to_be_clickable((By.NAME, "ctl00$cphMain$ddCurrency"))))\
            .select_by_value("10")
        allure.attach(driver.get_screenshot_as_png(), "9_Currency", allure.attachment_type.PNG)

    # ==========================================
    # 10. NÚMERO DE DOCUMENTO
    # ==========================================
    with allure.step("10. Escribir número de documento"):
        safe_send_keys(wait, (By.NAME, "ctl00$cphMain$txtDocNumber"), "123456789")
        allure.attach(driver.get_screenshot_as_png(), "10_DocNumber", allure.attachment_type.PNG)

    # ==========================================
    # 11. CAJA (CashFlow Value='8')
    # ==========================================
    with allure.step("11. Seleccionar Caja (Value='8')"):
        Select(wait.until(EC.element_to_be_clickable((By.NAME, "ctl00$cphMain$ddCashFlow1"))))\
            .select_by_value("8")
        allure.attach(driver.get_screenshot_as_png(), "11_CashFlow", allure.attachment_type.PNG)

    # ==========================================
    # 12. MONTO
    # ==========================================
    with allure.step("12. Ingresar Monto"):
        safe_send_keys(wait, (By.NAME, "ctl00$cphMain$txtAmount1"), "900000")
        allure.attach(driver.get_screenshot_as_png(), "12_Monto", allure.attachment_type.PNG)

    # ==========================================
    # 13. DETALLE
    # ==========================================
    with allure.step("13. Ingresar Detalle"):
        safe_send_keys(wait, (By.NAME, "ctl00$cphMain$txtDetail"), "Test automático")
        allure.attach(driver.get_screenshot_as_png(), "13_Detalle", allure.attachment_type.PNG)

    # ==========================================
    # 14. GUARDAR
    # ==========================================
    with allure.step("14. Guardar Orden de Pago"):
        boton_guardar = wait.until(EC.presence_of_element_located((
            By.XPATH, 
            "//input[@name='ctl00$cphMain$btnSave' and @value='Guardar']"
        )))
        driver.execute_script("arguments[0].click();", boton_guardar)
        allure.attach(driver.get_screenshot_as_png(), "14_Click_Guardar", allure.attachment_type.PNG)

    # ==========================================
    # 15. ESPERAR CARGA
    # ==========================================
    with allure.step("15. Esperar que la pantalla cargue"):
        time.sleep(5)
        wait.until(EC.presence_of_element_located((By.XPATH, "//body")))
        allure.attach(driver.get_screenshot_as_png(), "15_Pantalla_Cargada", allure.attachment_type.PNG)

    # ==========================================
    # 16. INGRESAR FECHA ACTUAL
    # ==========================================
    with allure.step("16. Ingresar fecha del día"):
        fecha_hoy = datetime.now().strftime("%d/%m/%Y")
        safe_send_keys(wait, (By.ID, "txtReceiptDate"), fecha_hoy)
        allure.attach(driver.get_screenshot_as_png(), "16_Fecha_Ingresada", allure.attachment_type.PNG)

    # ==========================================
    # 17. SCROLL A TABLA IMPUTACIÓN
    # ==========================================
    with allure.step("17. Scroll hasta tabla de imputación de facturas"):
        tabla = wait.until(EC.presence_of_element_located((By.ID, "tblAllocationSupplierInvoices")))
        driver.execute_script("arguments[0].scrollIntoView(true);", tabla)
        time.sleep(2)
        allure.attach(driver.get_screenshot_as_png(), "17_Scroll_Tabla", allure.attachment_type.PNG)

    # ==========================================
    # 18. CLICK EN IMPUTAR (Primer icon-check)
    # ==========================================
    with allure.step("18. Click en el primer check de imputación"):
        primer_check = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, 
            "#tblAllocationSupplierInvoices i.icon-check"
        )))
        driver.execute_script("arguments[0].click();", primer_check)
        time.sleep(5)
        allure.attach(driver.get_screenshot_as_png(), "18_Click_Check", allure.attachment_type.PNG)

    # ==========================================
    # 19. VALIDAR TABLA INTERNA
    # ==========================================
    with allure.step("19. Validar existencia de celda en tabla interna"):
        wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR,
            ".table.table-striped.table-bordered.table-hover.table-condensed.text-center.m-b-0 td.text-center"
        )))
        allure.attach(driver.get_screenshot_as_png(), "19_Tabla_Interna_Validada", allure.attachment_type.PNG)

    # ==========================================
    # 20. SCROLL Y CLICKEAR APROBAR
    # ==========================================
    with allure.step("20. Scroll arriba y aprobar recibo"):
        boton_aprobar = wait.until(EC.presence_of_element_located((
            By.XPATH,
            "//input[@value='Aprobar & Aplicar Recibo']"
        )))
        driver.execute_script("arguments[0].scrollIntoView(true);", boton_aprobar)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", boton_aprobar)
        time.sleep(5)
        allure.attach(driver.get_screenshot_as_png(), "20_Click_Aprobar", allure.attachment_type.PNG)

    # ==========================================
    # 21. VALIDAR DESAPARICIÓN DEL BOTÓN
    # ==========================================
    with allure.step("21. Validar que el botón de aprobación desapareció"):
        wait.until(EC.invisibility_of_element_located((
            By.XPATH,
            "//input[@value='Aprobar & Aplicar Recibo']"
        )))
        allure.attach(driver.get_screenshot_as_png(), "21_Fin_Test", allure.attachment_type.PNG)
