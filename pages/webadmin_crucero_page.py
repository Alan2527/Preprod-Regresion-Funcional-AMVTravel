"""
Page Object de la creación de Cruceros en el WebAdmin (cruises/detail.aspx).
Form con solapas (CruiseTabContainer). Selectores confirmados contra el HTML real.
"""
from selenium.webdriver.common.by import By

_B = "ctl00$cph1$CruiseTabContainer$pnlDetails$"
_ID = "ctl00_cph1_CruiseTabContainer_pnlDetails_"


class WebAdminCruceroPage:

    # ── Menú lateral: Cruceros (acordeón) → Adm. de Cruceros ──────────────────
    MENU_CRUCEROS = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'javascript:void')]"
        "//span[normalize-space()='Cruceros']")
    SUBMENU_ADM_CRUCEROS = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'/administration/cruises/cruises.aspx')]"
        "//span[normalize-space()='Adm. de Cruceros']")

    # ── Botón "Nuevo" (navega a detail.aspx) ──────────────────────────────────
    BTN_NUEVO = (By.ID, "btnAddNew")

    # ── Formulario (CruiseTabContainer / pnlDetails) ──────────────────────────
    TXT_NAME       = (By.NAME, f"{_B}txtName$txtValue")
    DD_CURRENCY    = (By.NAME, f"{_B}ddlCurrency")
    TXT_RATE_MIN   = (By.NAME, f"{_B}txtRateMin$txtValue")
    TXT_RATE_MAX   = (By.NAME, f"{_B}txtRateMax$txtValue")
    DD_NAVY        = (By.NAME, f"{_B}ddlNavy")        # Flota
    DD_CITY_DEP    = (By.NAME, f"{_B}ddlCityDep")     # Ciudad de salida
    DD_CITY_ARR    = (By.NAME, f"{_B}ddlCityArr")     # Ciudad de llegada
    TXT_ORDEN      = (By.NAME, f"{_B}txtOrden$txtValue")
    CB_PUBLICADO   = (By.ID,   f"{_ID}cbPublicado")
    NOMBRE_DESC_ES = (By.NAME, f"{_B}ctrlNameDescQuill$rptrLanguages$ctl00$txtName")
    QUILL_ES = (By.CSS_SELECTOR,
        f"#{_ID}ctrlNameDescQuill_rptrLanguages_ctl00_txtQuill_editor .ql-editor")
    BTN_GUARDAR = (By.NAME, f"{_B}btnSave")

    # ── Solapas (tabs) ────────────────────────────────────────────────────────
    SOLAPAS = {
        "Detalle":   "ctl00_cph1_CruiseTabContainer_pnlDetails_tab",
        "Imagenes":  "ctl00_cph1_CruiseTabContainer_pnlImagenes_tab",
        "Destinos":  "ctl00_cph1_CruiseTabContainer_pnlDestinos_tab",
        "Salidas":   "ctl00_cph1_CruiseTabContainer_pnlSalidas_tab",
        "Cabinas":   "ctl00_cph1_CruiseTabContainer_pnlCabs_tab",
        "Politicas": "ctl00_cph1_CruiseTabContainer_pnlPolicies_tab",
    }
    TAB_CONTAINER = "CruiseTabContainer"

    # ── Lista (grid + buscador) ───────────────────────────────────────────────
    TXT_SEARCH = (By.NAME, "ctl00$cph1$txtSearch")
    BTN_SEARCH = (By.NAME, "ctl00$cph1$btnSearch")
    TABLA = (By.ID, "ctl00_cph1_gvCruises")

    @staticmethod
    def fila_por_nombre(nombre):
        return (By.XPATH,
            f"//table[@id='ctl00_cph1_gvCruises']//td[contains(normalize-space(),\"{nombre}\")]")
