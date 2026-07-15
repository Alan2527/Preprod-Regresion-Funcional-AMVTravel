"""
Page Object de Destinos en el WebAdmin (Ubicación → Destinos, destinations/default.aspx).

"Nuevo" (`btnAddNew`) navega a destinations/detail.aspx (form tabContainer, solapa
Detalle): Nombre + Nombre SEO (txtSEName) + País (ddlCountries) + Publicado.
(La solapa Ciudades / pnlCities es aparte y opcional.)

La lista `gvObjects` es corta → se valida la fila por el sello sin buscador.

Selectores confirmados contra el DOM real (qa.amv.travel).
"""
from selenium.webdriver.common.by import By

_B = "ctl00$cph1$tabContainer$pnlDetails$"
_ID = "ctl00_cph1_tabContainer_pnlDetails_"


class WebAdminDestinationPage:

    MENU_UBICACION = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'javascript:void')]"
        "//span[normalize-space()='Ubicación']")
    SUBMENU = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'/administration/destinations/default.aspx')]"
        "//span[normalize-space()='Destinos']")

    URL_LISTA = "/administration/destinations/default.aspx"
    URL_DETALLE = "destinations/detail.aspx"

    BTN_NUEVO = (By.ID, "btnAddNew")

    TXT_NAME = (By.NAME, f"{_B}txtName$txtValue")
    TXT_SENAME = (By.NAME, f"{_B}txtSEName$txtValue")
    DD_PAIS = (By.NAME, f"{_B}ddlCountries")
    CB_PUBLICADO = (By.ID, f"{_ID}cbPublicado")
    BTN_GUARDAR = (By.NAME, f"{_B}btnSave")

    TABLA = (By.ID, "ctl00_cph1_gvObjects")

    @staticmethod
    def fila_por_nombre(nombre):
        return (By.XPATH,
            f"//table[@id='ctl00_cph1_gvObjects']//td[contains(normalize-space(),\"{nombre}\")]")
