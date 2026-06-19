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


def llenar_tour(driver, wait, nombre, texto_quill, fecha_desde, fecha_hasta):
    """Llena el form Detalle del Tour (campos requeridos + Nombre y Descripción ES)."""
    P = WebAdminTourPage
    safe_send_keys(wait, P.TXT_NAME, nombre)
    _set_fecha(driver, wait, P.FECHA_DESDE, fecha_desde)
    _set_fecha(driver, wait, P.FECHA_HASTA, fecha_hasta)
    Select(wait.until(EC.element_to_be_clickable(P.DD_CURRENCY))).select_by_visible_text("Dollar")
    safe_send_keys(wait, P.TXT_MARKUP, "100")
    safe_send_keys(wait, P.TXT_TOTAL_RATE, "100")
    safe_send_keys(wait, P.TXT_EXTRA_RATE, "0")
    safe_send_keys(wait, P.TXT_RATE_MIN, "0")
    safe_send_keys(wait, P.TXT_NIGHTS, "3")
    Select(wait.until(EC.element_to_be_clickable(P.DD_TYPE))).select_by_visible_text("VIP")
    safe_send_keys(wait, P.TXT_ORDEN, "1")
    for loc in (P.CB_PUBLICADO, P.CB_DESTACADO):
        cb = wait.until(EC.presence_of_element_located(loc))
        if not cb.is_selected():
            driver.execute_script("arguments[0].click();", cb)
    safe_send_keys(wait, P.NOMBRE_DESC_ES, nombre)
    escribir_quill(driver, wait, P.QUILL_ES, texto_quill)


def validar_solapas(driver, container_id, nombres, solapas_map):
    """Valida que cada solapa esperada exista y que NINGUNA esté deshabilitada."""
    for nombre in nombres:
        tab_id = solapas_map[nombre]
        assert driver.find_elements(By.ID, tab_id), f"No existe la solapa '{nombre}' ({tab_id})"
    disabled = driver.find_elements(
        By.CSS_SELECTOR, f"[id*='{container_id}'] .ajax__tab_disabled")
    assert not disabled, f"Hay {len(disabled)} solapa(s) deshabilitada(s) en {container_id}"
