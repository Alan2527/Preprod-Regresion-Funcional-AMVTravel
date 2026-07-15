"""
Page Object de Adm. de puntos en el WebAdmin
(Contenidos → Adm. de puntos, loyaltypoints/default.aspx).

La pantalla es un TabContainer (CustomerTabContainer) con 3 solapas:
- Productos (pnlProductSetting): alta/baja de reglas de puntos por producto/ciudad.
- Agencias  (pnlAgencySetting): alta/baja de agencias habilitadas al programa.
- Configuración (TabPanel1): multiplicador, toggles y grilla de categorías.

Las altas se hacen con "+ Agregar" (postback que suma la fila al grid). Las bajas son
por fila (link Borrar/Eliminar) con un popup de confirmación Sí/No.

Selectores confirmados contra el DOM real (qa.amv.travel).
"""
from selenium.webdriver.common.by import By

_AG = "ctl00_cph1_CustomerTabContainer_pnlAgencySetting_ctrlAgencySettingControl_"
_AGN = "ctl00$cph1$CustomerTabContainer$pnlAgencySetting$ctrlAgencySettingControl$"
_PR = "ctl00_cph1_CustomerTabContainer_pnlProductSetting_ctrlProductSettingControl_"
_PRN = "ctl00$cph1$CustomerTabContainer$pnlProductSetting$ctrlProductSettingControl$"
_CFG = "ctl00_cph1_CustomerTabContainer_TabPanel1_"


class WebAdminLoyaltyPointsPage:

    # ── Menú lateral: Contenidos → Adm. de puntos ─────────────────────────────
    MENU_CONTENIDOS = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'javascript:void')]"
        "//span[normalize-space()='Contenidos']")
    SUBMENU = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'/administration/loyaltypoints/default.aspx')]"
        "//span[normalize-space()='Adm. de puntos']")
    URL = "/administration/loyaltypoints/default.aspx"

    # ── Headers de las solapas (AjaxControlToolkit TabContainer) ──────────────
    TAB_PRODUCTOS = (By.ID, "__tab_ctl00_cph1_CustomerTabContainer_pnlProductSetting")
    TAB_AGENCIAS = (By.ID, "__tab_ctl00_cph1_CustomerTabContainer_pnlAgencySetting")
    TAB_CONFIG = (By.ID, "__tab_ctl00_cph1_CustomerTabContainer_TabPanel1")

    # ── Solapa Agencias ───────────────────────────────────────────────────────
    AG_DD_PAIS = (By.NAME, f"{_AGN}ddlCountry")
    AG_DD_AGENCIA = (By.NAME, f"{_AGN}ddlAgency")
    AG_TXT_OVER = (By.NAME, f"{_AGN}txtOver")
    AG_CB_EXCLUDE = (By.ID, f"{_AG}cbExclude")
    AG_BTN_AGREGAR = (By.ID, f"{_AG}btnAddAgencySetting")
    AG_GRID = (By.ID, f"{_AG}gvAgencySetting")
    AG_CONFIRM_SI = (By.ID, f"{_AG}cbDelete_btnYES")

    @staticmethod
    def ag_filas_agencia():
        # Columna "Agencia" (2ª) de las filas de datos del grid de agencias.
        return (By.XPATH,
            f"//table[@id='{_AG}gvAgencySetting']"
            f"//tr[contains(@class,'rowstyle') or contains(@class,'altrowstyle')]/td[2]")

    @staticmethod
    def ag_borrar_por_agencia(nombre):
        return (By.XPATH,
            f"//table[@id='{_AG}gvAgencySetting']"
            f"//tr[td[contains(normalize-space(),\"{nombre}\")]]//a[contains(@id,'btnDelete')]")

    @staticmethod
    def ag_celda_agencia(nombre):
        return (By.XPATH,
            f"//table[@id='{_AG}gvAgencySetting']//td[contains(normalize-space(),\"{nombre}\")]")

    # ── Solapa Productos ──────────────────────────────────────────────────────
    PR_DD_WILDCARD = (By.NAME, f"{_PRN}ddProductWildcard")
    PR_DD_PAIS = (By.NAME, f"{_PRN}ddCountry")
    PR_DD_CITY = (By.NAME, f"{_PRN}ddCity")
    PR_DD_PRODUCT = (By.NAME, f"{_PRN}ddProduct")
    PR_CB_EXCLUDE = (By.ID, f"{_PR}cbExclude")
    PR_TXT_MARKUP = (By.NAME, f"{_PRN}txtMarkup$txtValue")
    PR_BTN_AGREGAR = (By.ID, f"{_PR}btnAddProductSetting")
    PR_GRID = (By.ID, f"{_PR}gvProductsSetting")
    PR_CONFIRM_SI = (By.ID, f"{_PR}cbDelete_btnYES")

    @staticmethod
    def pr_filas_ciudad():
        # Columna "Ciudad" (2ª) de las filas de datos del grid de productos.
        return (By.XPATH,
            f"//table[@id='{_PR}gvProductsSetting']"
            f"//tr[contains(@class,'rowstyle') or contains(@class,'altrowstyle')]/td[2]")

    @staticmethod
    def pr_borrar_por_ciudad(ciudad):
        return (By.XPATH,
            f"//table[@id='{_PR}gvProductsSetting']"
            f"//tr[td[contains(normalize-space(),\"{ciudad}\")]]//a[contains(@id,'lnkDelete')]")

    @staticmethod
    def pr_celda_ciudad(ciudad):
        return (By.XPATH,
            f"//table[@id='{_PR}gvProductsSetting']//td[contains(normalize-space(),\"{ciudad}\")]")

    # ── Solapa Configuración ──────────────────────────────────────────────────
    CFG_CB_ENABLED = (By.ID, f"{_CFG}cbEnabled")
    CFG_MULTIPLIER = (By.ID, f"{_CFG}txtlblPointMultiplier_txtValue")
    CFG_CB_USER = (By.ID, f"{_CFG}cbUserPointsEnabled")
    CFG_TXT_USER = (By.ID, f"{_CFG}txtUserPointsPercentage")
    CFG_CB_NONONLINE = (By.ID, f"{_CFG}cbNonOnlineEnabled")
    CFG_TXT_NONONLINE = (By.ID, f"{_CFG}txtNonOnlinePercentage")
    CFG_GRID_CATEGORIES = (By.ID, f"{_CFG}gvCategories")
    CFG_CATEGORIES_HEADERS = (By.CSS_SELECTOR, f"#{_CFG}gvCategories th")
    CFG_CATEGORIES_FILAS = (By.CSS_SELECTOR,
        f"#{_CFG}gvCategories tr.rowstyle, #{_CFG}gvCategories tr.altrowstyle")
    CFG_COLUMNAS_CATEGORIES = ["ID", "Nombre", "Descripción", "Porcentaje de acumulación", "Editar"]
