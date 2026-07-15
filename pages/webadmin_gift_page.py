"""
Page Object de Gifts en el WebAdmin (Contenidos → Gifts, gifts/default.aspx).

"+ Agregar Nuevo" (`btnAddNew`) navega a gifts/detail.aspx (mainTabContainer/pnlDetails):
Nombre + Orden + Nombre/Descripción localizado (Quill, 4 idiomas) + Publicado.
La imagen (fuPicture) es opcional → no se toca. Lista `gvData` con buscador.

Selectores confirmados contra el DOM real (qa.amv.travel).
"""
from selenium.webdriver.common.by import By

_B = "ctl00$cph1$mainTabContainer$pnlDetails$"
_ID = "ctl00_cph1_mainTabContainer_pnlDetails_"
_QUILL = "ctrlNameDescQuill"


class WebAdminGiftPage:

    MENU_CONTENIDOS = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'javascript:void')]"
        "//span[normalize-space()='Contenidos']")
    SUBMENU = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'/administration/gifts/default.aspx')]"
        "//span[normalize-space()='Gifts']")

    URL_LISTA = "/administration/gifts/default.aspx"
    URL_DETALLE = "gifts/detail.aspx"

    BTN_NUEVO = (By.ID, "btnAddNew")

    TXT_NAME = (By.NAME, f"{_B}txtName$txtValue")
    TXT_ORDEN = (By.NAME, f"{_B}txtDisplayOrder$txtValue")
    NOMBRE_ES = (By.NAME, f"{_B}{_QUILL}$rptrLanguages$ctl00$txtName")
    QUILL_ES = (By.CSS_SELECTOR,
        f"#{_ID}{_QUILL}_rptrLanguages_ctl00_txtQuill_editor .ql-editor")
    CB_PUBLICADO = (By.ID, f"{_ID}cbPublished")
    BTN_GUARDAR = (By.NAME, f"{_B}btnSave")

    TXT_SEARCH = (By.NAME, "ctl00$cph1$txtSearch")
    BTN_SEARCH = (By.NAME, "ctl00$cph1$btnSearch")
    TABLA = (By.ID, "ctl00_cph1_gvData")

    @staticmethod
    def fila_por_nombre(nombre):
        return (By.XPATH,
            f"//table[@id='ctl00_cph1_gvData']//td[contains(normalize-space(),\"{nombre}\")]")
