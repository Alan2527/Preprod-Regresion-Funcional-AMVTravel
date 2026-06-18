"""
Page Object de la creación de Vehículos en el WebAdmin (vehicletypes/default.aspx).

Estructura idéntica a Tipos de servicio (nombre + 4 traducciones + Publicado),
pero con Capacity From / Capacity To en vez de Orden. Form INLINE (se despliega
bajo la tabla al tocar "Nuevo"), no es modal.

Selectores confirmados contra el HTML real (preprod.amv.travel).
"""
from selenium.webdriver.common.by import By


class WebAdminVehiculoPage:

    # ── Menú lateral: Servicios (acordeón) → Vehículos ────────────────────────
    MENU_SERVICIOS = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']"
        "//a[contains(@href,'javascript:void')]"
        "//span[normalize-space()='Servicios']")
    SUBMENU_VEHICULOS = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']"
        "//a[contains(@href,'/administration/vehicletypes/default.aspx')]"
        "//span[normalize-space()='Vehículos']")

    # ── Botón "Nuevo" (submit → despliega el form inline) ─────────────────────
    BTN_NUEVO = (By.NAME, "ctl00$cphActions$btnNew")

    # ── Formulario ────────────────────────────────────────────────────────────
    TXT_NAME          = (By.NAME, "ctl00$cph1$txtName$txtValue")
    TXT_CAPACITY_FROM = (By.NAME, "ctl00$cph1$txtCapacityFrom$txtValue")
    TXT_CAPACITY_TO   = (By.NAME, "ctl00$cph1$txtCapacityTo$txtValue")
    CB_PUBLICADO      = (By.ID, "ctl00_cph1_cbPublicado")

    # Traducciones por idioma: ctrl0=Español, ctrl1=English, ctrl2=Portuguese, ctrl3=Italian.
    @staticmethod
    def traduccion(indice):
        return (By.NAME, f"ctl00$cph1$lvTranslations$ctrl{indice}$txtLocName$txtValue")

    # ── Guardar ───────────────────────────────────────────────────────────────
    BTN_GUARDAR = (By.NAME, "ctl00$cph1$btnSave")

    # ── Buscador de la lista ──────────────────────────────────────────────────
    TXT_SEARCH = (By.ID, "ctl00_cph1_txtSearch")
    BTN_SEARCH = (By.ID, "ctl00_cph1_btnSearch")

    # ── Tabla de la lista ─────────────────────────────────────────────────────
    TABLA = (By.ID, "ctl00_cph1_gvTypes")

    @staticmethod
    def fila_por_nombre(nombre):
        return (By.XPATH,
            f"//table[@id='ctl00_cph1_gvTypes']"
            f"//td[contains(normalize-space(),\"{nombre}\")]")
