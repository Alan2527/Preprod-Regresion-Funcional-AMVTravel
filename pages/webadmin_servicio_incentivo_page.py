"""
Page Object de la creación de Servicios de incentivo en el WebAdmin.
Lista: incentives/Servicedefault.aspx · Detalle (form): incentives/servicedetail.aspx.

El alta es en una PÁGINA APARTE (servicedetail.aspx), no inline ni modal.
Campos bajo `ctl00$cph1$tabsIncentiveService$pnlDetails$`.
- Ciudad (ddlCity) puede disparar postback que recarga "Servicio Relacionado" (ddlService).
- "Detalle de Incentivos" tiene, por idioma, un Nombre (input) + un editor Quill.
Selectores confirmados contra el HTML real (preprod.amv.travel).
"""
from selenium.webdriver.common.by import By

_B  = "ctl00$cph1$tabsIncentiveService$pnlDetails$"
_ID = "ctl00_cph1_tabsIncentiveService_pnlDetails_"


class WebAdminServicioIncentivoPage:

    # ── Menú lateral: Servicios (acordeón) → Servicios de incentivo ───────────
    MENU_SERVICIOS = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']"
        "//a[contains(@href,'javascript:void')]"
        "//span[normalize-space()='Servicios']")
    SUBMENU_INCENTIVOS = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']"
        "//a[contains(@href,'/administration/incentives/Servicedefault.aspx')]"
        "//span[normalize-space()='Servicios de incentivo']")

    # ── Botón "+ Agregar Servicio" (navega a servicedetail.aspx por location.href) ──
    BTN_AGREGAR = (By.XPATH, "//input[@value='+ Agregar Servicio']")

    # ── Formulario (servicedetail.aspx) ───────────────────────────────────────
    TXT_NAME       = (By.NAME, f"{_B}txtName")           # input directo (sin $txtValue)
    DD_CITY        = (By.NAME, f"{_B}ddlCity")
    DD_SERVICE     = (By.NAME, f"{_B}ddlService")        # Servicio Relacionado (dep. de ciudad)
    DD_TYPE        = (By.NAME, f"{_B}ddlServiceType")
    DD_DESTINATION = (By.NAME, f"{_B}ddlDestination")
    TXT_ORDEN      = (By.NAME, f"{_B}txtDisplayOrder$txtValue")
    CB_DESTACADO   = (By.ID,   f"{_ID}chkGreat")
    CB_PUBLICADO   = (By.ID,   f"{_ID}cbPublished")

    # Detalle de Incentivos (ES = ctl00): Nombre (input) + Quill.
    DETALLE_NOMBRE_ES = (By.NAME, f"{_B}ctrlIncentiveDetailQuill$rptrLanguages$ctl00$txtName")
    QUILL_ES = (By.CSS_SELECTOR,
        f"#{_ID}ctrlIncentiveDetailQuill_rptrLanguages_ctl00_txtQuill_editor .ql-editor")

    # ── Guardar ───────────────────────────────────────────────────────────────
    BTN_GUARDAR = (By.NAME, f"{_B}btnSave")

    # ── Tabla de la lista ─────────────────────────────────────────────────────
    TABLA = (By.ID, "ctl00_cph1_gvIncentiveService")

    @staticmethod
    def opcion_service(texto):
        # Opción de "Servicio Relacionado" tras el postback de ciudad.
        return (By.XPATH,
            f"//select[@name='{_B}ddlService']/option[contains(normalize-space(),\"{texto}\")]")

    @staticmethod
    def fila_por_nombre(nombre):
        return (By.XPATH,
            f"//table[@id='ctl00_cph1_gvIncentiveService']"
            f"//td[contains(normalize-space(),\"{nombre}\")]")
