"""
Page Object de Regiones en el WebAdmin (Ubicación → Regiones, regions/default.aspx).

"Crear Región" (`btnAddNew`) navega a regions/detail.aspx (form RegionTabContainer,
solapa Detalle): Nombre + País (ddlCountries) + Ciudades (lstCities, dependiente del
país, OPCIONAL) + Publicado + Mostrar en el sitio.

Selectores confirmados contra el DOM real (qa.amv.travel).
"""
from selenium.webdriver.common.by import By

_B = "ctl00$cph1$RegionTabContainer$pnlDetails$"
_ID = "ctl00_cph1_RegionTabContainer_pnlDetails_"


class WebAdminRegionPage:

    MENU_UBICACION = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'javascript:void')]"
        "//span[normalize-space()='Ubicación']")
    SUBMENU = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'/administration/regions/default.aspx')]"
        "//span[normalize-space()='Regiones']")

    URL_LISTA = "/administration/regions/default.aspx"
    URL_DETALLE = "regions/detail.aspx"

    BTN_NUEVO = (By.ID, "btnAddNew")

    TXT_NAME = (By.NAME, f"{_B}txtName$txtValue")
    DD_PAIS = (By.NAME, f"{_B}ddlCountries")
    CB_PUBLICADO = (By.ID, f"{_ID}cbPublicado")
    BTN_GUARDAR = (By.NAME, f"{_B}btnSave")

    TXT_SEARCH = (By.NAME, "ctl00$cph1$txtSearch")
    BTN_SEARCH = (By.NAME, "ctl00$cph1$btnSearch")
    TABLA = (By.ID, "ctl00_cph1_gvRegions")

    @staticmethod
    def fila_por_nombre(nombre):
        return (By.XPATH,
            f"//table[@id='ctl00_cph1_gvRegions']//td[contains(normalize-space(),\"{nombre}\")]")
