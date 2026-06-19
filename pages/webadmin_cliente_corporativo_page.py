"""Page Object de Clientes Corporativos (Agencias) — corpcustomers.aspx / corpcustomerdetail.aspx
(CustomerTabContainer). Más simple que Usuarios: guarda directo (sin modal de email)."""
from selenium.webdriver.common.by import By

_B = "ctl00$cph1$CustomerTabContainer$pnlDetails$"


class WebAdminClienteCorporativoPage:
    MENU_AGENCIAS = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'javascript:void')]"
        "//span[normalize-space()='Agencias']")
    SUBMENU_CLIENTES_CORP = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'/administration/corporate/corpcustomers.aspx')]")

    BTN_NUEVO = (By.ID, "btnAddNew")   # → corpcustomerdetail.aspx

    TXT_NAME     = (By.NAME, f"{_B}txtName$txtValue")
    TXT_LASTNAME = (By.NAME, f"{_B}txtLastName$txtValue")
    TXT_EMAIL    = (By.NAME, f"{_B}txtEmail$txtValue")
    TXT_USERNAME = (By.NAME, f"{_B}txtUserName$txtValue")
    TXT_PASS     = (By.NAME, f"{_B}txtPass$txtValue")
    DD_CORP      = (By.NAME, f"{_B}ddlCorps")
    DD_CURRENCY  = (By.NAME, f"{_B}ddlCurrency")
    DD_USERTYPE  = (By.NAME, f"{_B}ddlWebUserType")
    CB_PUBLICADO = (By.ID,   "ctl00_cph1_CustomerTabContainer_pnlDetails_cbPublicado")
    BTN_GUARDAR  = (By.NAME, f"{_B}btnSave")

    TXT_SEARCH = (By.NAME, "ctl00$cph1$txtSearch")
    BTN_SEARCH = (By.NAME, "ctl00$cph1$btnSearch")
    TABLA = (By.CSS_SELECTOR, "table.tablestyle")

    @staticmethod
    def fila_por_nombre(nombre):
        return (By.XPATH,
            f"//table[contains(@class,'tablestyle')]//td[contains(normalize-space(),\"{nombre}\")]")
