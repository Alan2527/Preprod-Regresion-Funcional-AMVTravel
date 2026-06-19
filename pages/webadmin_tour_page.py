"""
Page Object COMPARTIDO de los "Receptive Tours" del WebAdmin: Paquetes, Oportunidades
y Travel Sale comparten la MISMA estructura (grid gvReceptiveTours + form TourTabContainer),
sólo cambia la URL/submenú y qué solapas (tabs) hay.

Lista: receptivetours/ · opportunities/ · travelsale/  →  detail.aspx (form con solapas).
Selectores confirmados contra el HTML real (preprod.amv.travel).
"""
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from helpers import safe_click, safe_send_keys

_B = "ctl00$cph1$TourTabContainer$pnlDetails$"
_ID = "ctl00_cph1_TourTabContainer_pnlDetails_"


class WebAdminTourPage:

    # ── Menú lateral: Circuitos (acordeón) → submenús ─────────────────────────
    MENU_CIRCUITOS = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'javascript:void')]"
        "//span[normalize-space()='Circuitos']")
    SUBMENU_PAQUETES = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'/administration/receptivetours/')]"
        "//span[normalize-space()='Paquetes']")
    SUBMENU_OPORTUNIDADES = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'/administration/opportunities/')]"
        "//span[normalize-space()='Oportunidades']")
    SUBMENU_TRAVELSALE = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'/administration/travelsale/')]"
        "//span[normalize-space()='Travel Sale']")

    # ── Botón "Crear" de la lista (navega a detail.aspx) ──────────────────────
    BTN_NUEVO = (By.ID, "btnAddNew")

    # ── Formulario (TourTabContainer / pnlDetails) ────────────────────────────
    TXT_NAME       = (By.NAME, f"{_B}txtName$txtValue")
    FECHA_DESDE    = (By.NAME, f"{_B}ctrlFrom$txtDateTime")
    FECHA_HASTA    = (By.NAME, f"{_B}ctrlTo$txtDateTime")
    DD_CURRENCY    = (By.NAME, f"{_B}ddlCurrency")
    TXT_MARKUP     = (By.NAME, f"{_B}txtMarkup$txtValue")
    TXT_TOTAL_RATE = (By.NAME, f"{_B}txtTotalRate$txtValue")
    TXT_EXTRA_RATE = (By.NAME, f"{_B}txtExtraRate$txtValue")
    TXT_RATE_MIN   = (By.NAME, f"{_B}txtRateMin$txtValue")
    TXT_NIGHTS     = (By.NAME, f"{_B}txtNights$txtValue")
    DD_TYPE        = (By.NAME, f"{_B}ddType")
    TXT_ORDEN      = (By.NAME, f"{_B}txtOrden$txtValue")
    CB_PUBLICADO   = (By.ID,   f"{_ID}cbPublicado")
    CB_DESTACADO   = (By.ID,   f"{_ID}cbGreat")
    NOMBRE_DESC_ES = (By.NAME, f"{_B}ctrlNameDescQuill$rptrLanguages$ctl00$txtName")
    QUILL_ES = (By.CSS_SELECTOR,
        f"#{_ID}ctrlNameDescQuill_rptrLanguages_ctl00_txtQuill_editor .ql-editor")
    BTN_GUARDAR = (By.NAME, f"{_B}SaveButton")

    # ── Solapas (tabs) — id del <span> de cada solapa ─────────────────────────
    SOLAPAS = {
        "Detalle":  "ctl00_cph1_TourTabContainer_pnlDetails_tab",
        "Imagenes": "ctl00_cph1_TourTabContainer_pnlImagenes_tab",
        "Videos":   "ctl00_cph1_TourTabContainer_pnlVideos_tab",
        "Destinos": "ctl00_cph1_TourTabContainer_pnlDestinations_tab",
        "Agencias": "ctl00_cph1_TourTabContainer_pnlAgencies_tab",
    }
    TAB_CONTAINER = "TourTabContainer"

    # ── Lista (grid + buscador) ───────────────────────────────────────────────
    TXT_SEARCH = (By.NAME, "ctl00$cph1$txtSearch")
    BTN_SEARCH = (By.NAME, "ctl00$cph1$btnSearch")
    TABLA = (By.ID, "ctl00_cph1_gvReceptiveTours")

    @staticmethod
    def fila_por_nombre(nombre):
        return (By.XPATH,
            f"//table[@id='ctl00_cph1_gvReceptiveTours']"
            f"//td[contains(normalize-space(),\"{nombre}\")]")


def escribir_quill(driver, wait, locator, texto):
    """Escribe en un editor Quill (div.ql-editor contenteditable)."""
    editor = wait.until(EC.visibility_of_element_located(locator))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", editor)
    editor.click()
    editor.send_keys(texto)


def _set_fecha(driver, wait, locator, valor):
    """Setea una fecha en un input flatpickr (js-datepicker) por JS + change."""
    el = wait.until(EC.presence_of_element_located(locator))
    driver.execute_script(
        "arguments[0].value=arguments[1];"
        "arguments[0].dispatchEvent(new Event('input',{bubbles:true}));"
        "arguments[0].dispatchEvent(new Event('change',{bubbles:true}));",
        el, valor)


def _presente(driver, locator):
    """Devuelve el primer elemento del locator si existe en el DOM, o None."""
    els = driver.find_elements(*locator)
    return els[0] if els else None


def llenar_tour(driver, wait, nombre, texto_quill, fecha_desde, fecha_hasta):
    """Llena el form Detalle del Tour. Es ADAPTABLE: Paquete/Oportunidad/TravelSale
    comparten TourTabContainer pero NO tienen los mismos campos (ej.: TravelSale no
    tiene tarifas ni Tipo; Oportunidad no tiene Tipo). Sólo se llena lo que existe."""
    P = WebAdminTourPage
    safe_send_keys(wait, P.TXT_NAME, nombre)
    if _presente(driver, P.FECHA_DESDE):
        _set_fecha(driver, wait, P.FECHA_DESDE, fecha_desde)
    if _presente(driver, P.FECHA_HASTA):
        _set_fecha(driver, wait, P.FECHA_HASTA, fecha_hasta)
    if _presente(driver, P.DD_CURRENCY):
        Select(driver.find_element(*P.DD_CURRENCY)).select_by_visible_text("Dollar")
    # Tarifas (sólo Paquete/Oportunidad).
    for loc, val in ((P.TXT_MARKUP, "100"), (P.TXT_TOTAL_RATE, "100"),
                     (P.TXT_EXTRA_RATE, "0"), (P.TXT_RATE_MIN, "0")):
        if _presente(driver, loc):
            safe_send_keys(wait, loc, val)
    safe_send_keys(wait, P.TXT_NIGHTS, "3")   # presente en los 3
    if _presente(driver, P.DD_TYPE):          # sólo Paquete
        Select(driver.find_element(*P.DD_TYPE)).select_by_visible_text("VIP")
    safe_send_keys(wait, P.TXT_ORDEN, "1")    # presente en los 3
    for loc in (P.CB_PUBLICADO, P.CB_DESTACADO):
        cb = _presente(driver, loc)
        if cb and not cb.is_selected():
            driver.execute_script("arguments[0].click();", cb)
    safe_send_keys(wait, P.NOMBRE_DESC_ES, nombre)
    escribir_quill(driver, wait, P.QUILL_ES, texto_quill)


def validar_solapas(driver, container_id, nombres, solapas_map):
    """Valida que cada solapa ESPERADA exista y NO esté deshabilitada.
    (No exige 0 deshabilitadas en todo el contenedor: otras solapas como Hoteles/
    Servicios quedan deshabilitadas legítimamente hasta cargar más datos.)"""
    for nombre in nombres:
        tab_id = solapas_map[nombre]
        el = driver.find_elements(By.ID, tab_id)
        assert el, f"No existe la solapa '{nombre}' ({tab_id})"
        # La clase 'ajax__tab_disabled' la pone ACT en algún ancestro del <span> de la solapa.
        deshabilitada = driver.execute_script(
            "var e=arguments[0];"
            "while(e && e!==document.body){"
            "  if(e.classList && e.classList.contains('ajax__tab_disabled')) return true;"
            "  e=e.parentElement;"
            "} return false;", el[0])
        assert not deshabilitada, f"La solapa '{nombre}' está deshabilitada"
