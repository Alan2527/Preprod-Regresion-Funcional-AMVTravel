"""
Page Object de Barrios en el WebAdmin (Ubicación → Barrios, types/districts.aspx).

⚠ A diferencia del resto, "Crear Barrio" (`ctl00_cphActions_btnNew`) abre un MODAL
en la MISMA página (no navega a un detail). El form del modal es mínimo:
Nombre + Ciudad (ddlCities) + Guardar.

La lista tiene buscador → se valida la fila por el sello tras guardar.

Selectores confirmados contra el DOM real (qa.amv.travel).
"""
from selenium.webdriver.common.by import By


class WebAdminDistrictPage:

    MENU_UBICACION = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'javascript:void')]"
        "//span[normalize-space()='Ubicación']")
    SUBMENU = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'/administration/types/districts.aspx')]"
        "//span[normalize-space()='Barrios']")

    URL_LISTA = "/administration/types/districts.aspx"

    # Botón que abre el modal.
    BTN_NUEVO = (By.ID, "ctl00_cphActions_btnNew")

    # Form del modal.
    TXT_NAME = (By.NAME, "ctl00$cph1$txtName$txtValue")
    DD_CIUDAD = (By.NAME, "ctl00$cph1$ddlCities")
    BTN_GUARDAR = (By.NAME, "ctl00$cph1$btnSave")

    # Lista (grid + buscador).
    TXT_SEARCH = (By.NAME, "ctl00$cph1$txtSearch")
    BTN_SEARCH = (By.NAME, "ctl00$cph1$btnSearch")
    TABLA = (By.ID, "ctl00_cph1_gvDistricts")

    @staticmethod
    def fila_por_nombre(nombre):
        return (By.XPATH,
            f"//table[@id='ctl00_cph1_gvDistricts']//td[contains(normalize-space(),\"{nombre}\")]")
