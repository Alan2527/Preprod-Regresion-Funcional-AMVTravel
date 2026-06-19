"""
Page Object de la creación de Cabinas en el WebAdmin (cruisecabs/detail.aspx).
Form con solapas (tabContainer, en minúscula). Selectores confirmados contra el HTML real.
"""
from selenium.webdriver.common.by import By

_B = "ctl00$cph1$tabContainer$pnlDetails$"
_ID = "ctl00_cph1_tabContainer_pnlDetails_"


class WebAdminCabinaPage:

    # ── Menú lateral: Cruceros (acordeón) → Cabinas ───────────────────────────
    MENU_CRUCEROS = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'javascript:void')]"
        "//span[normalize-space()='Cruceros']")
    SUBMENU_CABINAS = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'/administration/cruisecabs/default.aspx')]"
        "//span[normalize-space()='Cabinas']")

    # ── Botón "Nuevo" (navega a detail.aspx) ──────────────────────────────────
    BTN_NUEVO = (By.ID, "btnAddNew")

    # ── Formulario (tabContainer / pnlDetails) ────────────────────────────────
    TXT_NAME       = (By.NAME, f"{_B}txtName$txtValue")
    DD_CRUISE      = (By.NAME, f"{_B}ddlCruise")      # Crucero al que pertenece
    DD_CURRENCY    = (By.NAME, f"{_B}ddlCurrency")
    TXT_MIN_RATE   = (By.NAME, f"{_B}txtMinRate$txtValue")
    TXT_CAPACIDAD  = (By.NAME, f"{_B}txtCapacidad$txtValue")
    DD_TYPE        = (By.NAME, f"{_B}ddlType")        # Tipo de cabina
    CB_PUBLICADO   = (By.ID,   f"{_ID}cbPublicado")
    NOMBRE_DESC_ES = (By.NAME, f"{_B}ctrlNameDescQuill$rptrLanguages$ctl00$txtName")
    QUILL_ES = (By.CSS_SELECTOR,
        f"#{_ID}ctrlNameDescQuill_rptrLanguages_ctl00_txtQuill_editor .ql-editor")
    BTN_GUARDAR = (By.NAME, f"{_B}btnSave")

    # ── Solapas (tabs) ────────────────────────────────────────────────────────
    SOLAPAS = {
        "Detalle":  "ctl00_cph1_tabContainer_pnlDetails_tab",
        "Imagenes": "ctl00_cph1_tabContainer_pnlImagenes_tab",
        "Tarifas":  "ctl00_cph1_tabContainer_pnlCabRates_tab",
    }
    TAB_CONTAINER = "tabContainer"

    # ── Lista (grid + buscador) ───────────────────────────────────────────────
    TXT_SEARCH = (By.NAME, "ctl00$cph1$txtSearch")
    BTN_SEARCH = (By.NAME, "ctl00$cph1$btnSearch")
    TABLA = (By.ID, "ctl00_cph1_gvCabs")

    @staticmethod
    def fila_por_nombre(nombre):
        return (By.XPATH,
            f"//table[@id='ctl00_cph1_gvCabs']//td[contains(normalize-space(),\"{nombre}\")]")
