"""
Page Object de la pantalla 'Crear Orden de Cobro' del BackOffice.
Centraliza los selectores de navegación, selección de cliente, formulario,
imputación (multi-estrategia) y aprobación.
"""

from selenium.webdriver.common.by import By


class BoChargeOrderPage:
    # --- Navegación ---
    MENU = (By.CSS_SELECTOR, ".menu-accordion:nth-child(4) > a > span")
    SUBMENU = (By.CSS_SELECTOR, ".open li:nth-child(3) span")
    LINK_NUEVO = (By.LINK_TEXT, "Nuevo")

    # --- Formulario ---
    DD_PAYMENT_REFS = (By.ID, "ddPaymentRefs")
    DD_CURRENCY = (By.ID, "ddCurrency")
    TXT_CUSTOMER = (By.ID, "txtCustomer")
    ICON_MAGNIFIER = (By.CSS_SELECTOR, ".icon-magnifier")
    INPUT_SEARCH = (By.CSS_SELECTOR, "input[type='search']")

    # --- Selección de cliente ---
    DATA_CUSTOMERS_SELECTOR = "#dataCustomers"  # para wait_table_rows
    DATA_CUSTOMERS = (By.ID, "dataCustomers")
    FILA_CLIENTE = (By.XPATH, "//table[@id='dataCustomers']//td[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'hectours')]")

    DD_CASHFLOW = (By.ID, "ddCashFlow1")
    TXT_DETAIL = (By.ID, "txtDetail")
    TXT_AMOUNT = (By.ID, "txtAmount1")
    BTN_SAVE = (By.ID, "btnSave")

    # --- Imputación / aprobación ---
    TBL_ALLOCATION = (By.ID, "tblChargeOrderAllocation")
    IMPUTAR_LINK = (By.CSS_SELECTOR, "a[id*='lnkAsignarTotal']")
    IMPUTAR_ICONO = (By.CSS_SELECTOR, "a[id*='lnkAsignarTotal'] i.icon-check")
    IMPUTAR_POSTBACK = (By.XPATH, "//a[contains(@href,'__doPostBack') and contains(@id,'lnkAsignarTotal')]")
    TABLA_INTERNA = (By.CSS_SELECTOR, ".table.table-striped.table-bordered.table-hover.table-condensed.text-center.m-b-0")
    CELDA_TABLA_INTERNA = (By.CSS_SELECTOR, ".table.table-striped.table-bordered.table-hover.table-condensed.text-center.m-b-0 td.text-center")
    TXT_RECEIPT_DATE = (By.ID, "txtReceiptDate")
    BTN_APROBAR = (By.XPATH, "//input[@value='Aprobar & Aplicar Recibo']")
