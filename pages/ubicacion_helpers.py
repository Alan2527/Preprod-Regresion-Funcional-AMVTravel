"""
Helpers compartidos por los tests de Ubicación (Regiones, Ciudades, Barrios,
Destinos, Restaurantes). Mismo espíritu que `pages/cotizacion_helpers.py`.
"""
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC


def seleccionar(driver, wait, locator, texto=None, postback=False):
    """Selecciona una opción de un <select>.

    - Si `texto` se pasa, elige la primera opción que lo contenga (case-insensitive).
    - Si no matchea (o no se pasa), elige la primera opción REAL (índice 1 si hay
      placeholder en el índice 0, si no el 0).
    - Si `postback=True`, espera al postback del control dependiente.
    Devuelve el texto elegido.
    """
    el = wait.until(EC.presence_of_element_located(locator))
    sel = Select(el)
    elegido = None
    if texto:
        for o in sel.options:
            if texto.lower() in (o.text or "").strip().lower():
                sel.select_by_visible_text(o.text)
                elegido = o.text
                break
    if elegido is None:
        idx = 1 if len(sel.options) > 1 else 0
        sel.select_by_index(idx)
        elegido = sel.options[idx].text
    if postback:
        time.sleep(1.5)  # esperar el postback del dependiente (ciudad→hotel, etc.)
    return elegido
