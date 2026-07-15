"""
Page Object de Ciudades en el WebAdmin (Ubicación → Ciudades, cities/default.aspx).

"Crear Ciudad" (`btnAddNew`) navega a cities/detail.aspx (form CityTabContainer,
solapa Detalle): Nombre + Código IATA (opcional) + Orden + Markup (opcional) +
País (ddlCountries) + descripción Quill (opcional) + Publicado.

Selectores confirmados contra el DOM real (qa.amv.travel).
"""
from selenium.webdriver.common.by import By

_B = "ctl00$cph1$CityTabContainer$pnlDetails$"
_ID = "ctl00_cph1_CityTabContainer_pnlDetails_"


class WebAdminCityPage:

    MENU_UBICACION = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'javascript:void')]"
        "//span[normalize-space()='Ubicación']")
    SUBMENU = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'/administration/cities/default.aspx')]"
        "//span[normalize-space()='Ciudades']")

    URL_LISTA = "/administration/cities/default.aspx"
    URL_DETALLE = "cities/detail.aspx"

    BTN_NUEVO = (By.ID, "btnAddNew")

    TXT_NAME = (By.NAME, f"{_B}txtName$txtValue")
    TXT_ORDEN = (By.NAME, f"{_B}txtDisplayOrder$txtValue")
    DD_PAIS = (By.NAME, f"{_B}ddlCountries")
    CB_PUBLICADO = (By.ID, f"{_ID}cbPublicado")
    BTN_GUARDAR = (By.NAME, f"{_B}btnSave")

    TXT_SEARCH = (By.NAME, "ctl00$cph1$txtSearch")
    BTN_SEARCH = (By.NAME, "ctl00$cph1$btnSearch")
    TABLA = (By.ID, "ctl00_cph1_gvCities")

    @staticmethod
    def fila_por_nombre(nombre):
        return (By.XPATH,
            f"//table[@id='ctl00_cph1_gvCities']//td[contains(normalize-space(),\"{nombre}\")]")
