"""
Page Object de la creación de Comodidades en el WebAdmin (types/serviceamenities.aspx).

Form INLINE (se despliega bajo la tabla al tocar "Nuevo"). Estructura simple:
Nombre (único) + 4 traducciones (ES/EN/PT/IT) + Publicado. Sin orden.

Selectores confirmados contra el HTML real (preprod.amv.travel).
"""
from selenium.webdriver.common.by import By


class WebAdminComodidadPage:

    # ── Menú lateral: Servicios (acordeón) → Comodidades ──────────────────────
    MENU_SERVICIOS = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']"
        "//a[contains(@href,'javascript:void')]"
        "//span[normalize-space()='Servicios']")
    SUBMENU_COMODIDADES = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']"
        "//a[contains(@href,'/administration/types/serviceamenities.aspx')]"
        "//span[normalize-space()='Comodidades']")

    # ── Botón "Nuevo" (submit → despliega el form inline) ─────────────────────
    BTN_NUEVO = (By.NAME, "ctl00$cphActions$btnNew")

    # ── Formulario ────────────────────────────────────────────────────────────
    TXT_NAME     = (By.NAME, "ctl00$cph1$txtName$txtValue")
    CB_PUBLICADO = (By.ID, "ctl00_cph1_cbPublicado")

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
    TABLA = (By.ID, "ctl00_cph1_gvServiceAmenities")

    @staticmethod
    def fila_por_nombre(nombre):
        return (By.XPATH,
            f"//table[@id='ctl00_cph1_gvServiceAmenities']"
            f"//td[contains(normalize-space(),\"{nombre}\")]")
