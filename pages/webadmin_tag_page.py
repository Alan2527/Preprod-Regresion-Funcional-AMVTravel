"""
Page Object de la creación de Tags (de Servicios) en el WebAdmin.

Particularidades:
- El botón "Nuevo" (id="btnAddNew") abre un MODAL (ModalPopupExtender del
  AjaxControlToolkit) vía openModalExtension(); el form vive en #ctl00_cph1_pnlPopup.
- El "Guardar" (btnNewTag) es un submit → postback full que recarga la lista.
- La lista se filtra con un buscador (txtSearch + btnSearch). La fila muestra el
  nombre con un sufijo " #<id>" (ej: "Tag Test ... 18/06/2026 15:57:35 #7").
"""
from selenium.webdriver.common.by import By


class WebAdminTagPage:

    # ── Menú lateral: Servicios (acordeón) → Tags ─────────────────────────────
    MENU_SERVICIOS = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']"
        "//a[contains(@href,'javascript:void')]"
        "//span[normalize-space()='Servicios']")
    SUBMENU_TAGS = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']"
        "//a[contains(@href,'/administration/services/tags.aspx')]"
        "//span[normalize-space()='Tags']")

    # ── Botón "Nuevo" (abre el modal) ─────────────────────────────────────────
    BTN_NUEVO = (By.ID, "btnAddNew")

    # ── Modal "Agregar nuevo tag" ─────────────────────────────────────────────
    MODAL       = (By.ID, "ctl00_cph1_pnlPopup")
    TXT_NAME    = (By.ID, "ctl00_cph1_txtName")
    BTN_GUARDAR = (By.ID, "ctl00_cph1_btnNewTag")   # <input value="Guardar"> (submit)

    # ── Buscador de la lista ──────────────────────────────────────────────────
    TXT_SEARCH = (By.ID, "ctl00_cph1_txtSearch")    # placeholder/label "Nombre"
    BTN_SEARCH = (By.ID, "ctl00_cph1_btnSearch")    # <input value="Buscar"> (postback)

    # ── Tabla de la lista ─────────────────────────────────────────────────────
    TABLA = (By.ID, "ctl00_cph1_gvData")

    @staticmethod
    def fila_por_nombre(nombre):
        # El nombre completo (con fecha/hora) aparece en el <td>; normalize-space
        # tolera el padding del HTML de la grilla. Se matchea por el sello (ASCII).
        return (By.XPATH,
            f"//table[@id='ctl00_cph1_gvData']"
            f"//td[contains(normalize-space(),\"{nombre}\")]")
