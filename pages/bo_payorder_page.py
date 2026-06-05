"""
Page Object de la pantalla 'Crear Orden de Pago' del BackOffice.
Centraliza los selectores de navegación, formulario, imputación y aprobación.
"""

from selenium.webdriver.common.by import By


class BoPayOrderPage:
    # --- Navegación ---
    MENU_ADMIN = (By.XPATH, "//span[contains(text(), 'Administración')]")
    LINK_PAYORDERS = (By.XPATH, "//a[contains(@href, '/administration/payorders')]")
    BTN_NUEVO = (By.CSS_SELECTOR, "a.btn.btn-sm.btn-info.btn-icon.m-t4.usepreload")

    # --- Proveedor ---
    BTN_SUPPLIER = (By.ID, "btnSupplier")
    INPUT_SEARCH = (By.CSS_SELECTOR, "input[type='search']")
    FILA_PROVEEDOR = (By.CLASS_NAME, "sorting_1")

    # --- Formulario ---
    DD_PAYMENT_REFS = (By.NAME, "ctl00$cphMain$ddPaymentRefs")
    TXT_DETAIL = (By.NAME, "ctl00$cphMain$txtDetail")
    DD_CURRENCY = (By.NAME, "ctl00$cphMain$ddCurrency")
    DD_CASHFLOW = (By.NAME, "ctl00$cphMain$ddCashFlow1")
    TXT_AMOUNT = (By.NAME, "ctl00$cphMain$txtAmount1")
    BTN_SAVE = (By.XPATH, "//input[@type='submit' and @name='ctl00$cphMain$btnSave']")

    # --- Imputación / aprobación ---
    VALIDATION_ERRORS = (By.CSS_SELECTOR, ".validation-summary-errors, .field-validation-error, .alert-danger, span[id*='Error'], .text-danger")
    LNK_ASIGNAR_TOTAL = (By.CSS_SELECTOR, "a[id$='lnkAsignarTotal'], #lnkAsignarTotal")
    CANDIDATOS_ASIGNAR = (By.CSS_SELECTOR, "a[id*='Asignar'], a[id*='asignar'], a[id*='lnk']")
    CELDA_TABLA_INTERNA = (By.CSS_SELECTOR, ".table.table-striped.table-bordered.table-hover.table-condensed.text-center.m-b-0 td.text-center")
    TXT_RECEIPT_DATE = (By.NAME, "ctl00$cphMain$txtReceiptDate")
    BTN_APPROVE = (By.XPATH, "//input[@type='submit' and @name='ctl00$cphMain$btnApprove']")
