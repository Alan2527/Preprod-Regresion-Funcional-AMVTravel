"""
Page Object de la creación de Series en el WebAdmin (series/Detail.aspx).
Form con solapas (SerieTabContainer). Detalle simple: Nombre + Orden + Publicado +
Nombre y Descripción (ES + Quill). Sólo Nombre es requerido.

Selectores confirmados contra el HTML real (preprod.amv.travel).
"""
from selenium.webdriver.common.by import By

_B = "ctl00$cph1$SerieTabContainer$pnlDetails$"
_ID = "ctl00_cph1_SerieTabContainer_pnlDetails_"


class WebAdminSeriePage:

    # ── Menú lateral: Circuitos (acordeón) → Series ───────────────────────────
    MENU_CIRCUITOS = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'javascript:void')]"
        "//span[normalize-space()='Circuitos']")
    SUBMENU_SERIES = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'/administration/series/')]"
        "//span[normalize-space()='Series']")

    # ── Botón "Crear" (navega a Detail.aspx) ──────────────────────────────────
    BTN_NUEVO = (By.ID, "btnAddNew")

    # ── Formulario (SerieTabContainer / pnlDetails) ───────────────────────────
    TXT_NAME       = (By.NAME, f"{_B}txtName$txtValue")
    TXT_ORDEN      = (By.NAME, f"{_B}txtOrden")          # sin wrapper $txtValue
    CB_PUBLICADO   = (By.ID,   f"{_ID}cbPublicado")
    NOMBRE_DESC_ES = (By.NAME, f"{_B}ctrlNameDescQuill$rptrLanguages$ctl00$txtName")
    QUILL_ES = (By.CSS_SELECTOR,
        f"#{_ID}ctrlNameDescQuill_rptrLanguages_ctl00_txtQuill_editor .ql-editor")
    BTN_GUARDAR = (By.NAME, f"{_B}SaveButton")

    # ── Solapas (tabs) ────────────────────────────────────────────────────────
    SOLAPAS = {
        "Detalle":  "ctl00_cph1_SerieTabContainer_pnlDetails_tab",
        "Paquetes": "ctl00_cph1_SerieTabContainer_pnlPackage_tab",
        "Salidas":  "ctl00_cph1_SerieTabContainer_pnlSeriesDepartures_tab",
        "Tarifas":  "ctl00_cph1_SerieTabContainer_pnlSeriesTariffs_tab",
        "Cupos":    "ctl00_cph1_SerieTabContainer_pnlSeriesQuotas_tab",
    }
    TAB_CONTAINER = "SerieTabContainer"

    # ── Lista (grid + buscador) ───────────────────────────────────────────────
    TXT_SEARCH = (By.NAME, "ctl00$cph1$txtSearchName")
    BTN_SEARCH = (By.NAME, "ctl00$cph1$btnSearch")
    TABLA = (By.ID, "ctl00_cph1_gvSeries")

    @staticmethod
    def fila_por_nombre(nombre):
        return (By.XPATH,
            f"//table[@id='ctl00_cph1_gvSeries']"
            f"//td[contains(normalize-space(),\"{nombre}\")]")
