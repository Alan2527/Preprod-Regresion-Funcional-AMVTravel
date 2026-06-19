"""Page Object de Corporativo (Agencias) — corpcompanies.aspx / corpdetail.aspx (CorpTabContainer)."""
from selenium.webdriver.common.by import By

_B = "ctl00$cph1$CorpTabContainer$pnlDetails$"


class WebAdminCorporativoPage:
    MENU_AGENCIAS = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'javascript:void')]"
        "//span[normalize-space()='Agencias']")
    SUBMENU_CORPORATIVO = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'/administration/corporate/corpcompanies.aspx')]")

    BTN_NUEVO = (By.ID, "btnAddNew")   # → corpdetail.aspx

    TXT_NAME    = (By.NAME, f"{_B}txtName$txtValue")
    TXT_ADDRESS = (By.NAME, f"{_B}txtAddress$txtValue")
    TXT_COMMENT = (By.NAME, f"{_B}txtComment$txtValue")
    TXT_EMAIL   = (By.NAME, f"{_B}txtEmail$txtValue")
    TXT_PHONE   = (By.NAME, f"{_B}txtPhone$txtValue")
    TXT_REWARD  = (By.NAME, f"{_B}txtRewardPointTotal$txtValue")
    DD_MARKET   = (By.NAME, f"{_B}ddMarket")
    DD_VENDOR   = (By.NAME, f"{_B}ddVendor")
    DD_CITIES   = (By.NAME, f"{_B}ddlCities")
    CB_PUBLICADO = (By.ID,  f"ctl00_cph1_CorpTabContainer_pnlDetails_cbPublicado")
    BTN_GUARDAR = (By.NAME, f"{_B}btnSave")

    SOLAPAS = {
        "Detalle": "ctl00_cph1_CorpTabContainer_pnlDetails_tab",
        "Config. de productos": "ctl00_cph1_CorpTabContainer_pnlProductSetting_tab",
    }
    TAB_CONTAINER = "CorpTabContainer"

    TXT_SEARCH = (By.NAME, "ctl00$cph1$txtSearch")
    BTN_SEARCH = (By.NAME, "ctl00$cph1$btnSearch")
    TABLA = (By.CSS_SELECTOR, "table.tablestyle")

    @staticmethod
    def fila_por_nombre(nombre):
        return (By.XPATH,
            f"//table[contains(@class,'tablestyle')]//td[contains(normalize-space(),\"{nombre}\")]")
