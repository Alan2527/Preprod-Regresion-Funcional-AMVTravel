"""
Page Object de la creación de Tipos de servicio en el WebAdmin (servicetypes.aspx).

Estructura idéntica a Categorías (nombre + 4 traducciones + orden), más dos toggles:
Publicado y "Es servicio adicional". El form es INLINE (se despliega bajo la tabla
al tocar "Nuevo"), no es un modal.

Selectores confirmados contra el HTML real (qa.amv.travel, mismos IDs ASP.NET que preprod).
⚠ "Es servicio adicional" (cbIsAdditional) NO se toca: al tildarlo dispara un popup de
   confirmación (mpeIsAdditional). Lo dejamos OFF.
"""
from selenium.webdriver.common.by import By


class WebAdminTipoServicioPage:

    # ── Menú lateral: Servicios (acordeón) → Tipos de servicio ────────────────
    MENU_SERVICIOS = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']"
        "//a[contains(@href,'javascript:void')]"
        "//span[normalize-space()='Servicios']")
    SUBMENU_TIPOS = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']"
        "//a[contains(@href,'/administration/services/servicetypes.aspx')]"
        "//span[normalize-space()='Tipos de servicio']")

    # ── Botón "Nuevo" (submit → despliega el form inline) ─────────────────────
    BTN_NUEVO = (By.NAME, "ctl00$cphActions$btnNew")

    # ── Formulario ────────────────────────────────────────────────────────────
    TXT_NAME  = (By.NAME, "ctl00$cph1$txtName$txtValue")
    TXT_ORDEN = (By.NAME, "ctl00$cph1$txtOrden$txtValue")
    CB_PUBLICADO     = (By.ID, "ctl00_cph1_cbPublicado")
    CB_IS_ADDITIONAL = (By.ID, "ctl00_cph1_cbIsAdditional")  # se deja OFF (no tocar)

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
    TABLA = (By.ID, "ctl00_cph1_gvServiceTypes")

    @staticmethod
    def fila_por_nombre(nombre):
        # El nombre completo (con fecha/hora) aparece en el <td>; normalize-space
        # tolera el padding del HTML. Se matchea por el sello (ASCII).
        return (By.XPATH,
            f"//table[@id='ctl00_cph1_gvServiceTypes']"
            f"//td[contains(normalize-space(),\"{nombre}\")]")
