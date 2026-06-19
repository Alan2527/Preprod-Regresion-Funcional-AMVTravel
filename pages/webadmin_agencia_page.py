"""Page Object de Adm. de Agencias — agencies/detail.aspx (AgencyTabContainer).
⚠ Flujo de 2 pasos: se guarda la agencia (btnSavePopUp) → aparece un MODAL preguntando si
se crea el usuario admin → "Sí" → redirige a un form de Usuario (CustomerTabContainer, ver
WebAdminUsuarioPage). El modal de confirmación NO estaba en el HTML capturado: el botón "Sí"
se busca por texto (best-effort)."""
from selenium.webdriver.common.by import By

_B = "ctl00$cph1$AgencyTabContainer$pnlDetails$"
_ID = "ctl00_cph1_AgencyTabContainer_pnlDetails_"


class WebAdminAgenciaPage:
    MENU_AGENCIAS = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'javascript:void')]"
        "//span[normalize-space()='Agencias']")
    SUBMENU_ADM_AGENCIAS = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[@href='/administration/agencies/']")

    BTN_NUEVO = (By.ID, "btnAddNew")   # → detail.aspx

    TXT_NAME    = (By.NAME, f"{_B}txtName$txtValue")
    TXT_TABNAME = (By.NAME, f"{_B}txtTabName$txtValue")   # Nombre del Tab de Oportunidades
    TXT_ADDRESS = (By.NAME, f"{_B}txtAddress$txtValue")
    TXT_EMAIL   = (By.NAME, f"{_B}txtEmail$txtValue")
    TXT_PHONE   = (By.NAME, f"{_B}txtPhone$txtValue")
    TXT_COMMENT = (By.NAME, f"{_B}txtComment$txtValue")
    DD_VENDOR   = (By.NAME, f"{_B}ddVendor")
    DD_MARKET   = (By.NAME, f"{_B}ddMarket")
    DD_CITIES   = (By.NAME, f"{_B}ddlCities")
    CB_PUBLICADO = (By.ID,  f"{_ID}cbPublicado")
    QUILL_ES = (By.CSS_SELECTOR,
        f"#{_ID}ctrlDescriptionQuill_rptrLanguages_ctl00_txtQuill_editor .ql-editor")
    BTN_GUARDAR = (By.NAME, f"{_B}btnSavePopUp")

    # Modal "¿Crear usuario admin?" tras guardar (best-effort por texto).
    MODAL_SI = (By.XPATH,
        "//*[(self::a or self::button or self::input)]"
        "[normalize-space(.)='Sí' or normalize-space(.)='Si' or @value='Sí' or @value='Si']")

    TXT_SEARCH = (By.NAME, "ctl00$cph1$txtSearch")
    BTN_SEARCH = (By.NAME, "ctl00$cph1$btnFilter")   # la lista usa btnFilter (no btnSearch)
    TABLA = (By.ID, "ctl00_cph1_gvAgencies")

    @staticmethod
    def fila_por_nombre(nombre):
        return (By.XPATH,
            f"//table[@id='ctl00_cph1_gvAgencies']//td[contains(normalize-space(),\"{nombre}\")]")
