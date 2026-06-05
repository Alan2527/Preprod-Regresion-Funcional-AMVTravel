"""
Helpers reutilizables para los tests de Selenium.

Centraliza las funciones robustas de interacción (click / escritura) que antes
estaban copiadas en varios archivos de test. Importar desde cualquier test:

    from helpers import safe_click, safe_send_keys, wait_table_rows
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    StaleElementReferenceException,
    ElementNotInteractableException,
)


def safe_click(wait, locator, retries=5):
    """Click resistente a elementos 'stale' (reintenta hasta `retries` veces)."""
    for _ in range(retries):
        try:
            elem = wait.until(EC.element_to_be_clickable(locator))
            elem.click()
            return
        except StaleElementReferenceException:
            time.sleep(1)
    raise Exception(f"No se pudo hacer click: {locator}")


def safe_send_keys(wait, locator, value, retries=5):
    """Escritura robusta: hace scroll, limpia y escribe; con fallback a JS nativo."""
    for _ in range(retries):
        try:
            elem = wait.until(EC.visibility_of_element_located(locator))
            wait._driver.execute_script("arguments[0].scrollIntoView(true);", elem)
            time.sleep(0.5)
            elem.clear()
            elem.send_keys(value)
            return
        except (StaleElementReferenceException, ElementNotInteractableException):
            try:
                # Fallback: asignar el valor por JavaScript si el campo se bloquea.
                elem = wait.until(EC.presence_of_element_located(locator))
                wait._driver.execute_script("arguments[0].value = arguments[1];", elem, value)
                return
            except Exception:
                time.sleep(1)
    raise Exception(f"No se pudo escribir en: {locator}")


def wait_table_rows(wait, table_id):
    """Espera a que una tabla tenga al menos una fila en su <tbody>."""
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f"{table_id} tbody tr")))
