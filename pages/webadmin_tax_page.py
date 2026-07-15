"""
Page Object de Impuestos en el WebAdmin (Finanzas → Impuestos, Taxes/Taxes.aspx).

La pantalla tiene 2 grillas (impuestos generales `gvTaxes` y defaults de hotelería).
Se automatiza el impuesto GENERAL: "Nuevo" (`ctl00_cphActions_btnNew`) abre un MODAL
(BenchmarkTabContainer bajo pnlGeneral): Nombre + Orden + Valor → Guardar.

Selectores confirmados contra el DOM real (qa.amv.travel).
"""
from selenium.webdriver.common.by import By

_B = "ctl00$cph1$tabMain$pnlGeneral$BenchmarkTabContainer$pnlDetails$"


class WebAdminTaxPage:

    MENU_FINANZAS = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'javascript:void')]"
        "//span[normalize-space()='Finanzas']")
    SUBMENU = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'/administration/Taxes/Taxes.aspx')]"
        "//span[normalize-space()='Impuestos']")

    URL_LISTA = "/administration/Taxes/Taxes.aspx"

    BTN_NUEVO = (By.ID, "ctl00_cphActions_btnNew")

    TXT_NAME = (By.NAME, f"{_B}txtName$txtValue")
    TXT_ORDEN = (By.NAME, f"{_B}txtOrden$txtValue")
    TXT_VALOR = (By.NAME, f"{_B}txtValue$txtValue")
    BTN_GUARDAR = (By.NAME, f"{_B}btnSave")

    TABLA = (By.ID, "ctl00_cph1_tabMain_pnlGeneral_gvTaxes")

    @staticmethod
    def fila_por_nombre(nombre):
        return (By.XPATH,
            f"//table[@id='ctl00_cph1_tabMain_pnlGeneral_gvTaxes']"
            f"//td[contains(normalize-space(),\"{nombre}\")]")
