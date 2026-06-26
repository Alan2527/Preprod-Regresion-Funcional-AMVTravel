"""Page Object de Cotizaciones → Individuales (budgets/budgetsingle.aspx, mainTabContainer)."""
from selenium.webdriver.common.by import By

_B = "ctl00$cph1$mainTabContainer$pnlDetails$"


class WebAdminCotizacionIndividualPage:
    MENU_COTIZACIONES = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'javascript:void')]"
        "//span[normalize-space()='Cotizaciones']")
    SUBMENU_INDIVIDUALES = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'/administration/budgets/defaultsingle.aspx')]"
        "//span[normalize-space()='Individuales']")

    BTN_NUEVO = (By.ID, "btnCreate")   # → budgetsingle.aspx

    # Formulario (Detalle de la cotización)
    TXT_REFERENCE = (By.NAME, f"{_B}txtReference$txtValue")
    TXT_TITLE     = (By.NAME, f"{_B}txtTitle$txtValue")
    DD_AGENCY     = (By.NAME, f"{_B}ddAgency")
    DD_LANG       = (By.NAME, f"{_B}ddLang")
    DD_ITINERARY  = (By.NAME, f"{_B}ddItinerary")
    FECHA_RECORD  = (By.NAME, f"{_B}ctrlReminderDate$txtDateTime")
    CHK_PRESENTACION = (By.ID, "ctl00_cph1_mainTabContainer_pnlDetails_chkShowPresentation")
    CB_PUBLICADO  = (By.ID,   "ctl00_cph1_mainTabContainer_pnlDetails_cbPublished")
    BTN_GUARDAR   = (By.NAME, f"{_B}btnSave")

    # Botón Preview (abre una pestaña nueva con previewmailingsingle.aspx)
    BTN_PREVIEW = (By.XPATH, "//a[@title='Preview' and contains(@href,'previewmailing')]")

    TAB_CONTAINER = "ctl00_cph1_mainTabContainer"
    SOLAPAS = ["Detalle", "Destinos", "Hoteles", "Restaurantes", "Cruceros"]

    # Landmarks estables del preview esperado (del itinerario "Argentina de Sur a Norte").
    PREVIEW_LANDMARKS = [
        "glaciar Perito Moreno",
        "Multiviajes Argentina SRL",
        "Precio neto del paquete por persona",
    ]

    TXT_SEARCH = (By.NAME, "ctl00$cph1$txtSearch")
    BTN_SEARCH = (By.NAME, "ctl00$cph1$btnSearch")
    TABLA = (By.ID, "ctl00_cph1_gvData")

    @staticmethod
    def fila_por_nombre(nombre):
        return (By.XPATH,
            f"//table[@id='ctl00_cph1_gvData']//td[contains(normalize-space(),\"{nombre}\")]")
