"""
Page Object de la creación de Servicios en el WebAdmin.
Contenedor ASP.NET: ServiciosTabContainer / pnlServicioDetails.

Particularidades:
- Idioma y Tags usan TomSelect (multiselect) — se interactúa vía JS (API Tom Select).
- Los editores Quill se escriben con click + send_keys sobre el div.ql-editor.
- txtOrden NO tiene el wrapper $txtValue (es un input directo).
"""
from selenium.webdriver.common.by import By

_B  = "ctl00$cph1$ServiciosTabContainer$pnlServicioDetails$"
_ID = "ctl00_cph1_ServiciosTabContainer_pnlServicioDetails_"


class WebAdminServicioPage:

    # ── Menú lateral ─────────────────────────────────────────────────────────
    MENU_SERVICIOS = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']"
        "//a[contains(@href,'javascript:void')]"
        "//span[normalize-space()='Servicios']")
    SUBMENU_ADM_SERVICIOS = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']"
        "//a[contains(@href,'/administration/services/')]"
        "//span")

    # ── Botón crear en la lista ───────────────────────────────────────────────
    BTN_CREAR = (By.XPATH,
        "(//a[contains(@href,'Detail.aspx')] "
        "| //input[@id='btnAddNew'] "
        "| //input[@id='ctl00_cphActions_btnNew'])[1]")

    # ── Información general ───────────────────────────────────────────────────
    TXT_NAME     = (By.NAME, f"{_B}txtName$txtValue")
    DD_TYPE      = (By.NAME, f"{_B}ddlServiceType")
    DD_CITY      = (By.NAME, f"{_B}ddlCities")
    TXT_ORDEN    = (By.NAME, f"{_B}txtOrden")           # sin wrapper $txtValue
    TXT_COMMENT  = (By.NAME, f"{_B}txtComment$txtValue")
    CB_PUBLICADO = (By.ID,   f"{_ID}cbPublicado")

    # ── Emails ────────────────────────────────────────────────────────────────
    TXT_EMAIL_SERVICIO = (By.NAME, f"{_B}txtServiceEmail$txtValue")
    TXT_EMAIL_EXTRA    = (By.NAME, f"{_B}txtEmailNoti$txtValue")

    # ── Checkboxes visibles ───────────────────────────────────────────────────
    CB_VIDRIERA      = (By.ID, f"{_ID}cbWindow")
    CB_OPCIONAL_REG  = (By.ID, f"{_ID}cbOptionalRegular")
    CB_OPCIONAL_PRIV = (By.ID, f"{_ID}cbOptionalPrivate")
    CB_CANCELABLE    = (By.ID, f"{_ID}cbCancelable")

    # ── Idioma y Tags (TomSelect) — se usan los IDs para el helper JS ─────────
    LB_LANGUAGES_ID = f"{_ID}lbLanguages"
    LB_TAGS_ID      = "lbTags"   # sin prefijo ASP.NET

    # ── Edades y cancelación ──────────────────────────────────────────────────
    # ⚠ Nombres inferidos: verificar en HTML real si alguno falla (TimeoutException)
    TXT_EDAD_DESDE   = (By.NAME, f"{_B}txtAgeFrom")
    TXT_EDAD_HASTA   = (By.NAME, f"{_B}txtAgeTo")
    TXT_GRATIS_HASTA = (By.NAME, f"{_B}txtFreeAge")
    TXT_HORAS_ANTES  = (By.NAME, f"{_B}txtHorasAntes")

    # ── Quill ES (ctl00 = primer idioma = Español) ────────────────────────────
    QUILL_INTRO = (By.CSS_SELECTOR,
        f"#{_ID}ctrlShortDescriptionQuill_rptrLanguages_ctl00_txtQuill_editor .ql-editor")
    QUILL_DETALLE = (By.CSS_SELECTOR,
        f"#{_ID}ctrlLongDescriptionQuill_rptrLanguages_ctl00_txtQuill_editor .ql-editor")
    # "Nombre y Descripción": input de nombre localizado + editor Quill
    QUILL_NAMEDESC_NOMBRE = (By.NAME,
        f"{_B}ctrlNameDescQuill$rptrLanguages$ctl00$txtName")
    QUILL_NAMEDESC_DESC = (By.CSS_SELECTOR,
        f"#{_ID}ctrlNameDescQuill_rptrLanguages_ctl00_txtQuill_editor .ql-editor")
    QUILL_POLITICA = (By.CSS_SELECTOR,
        f"#{_ID}ctrlCancelationQuill_rptrLanguages_ctl00_txtQuill_editor .ql-editor")
    QUILL_ENCUENTRO = (By.CSS_SELECTOR,
        f"#{_ID}ctrlMeetingPointQuill_rptrLanguages_ctl00_txtQuill_editor .ql-editor")
    QUILL_DESTINO = (By.CSS_SELECTOR,
        f"#{_ID}ctrlDestinationPointQuill_rptrLanguages_ctl00_txtQuill_editor .ql-editor")

    # ── Guardar ───────────────────────────────────────────────────────────────
    BTN_GUARDAR = (By.XPATH,
        "(//input[@value='Guardar'] | //button[@value='Guardar'])[1]")

    # ── Tabla de la lista ─────────────────────────────────────────────────────
    TABLA = (By.CSS_SELECTOR, "table.tablestyle")

    @staticmethod
    def fila_por_nombre(nombre):
        return (By.XPATH,
            f"//table[contains(@class,'tablestyle')]"
            f"//td[contains(normalize-space(),\"{nombre}\")]")
