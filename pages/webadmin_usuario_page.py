"""Page Object de Usuarios (Agencias) — customers/detail.aspx (CustomerTabContainer).
⚠ El botón "Guardar" arranca DESHABILITADO; el guardado real es "Guardar y enviar email"
(btnShowPopUp) → MODAL con confirmación de emails (txtModalEmail / txtModalVendorEmail) →
"Confirmar" (btnModalConfirm). Si la contraseña manual está activa puede aparecer un popup
de confirmación de password (btnConfirmPass). Reutilizable para el paso 2 de Agencias."""
from selenium.webdriver.common.by import By

_B = "ctl00$cph1$CustomerTabContainer$pnlDetails$"
_ID = "ctl00_cph1_CustomerTabContainer_pnlDetails_"


class WebAdminUsuarioPage:
    MENU_AGENCIAS = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'javascript:void')]"
        "//span[normalize-space()='Agencias']")
    SUBMENU_USUARIOS = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[@href='/administration/customers/']")

    BTN_NUEVO = (By.ID, "btnAddNew")   # → detail.aspx

    # Acceso
    TXT_USERNAME    = (By.NAME, f"{_B}txtUserName$txtValue")
    CHK_ENABLE_PASS = (By.ID,   f"{_ID}chkEnablePassword")
    TXT_PASS        = (By.NAME, f"{_B}txtPass")          # sin wrapper $txtValue
    CB_PUBLICADO    = (By.ID,   f"{_ID}cbPublicado")
    DD_USERTYPE     = (By.NAME, f"{_B}ddlWebUserType")   # Tipo de usuario
    # Datos personales
    TXT_NAME     = (By.NAME, f"{_B}txtName$txtValue")
    TXT_LASTNAME = (By.NAME, f"{_B}txtLastName$txtValue")
    TXT_EMAIL    = (By.NAME, f"{_B}txtEmail$txtValue")
    DD_AGENCIES  = (By.NAME, f"{_B}ddlAgencies")
    DD_COUNTRY   = (By.NAME, f"{_B}ddlCountry")
    # Configuración
    DD_CURRENCY   = (By.NAME, f"{_B}ddlCurrency")
    CB_SHOWMARKUP = (By.ID,   f"{_ID}cbShowMarkup")
    CB_ISVENDOR   = (By.ID,   f"{_ID}cbIsVendor")

    # Guardado vía modal "Datos del email"
    BTN_GUARDAR_EMAIL    = (By.NAME, f"{_B}btnShowPopUp")     # "Guardar y enviar email"
    BTN_CONFIRM_PASS     = (By.NAME, f"{_B}btnConfirmPass")   # popup password (si aparece)
    TXT_MODAL_EMAIL      = (By.NAME, f"{_B}txtModalEmail$txtValue")        # Cliente (disabled, prefilled)
    TXT_MODAL_VENDOR_EML = (By.NAME, f"{_B}txtModalVendorEmail$txtValue")  # Vendedor (prefilled)
    DD_SALES_MANAGER     = (By.NAME, f"{_B}ddlSalesManager")  # Responsable comercial (requerido en el modal)
    BTN_MODAL_CONFIRM    = (By.NAME, f"{_B}btnModalConfirm")  # "Confirmar"

    TXT_SEARCH = (By.NAME, "ctl00$cph1$txtSearch")
    BTN_SEARCH = (By.NAME, "ctl00$cph1$btnFilter")   # la lista usa btnFilter (no btnSearch)
    TABLA = (By.ID, "ctl00_cph1_gvAgencyCustomers")

    @staticmethod
    def fila_por_nombre(nombre):
        return (By.XPATH,
            f"//table[@id='ctl00_cph1_gvAgencyCustomers']//td[contains(normalize-space(),\"{nombre}\")]")
