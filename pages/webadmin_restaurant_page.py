"""
Page Object de Restaurantes en el WebAdmin
(Ubicación → Restaurantes, restaurants/default.aspx).

"+ Agregar Nuevo" (`btnAddNew`) navega a restaurants/detail.aspx (form
mainTabContainer, solapa Detalle). Requeridos usados: Nombre + Ciudad (ddCity, dispara
postback que recarga Hotel/Barrio) + Orden + Nombre/Descripción ES (Quill) + Publicado.
Imagen y precios son opcionales → no se tocan.

⚠ ddCity tiene ~700 opciones (formato "Ciudad | País") y dispara postback al elegir.

Selectores confirmados contra el DOM real (qa.amv.travel).
"""
from selenium.webdriver.common.by import By

_B = "ctl00$cph1$mainTabContainer$pnlDetails$"
_ID = "ctl00_cph1_mainTabContainer_pnlDetails_"
_QUILL = "ctrlDescriptionQuill"


class WebAdminRestaurantPage:

    MENU_UBICACION = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'javascript:void')]"
        "//span[normalize-space()='Ubicación']")
    SUBMENU = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'/administration/restaurants/default.aspx')]"
        "//span[normalize-space()='Restaurantes']")

    URL_LISTA = "/administration/restaurants/default.aspx"
    URL_DETALLE = "restaurants/detail.aspx"

    BTN_NUEVO = (By.ID, "btnAddNew")

    TXT_NAME = (By.NAME, f"{_B}txtName$txtValue")
    TXT_ORDEN = (By.NAME, f"{_B}txtDisplayOrder$txtValue")
    DD_CIUDAD = (By.NAME, f"{_B}ddCity")
    NOMBRE_ES = (By.NAME, f"{_B}{_QUILL}$rptrLanguages$ctl00$txtName")
    QUILL_ES = (By.CSS_SELECTOR,
        f"#{_ID}{_QUILL}_rptrLanguages_ctl00_txtQuill_editor .ql-editor")
    CB_PUBLICADO = (By.ID, f"{_ID}cbPublicado")
    BTN_GUARDAR = (By.NAME, f"{_B}btnSave")

    TXT_SEARCH = (By.NAME, "ctl00$cph1$txtSearch")
    BTN_SEARCH = (By.NAME, "ctl00$cph1$btnSearch")
    TABLA = (By.ID, "ctl00_cph1_gvData")

    @staticmethod
    def fila_por_nombre(nombre):
        return (By.XPATH,
            f"//table[@id='ctl00_cph1_gvData']//td[contains(normalize-space(),\"{nombre}\")]")
