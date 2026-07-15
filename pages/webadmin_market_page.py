"""
Page Object de Mercados en el WebAdmin (Finanzas → Mercados, markets/default.aspx).

"Nuevo" (`btnAddNew`) navega a markets/detail.aspx (tabContainer/pnlDetails):
Nombre + Markup + Travel Sale + Idioma (ddlLanguages) + Publicado.
Lista `gvObjects` con buscador.

Selectores confirmados contra el DOM real (qa.amv.travel).
"""
from selenium.webdriver.common.by import By

_B = "ctl00$cph1$tabContainer$pnlDetails$"
_ID = "ctl00_cph1_tabContainer_pnlDetails_"


class WebAdminMarketPage:

    MENU_FINANZAS = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'javascript:void')]"
        "//span[normalize-space()='Finanzas']")
    SUBMENU = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'/administration/markets/default.aspx')]"
        "//span[normalize-space()='Mercados']")

    URL_LISTA = "/administration/markets/default.aspx"
    URL_DETALLE = "markets/detail.aspx"

    BTN_NUEVO = (By.ID, "btnAddNew")

    TXT_NAME = (By.NAME, f"{_B}txtName$txtValue")
    TXT_MARKUP = (By.NAME, f"{_B}txtMarkup$txtValue")
    TXT_TRAVELSALE = (By.NAME, f"{_B}txtTravelSale$txtValue")
    DD_IDIOMA = (By.NAME, f"{_B}ddlLanguages")
    CB_PUBLICADO = (By.ID, f"{_ID}cbPublicado")
    BTN_GUARDAR = (By.NAME, f"{_B}btnSave")

    TXT_SEARCH = (By.NAME, "ctl00$cph1$txtSearch")
    BTN_SEARCH = (By.NAME, "ctl00$cph1$btnSearch")
    TABLA = (By.ID, "ctl00_cph1_gvObjects")

    @staticmethod
    def fila_por_nombre(nombre):
        return (By.XPATH,
            f"//table[@id='ctl00_cph1_gvObjects']//td[contains(normalize-space(),\"{nombre}\")]")
