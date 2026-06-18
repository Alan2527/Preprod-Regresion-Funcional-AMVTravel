"""
Page Object de la creación de Características en el WebAdmin (charasteristicsadmin.aspx).

Form INLINE (se despliega bajo la tabla al tocar "Nuevo"). Particularidad: tanto el
Nombre como el Detalle son MULTI-IDIOMA (4 idiomas cada uno):
- Nombre  → lvNameTranslations$ctrl0..3$txtName$txtValue  (inputs)
- Detalle → lvDetailTranslations$ctrl0..3$txtDetail$txtValue (textareas)
ctrl0=Español, ctrl1=English, ctrl2=Portuguese, ctrl3=Italian.

Selectores confirmados contra el HTML real (preprod.amv.travel).
"""
from selenium.webdriver.common.by import By


class WebAdminCaracteristicaPage:

    # ── Menú lateral: Servicios (acordeón) → Caracteristicas ──────────────────
    MENU_SERVICIOS = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']"
        "//a[contains(@href,'javascript:void')]"
        "//span[normalize-space()='Servicios']")
    SUBMENU_CARACTERISTICAS = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']"
        "//a[contains(@href,'/administration/services/charasteristicsadmin.aspx')]"
        "//span[normalize-space()='Caracteristicas']")

    # ── Botón "Nuevo" (submit → despliega el form inline) ─────────────────────
    BTN_NUEVO = (By.NAME, "ctl00$cphActions$btnNew")

    # ── Formulario ────────────────────────────────────────────────────────────
    TXT_ORDEN    = (By.NAME, "ctl00$cph1$txtOrden$txtValue")
    CB_PUBLICADO = (By.ID, "ctl00_cph1_cbPublicado")

    # Nombre por idioma (input) y Detalle por idioma (textarea).
    @staticmethod
    def nombre(indice):
        return (By.NAME, f"ctl00$cph1$lvNameTranslations$ctrl{indice}$txtName$txtValue")

    @staticmethod
    def detalle(indice):
        return (By.NAME, f"ctl00$cph1$lvDetailTranslations$ctrl{indice}$txtDetail$txtValue")

    # ── Guardar ───────────────────────────────────────────────────────────────
    BTN_GUARDAR = (By.NAME, "ctl00$cph1$btnSave")

    # ── Buscador de la lista ──────────────────────────────────────────────────
    TXT_SEARCH = (By.ID, "ctl00_cph1_txtSearch")
    BTN_SEARCH = (By.ID, "ctl00_cph1_btnSearch")

    # ── Tabla de la lista ─────────────────────────────────────────────────────
    TABLA = (By.ID, "ctl00_cph1_gvCharasteristics")

    @staticmethod
    def fila_por_nombre(nombre):
        return (By.XPATH,
            f"//table[@id='ctl00_cph1_gvCharasteristics']"
            f"//td[contains(normalize-space(),\"{nombre}\")]")
