"""Page Object de Cotizaciones → Grupos (budgets/budgetdetail.aspx, mainTabContainer)."""
from selenium.webdriver.common.by import By

_B = "ctl00$cph1$mainTabContainer$pnlDetails$"


class WebAdminCotizacionGrupoPage:
    MENU_COTIZACIONES = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'javascript:void')]"
        "//span[normalize-space()='Cotizaciones']")
    SUBMENU_GRUPOS = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'/administration/budgets/default.aspx')]"
        "//span[normalize-space()='Grupos']")

    BTN_NUEVO = (By.ID, "btnCreate")   # → budgetdetail.aspx

    # Formulario (Detalle de la cotización)
    DD_BRANCH      = (By.NAME, f"{_B}ddBranch")        # Sucursal (requerido)
    FECHA_INICIO   = (By.NAME, f"{_B}ctrlInDate$txtDateTime")
    FECHA_RECORD   = (By.NAME, f"{_B}ctrlReminderDate$txtDateTime")
    CB_PUBLICADO   = (By.ID,   "ctl00_cph1_mainTabContainer_pnlDetails_cbPublished")
    TXT_REFERENCE  = (By.NAME, f"{_B}txtReference$txtValue")
    TXT_TITLE      = (By.NAME, f"{_B}txtTitle$txtValue")
    DD_LANG        = (By.NAME, f"{_B}ddLang")
    DD_ITINERARY   = (By.NAME, f"{_B}ddItinerary")
    DD_AGENCY      = (By.NAME, f"{_B}ddAgency")
    DD_EXECUTIVE   = (By.NAME, f"{_B}ddAccountExecutive")
    TXT_MARKUP     = (By.NAME, f"{_B}txtMarkup$txtValue")
    TXT_EXCHANGE   = (By.NAME, f"{_B}txtExchangeRate$txtValue")
    TXT_PAX        = (By.NAME, f"{_B}txtPaxCountBudget$txtValue")
    TXT_SGL        = (By.NAME, f"{_B}txtBudgetSGL$txtValue")
    TXT_DBL        = (By.NAME, f"{_B}txtBudgetDBL$txtValue")
    TXT_TPL        = (By.NAME, f"{_B}txtBudgetTPL$txtValue")
    TXT_OBSERVATION = (By.NAME, f"{_B}txtObservation")
    BTN_GUARDAR    = (By.NAME, f"{_B}btnSave")

    TAB_CONTAINER = "ctl00_cph1_mainTabContainer"
    SOLAPAS = ["Detalle", "Configuraci", "Destinos", "Hoteles",
               "Restaurantes", "Salones", "Gifts", "Archivos"]

    TXT_SEARCH = (By.NAME, "ctl00$cph1$txtSearch")
    BTN_SEARCH = (By.NAME, "ctl00$cph1$btnSearch")
    TABLA = (By.ID, "ctl00_cph1_gvData")

    @staticmethod
    def fila_por_nombre(nombre):
        return (By.XPATH,
            f"//table[@id='ctl00_cph1_gvData']//td[contains(normalize-space(),\"{nombre}\")]")
