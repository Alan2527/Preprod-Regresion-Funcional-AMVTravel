"""
Page Object de Tipo de Puntos de Interés en el WebAdmin
(Ubicación → Tipo de Puntos Int., benchmarks/benchmarktypes.aspx).

Misma estructura que Tipos de Comida: la lista tiene "+ Agregar Nuevo" (`btnAddNew`)
que navega a un detail aparte (benchmarktypesdetail.aspx) con una solapa (Detalle):
Nombre + control "Nombre" localizado en 4 idiomas (Quill) + Publicado.
La única diferencia con Tipos de Comida es el nombre del control Quill
(`ctrlNameQuill` en vez de `ctrlNameDescQuill`) y las URLs.

⚠ La lista NO tiene buscador → se valida la fila directamente en el grid `gvData`.

Selectores confirmados contra el DOM real (qa.amv.travel, mismos IDs ASP.NET que
preprod).
"""
from selenium.webdriver.common.by import By

_B = "ctl00$cph1$mainTabContainer$pnlDetails$"
_ID = "ctl00_cph1_mainTabContainer_pnlDetails_"
_QUILL = "ctrlNameQuill"


class WebAdminBenchmarkTypePage:

    # ── Menú lateral: Ubicación (acordeón) → Tipo de Puntos Int. ───────────────
    MENU_UBICACION = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'javascript:void')]"
        "//span[normalize-space()='Ubicación']")
    SUBMENU = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'/administration/benchmarks/benchmarktypes.aspx')]"
        "//span[normalize-space()='Tipo de Puntos Int.']")

    URL_LISTA = "/administration/benchmarks/benchmarktypes.aspx"
    URL_DETALLE = "benchmarktypesdetail.aspx"

    # ── Botón "Agregar Nuevo" (navega al detail) ──────────────────────────────
    BTN_NUEVO = (By.ID, "btnAddNew")

    # ── Formulario (detail, solapa Detalle) ───────────────────────────────────
    TXT_NAME = (By.NAME, f"{_B}txtName$txtValue")
    NOMBRE_ES = (By.NAME, f"{_B}{_QUILL}$rptrLanguages$ctl00$txtName")
    QUILL_ES = (By.CSS_SELECTOR,
        f"#{_ID}{_QUILL}_rptrLanguages_ctl00_txtQuill_editor .ql-editor")
    CB_PUBLICADO = (By.ID, f"{_ID}cbPublicado")
    BTN_GUARDAR = (By.NAME, f"{_B}btnSave")

    # ── Lista (grid, sin buscador) ────────────────────────────────────────────
    TABLA = (By.ID, "ctl00_cph1_gvData")

    @staticmethod
    def fila_por_nombre(nombre):
        return (By.XPATH,
            f"//table[@id='ctl00_cph1_gvData']//td[contains(normalize-space(),\"{nombre}\")]")
