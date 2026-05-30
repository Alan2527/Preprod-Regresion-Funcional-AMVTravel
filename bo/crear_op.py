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
# HELPERS
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
            wait._driver.execute_script("arguments[0].scrollIntoView(true);", elem)
            time.sleep(1)
            elem.clear()
            elem.send_keys(value)
            return
        except (StaleElementReferenceException, ElementNotInteractableException):
            try:
                elem = wait.until(EC.presence_of_element_located(locator))
                wait._driver.execute_script("arguments[0].value = arguments[1];", elem, value)
                return
            except:
                time.sleep(2)

    raise Exception(f"No se pudo escribir en: {locator}")


# =========================
# TEST
# =========================

@allure.feature("Administración BackOffice")
@allure.story("Crear Orden de Pago")
@allure.severity(allure.severity_level.CRITICAL)
def test_crear_orden_pago(driver):

    wait = WebDriverWait(driver, 45)

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
    # 2. NAVEGACIÓN
    # ==========================================
    with allure.step("2. Administración"):
        safe_click(wait, (By.XPATH, "//span[contains(text(), 'Administración')]"))

    with allure.step("2.1 PayOrders"):
        safe_click(wait, (By.XPATH, "//a[contains(@href, '/administration/payorders')]"))

    with allure.step("2.2 Nuevo"):
        safe_click(wait, (By.CSS_SELECTOR, "a.btn.btn-sm.btn-info.btn-icon.m-t4.usepreload"))
        time.sleep(4)

    # ==========================================
    # 3. PROVEEDOR
    # ==========================================
    with allure.step("3. Proveedor"):
        safe_click(wait, (By.ID, "btnSupplier"))

        search = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='search']")))
        search.clear()
        search.send_keys("MAX BAIRES")

        fila = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "sorting_1")))
        driver.execute_script("arguments[0].click();", fila)

        time.sleep(5)

    # ==========================================
    # 4-8 CAMPOS
    # ==========================================
    Select(wait.until(EC.element_to_be_clickable((By.NAME, "ctl00$cphMain$ddPaymentRefs")))).select_by_value("40")

    safe_send_keys(wait, (By.NAME, "ctl00$cphMain$txtDetail"), "Test Automático")

    Select(wait.until(EC.element_to_be_clickable((By.NAME, "ctl00$cphMain$ddCurrency")))).select_by_value("10")
    time.sleep(5)

    Select(wait.until(EC.element_to_be_clickable((By.NAME, "ctl00$cphMain$ddCashFlow1")))).select_by_value("8")
    time.sleep(5)

    safe_send_keys(wait, (By.NAME, "ctl00$cphMain$txtAmount1"), "900000")

# ==========================================
# 9. GUARDAR + REDIRECCIÓN REAL
# ==========================================
with allure.step("9. Guardar"):
    safe_click(wait, (By.XPATH, "//input[@type='submit' and @name='ctl00$cphMain$btnSave']"))

    # 🔥 ESTE ES EL FIX REAL
    WebDriverWait(driver, 60).until(
        EC.url_matches(r".*/payorder/\d+")
    )

    # opcional debug
    print("URL actual:", driver.current_url)

    time.sleep(2)


# ==========================================
# 10. TABLA IMPUTACIÓN (EN LA NUEVA PÁGINA)
# ==========================================
with allure.step("10. Tabla imputación"):

    tabla = WebDriverWait(driver, 60).until(
        EC.visibility_of_element_located((
            By.ID,
            "tblAllocationSupplierInvoices"
        ))
    )

    # validar filas reales
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((
            By.CSS_SELECTOR,
            "#tblAllocationSupplierInvoices tbody tr"
        ))
    )
    
    # ==========================================
    # 11. ASIGNAR TOTAL
    # ==========================================
    with allure.step("11. Asignar total"):
        btn = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR,
            "a[id*='lnkAsignarTotal']"
        )))
        driver.execute_script("arguments[0].click();", btn)
        time.sleep(5)

    # ==========================================
    # 12. VALIDAR TABLA
    # ==========================================
    with allure.step("12. Validar tabla"):
        celda = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR,
            ".table.table-striped td"
        )))

        driver.execute_script("arguments[0].scrollIntoView(false);", celda)
        time.sleep(2)

    # ==========================================
    # 13. FECHA
    # ==========================================
    fecha = datetime.now().strftime("%d/%m/%Y")
    safe_send_keys(wait, (By.NAME, "ctl00$cphMain$txtReceiptDate"), fecha)

    # ==========================================
    # 14. APROBAR
    # ==========================================
    with allure.step("14. Aprobar"):
        btn = wait.until(EC.presence_of_element_located((
            By.XPATH,
            "//input[@name='ctl00$cphMain$btnApprove']"
        )))
        driver.execute_script("arguments[0].click();", btn)

        time.sleep(8)

    # ==========================================
    # 15. VALIDACIÓN FINAL
    # ==========================================
    wait.until(EC.invisibility_of_element_located((
        By.XPATH,
        "//input[@name='ctl00$cphMain$btnApprove']"
    )))
