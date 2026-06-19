"""Page Object de Tipos de Usuario (Agencias) — usertypes.aspx, lista INLINE (gvUserTypes)."""
from selenium.webdriver.common.by import By


class WebAdminTipoUsuarioPage:
    MENU_AGENCIAS = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'javascript:void')]"
        "//span[normalize-space()='Agencias']")
    SUBMENU_TIPOS_USUARIO = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'/administration/types/usertypes.aspx')]")

    BTN_NUEVO    = (By.NAME, "ctl00$cphActions$btnNew")
    TXT_NAME     = (By.NAME, "ctl00$cph1$txtName$txtValue")
    TXT_DETAIL   = (By.NAME, "ctl00$cph1$txtDetail$txtValue")
    CB_PUBLICADO = (By.ID,   "ctl00_cph1_cbPublicado")
    BTN_GUARDAR  = (By.NAME, "ctl00$cph1$btnSave")

    TXT_SEARCH = (By.NAME, "ctl00$cph1$txtSearch")
    BTN_SEARCH = (By.NAME, "ctl00$cph1$btnSearch")
    TABLA = (By.ID, "ctl00_cph1_gvUserTypes")

    @staticmethod
    def fila_por_nombre(nombre):
        return (By.XPATH,
            f"//table[@id='ctl00_cph1_gvUserTypes']//td[contains(normalize-space(),\"{nombre}\")]")
