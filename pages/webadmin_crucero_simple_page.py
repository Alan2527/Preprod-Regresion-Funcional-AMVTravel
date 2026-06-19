"""
Page Object COMPARTIDO de Flotas y Tipos de Cabinas del WebAdmin.
Ambas son listas INLINE (lista + form en la misma página, grid gvTypes) con un form
mínimo: Nombre + Publicado. Sólo cambia el submenú/URL.

- Flotas: cruises/cruisenavies.aspx
- Tipos de Cabinas: cruisecabs/cruisecabtypes.aspx
Selectores confirmados contra el HTML real (preprod.amv.travel).
"""
from selenium.webdriver.common.by import By


class WebAdminCruceroSimplePage:

    # ── Menú lateral: Cruceros (acordeón) → submenús ──────────────────────────
    MENU_CRUCEROS = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'javascript:void')]"
        "//span[normalize-space()='Cruceros']")
    SUBMENU_FLOTAS = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'/administration/cruises/cruisenavies.aspx')]"
        "//span[normalize-space()='Flotas']")
    SUBMENU_TIPOS_CABINAS = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'/administration/cruisecabs/cruisecabtypes.aspx')]"
        "//span[normalize-space()='Tipos de Cabinas']")

    # ── Botón "Nuevo" (despliega el form inline) ──────────────────────────────
    BTN_NUEVO = (By.NAME, "ctl00$cphActions$btnNew")

    # ── Formulario inline ─────────────────────────────────────────────────────
    TXT_NAME     = (By.NAME, "ctl00$cph1$txtName$txtValue")
    CB_PUBLICADO = (By.ID,   "ctl00_cph1_cbPublicado")
    BTN_GUARDAR  = (By.NAME, "ctl00$cph1$btnSave")

    # ── Buscador + tabla ──────────────────────────────────────────────────────
    TXT_SEARCH = (By.NAME, "ctl00$cph1$txtSearch")
    BTN_SEARCH = (By.NAME, "ctl00$cph1$btnSearch")
    TABLA = (By.ID, "ctl00_cph1_gvTypes")

    @staticmethod
    def fila_por_nombre(nombre):
        return (By.XPATH,
            f"//table[@id='ctl00_cph1_gvTypes']//td[contains(normalize-space(),\"{nombre}\")]")
