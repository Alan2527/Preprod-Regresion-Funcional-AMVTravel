"""Page Object de Galerías de Pax (Agencias) — passengergalleries.aspx / passengergallerydetail.aspx."""
from selenium.webdriver.common.by import By

_B = "ctl00$cph1$mainTabContainer$pnlDetails$"


class WebAdminGaleriaPaxPage:
    MENU_AGENCIAS = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'javascript:void')]"
        "//span[normalize-space()='Agencias']")
    SUBMENU_GALERIAS = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'/administration/agencies/passengergalleries.aspx')]")

    BTN_NUEVO = (By.ID, "btnAddNew")   # "+ Agregar Nueva" → passengergallerydetail.aspx

    TXT_DETAIL   = (By.NAME, f"{_B}txtDetail$txtValue")
    DD_AGENCIES  = (By.NAME, f"{_B}ddAgencies")
    FECHA        = (By.NAME, f"{_B}ctrlDate$txtDateTime")
    CB_PUBLICADO = (By.ID,   "ctl00_cph1_mainTabContainer_pnlDetails_cbPublicado")
    BTN_GUARDAR  = (By.NAME, f"{_B}btnSave")

    TABLA = (By.ID, "ctl00_cph1_gvData")

    @staticmethod
    def fila_por_nombre(nombre):
        return (By.XPATH,
            f"//table[@id='ctl00_cph1_gvData']//td[contains(normalize-space(),\"{nombre}\")]")
