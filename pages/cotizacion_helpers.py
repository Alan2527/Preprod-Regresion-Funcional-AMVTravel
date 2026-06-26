"""Helpers compartidos para los tests de Cotizaciones (Grupos / Individuales)."""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC


def sel_primera(driver, locator):
    """Selecciona la primera opción real de un <select>, salteando placeholders
    ('' / -1 / -5 / 0). Captura el texto ANTES de seleccionar (el onchange puede
    disparar un postback que deja stale la opción). Selenium ya dispara el change."""
    els = driver.find_elements(*locator)
    if not els:
        return None
    sel = Select(els[0])
    for o in sel.options:
        v = o.get_attribute("value")
        if v and v not in ("-1", "-5", "0"):
            txt = o.text
            sel.select_by_value(v)
            return txt
    return None


def sel_texto(driver, locator, texto):
    """Selecciona por texto que CONTENGA `texto`; si no, cae a la primera real."""
    els = driver.find_elements(*locator)
    if not els:
        return None
    sel = Select(els[0])
    for o in sel.options:
        v = o.get_attribute("value")
        if texto.lower() in (o.text or "").lower() and v not in ("", "-1", "-5", "0"):
            txt = o.text
            sel.select_by_value(v)
            return txt
    return sel_primera(driver, locator)


def set_fecha(driver, locator, valor):
    """Setea una fecha en un input flatpickr (js-datepicker) por JS + change."""
    els = driver.find_elements(*locator)
    if els:
        driver.execute_script(
            "arguments[0].value=arguments[1];"
            "arguments[0].dispatchEvent(new Event('input',{bubbles:true}));"
            "arguments[0].dispatchEvent(new Event('change',{bubbles:true}));", els[0], valor)


def validar_solapas(driver, container_id, keywords):
    """Valida que cada solapa (AjaxControlToolkit TabContainer) cuyo header CONTENGA el
    keyword exista y NO esté deshabilitada. Las solapas se identifican por el texto del
    header (sólo la primera solapa tiene id 'pnl..._tab' en el HTML)."""
    for kw in keywords:
        xp = (f"//div[@id='{container_id}_header']"
              f"//a[contains(@class,'ajax__tab_tab')][contains(normalize-space(.),\"{kw}\")]")
        els = driver.find_elements(By.XPATH, xp)
        assert els, f"No existe la solapa que contiene '{kw}'"
        deshabilitada = driver.execute_script(
            "var e=arguments[0];"
            "while(e && e!==document.body){"
            "  if(e.classList && e.classList.contains('ajax__tab_disabled')) return true;"
            "  e=e.parentElement;"
            "} return false;", els[0])
        assert not deshabilitada, f"La solapa '{kw}' está deshabilitada/bloqueada"
