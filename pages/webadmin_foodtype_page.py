"""
Page Object de Tipos de Comida en el WebAdmin
(Ubicación → Tipos de Comida, restaurants/foodtypes.aspx).

Flujo de creación: la lista tiene "+ Agregar Nuevo" (`btnAddNew`) que navega a un
detail APARTE (foodtypesdetail.aspx). El form tiene una sola solapa (Detalle) con:
Nombre + control "Nombre y Descripción" localizado en 4 idiomas (Quill) + Publicado.

⚠ La lista NO tiene buscador → la validación de la fila se hace directamente sobre
el grid `gvData` buscando el <td> con el sello (fecha/hora de la corrida).

Selectores confirmados contra el DOM real (qa.amv.travel, mismos IDs ASP.NET que
preprod).
"""
from selenium.webdriver.common.by import By

_B = "ctl00$cph1$mainTabContainer$pnlDetails$"
_ID = "ctl00_cph1_mainTabContainer_pnlDetails_"
_QUILL = "ctrlNameDescQuill"   # control del "Nombre y Descripción" localizado


class WebAdminFoodTypePage:

    # ── Menú lateral: Ubicación (acordeón) → Tipos de Comida ───────────────────
    MENU_UBICACION = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'javascript:void')]"
        "//span[normalize-space()='Ubicación']")
    SUBMENU = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'/administration/restaurants/foodtypes.aspx')]"
        "//span[normalize-space()='Tipos de Comida']")

    URL_LISTA = "/administration/restaurants/foodtypes.aspx"
    URL_DETALLE = "foodtypesdetail.aspx"

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
