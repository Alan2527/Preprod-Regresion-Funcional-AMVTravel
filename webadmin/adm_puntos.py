"""
Tests de Contenidos → Adm. de puntos (loyaltypoints/default.aspx), 3 solapas:

1. Agencias    → agrega una agencia random, confirma que se guardó y la BORRA (cleanup).
2. Productos   → agrega una regla de producto random (por ciudad), confirma y la BORRA.
3. Configuración → solo valida que estén todos los controles/columnas que deben estar.

Las bajas dejan la pantalla como estaba (el test crea su propio dato y lo elimina).
⚠ Best-effort: los combos dependientes (país→agencia, país→ciudad) y el popup de
confirmación pueden requerir ajuste tras la primera corrida en CI.
"""
import time
import allure
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from helpers import safe_click, safe_send_keys
from pages.ubicacion_helpers import seleccionar
from pages.webadmin_loyaltypoints_page import WebAdminLoyaltyPointsPage as P


def _ir_a_puntos(wait):
    safe_click(wait, P.MENU_CONTENIDOS)
    time.sleep(1)
    safe_click(wait, P.SUBMENU)
    wait.until(EC.url_contains(P.URL))


def _opciones_reales(select_el):
    """Opciones con value distinto de '' y '0' (descarta placeholders)."""
    return [o for o in Select(select_el).options
            if (o.get_attribute("value") or "") not in ("", "0") and o.text.strip()]


# ──────────────────────────────────────────────────────────────────────────────
# SOLAPA 1 — AGENCIAS: alta + baja
# ──────────────────────────────────────────────────────────────────────────────
@allure.feature("WebAdmin AMV Travel")
@allure.story("Adm. de puntos · Agencias: alta de agencia + baja (cleanup)")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("""
Agrega una agencia random (que no esté ya en la grilla) al programa de puntos, valida
que se guardó (aparece en gvAgencySetting) y luego la elimina para dejar todo como estaba.
""")
def test_puntos_agencias(login_webadmin):
    driver = login_webadmin
    wait = WebDriverWait(driver, 45)

    with allure.step("1. Ir a Adm. de puntos → solapa Agencias"):
        _ir_a_puntos(wait)
        safe_click(wait, P.TAB_AGENCIAS)
        time.sleep(1)

    with allure.step("2. Elegir una agencia random que no esté en la grilla"):
        existentes = {e.get_attribute("textContent").strip()
                      for e in driver.find_elements(*P.ag_filas_agencia())}
        reales = _opciones_reales(driver.find_element(*P.AG_DD_AGENCIA))
        if not reales:  # si no hay agencias cargadas, elegir un país con agencias
            seleccionar(driver, wait, P.AG_DD_PAIS, "Argentina", postback=True)
            reales = _opciones_reales(driver.find_element(*P.AG_DD_AGENCIA))
        agencia = next((o.text.strip() for o in reales if o.text.strip() not in existentes), None)
        assert agencia, "No hay una agencia disponible que no esté ya en la grilla."
        Select(driver.find_element(*P.AG_DD_AGENCIA)).select_by_visible_text(agencia)
        safe_send_keys(wait, P.AG_TXT_OVER, "0")
        allure.attach(f"Agencia elegida: {agencia}", "Agencia", allure.attachment_type.TEXT)

    with allure.step("3. Agregar y confirmar que se guardó"):
        safe_click(wait, P.AG_BTN_AGREGAR)
        time.sleep(1.5)  # postback
        driver.find_elements(*P.TAB_AGENCIAS) and safe_click(wait, P.TAB_AGENCIAS)
        fila = wait.until(EC.presence_of_element_located(P.ag_celda_agencia(agencia)))
        assert fila is not None, f"La agencia '{agencia}' no se guardó en la grilla."
        allure.attach(driver.get_screenshot_as_png(), "Agregada", allure.attachment_type.PNG)

    with allure.step("4. Borrar la agencia agregada (cleanup) y verificar"):
        safe_click(wait, P.ag_borrar_por_agencia(agencia))
        wait.until(EC.visibility_of_element_located(P.AG_CONFIRM_SI))
        safe_click(wait, P.AG_CONFIRM_SI)
        time.sleep(1.5)  # postback de borrado
        wait.until_not(EC.presence_of_element_located(P.ag_celda_agencia(agencia)))
        assert not driver.find_elements(*P.ag_celda_agencia(agencia)), \
            f"La agencia '{agencia}' seguía en la grilla tras borrarla."
        allure.attach(driver.get_screenshot_as_png(), "Borrada", allure.attachment_type.PNG)


# ──────────────────────────────────────────────────────────────────────────────
# SOLAPA 2 — PRODUCTOS: alta + baja
# ──────────────────────────────────────────────────────────────────────────────
@allure.feature("WebAdmin AMV Travel")
@allure.story("Adm. de puntos · Productos: alta de regla + baja (cleanup)")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("""
Agrega una regla de producto por una ciudad random (que no esté ya en la grilla),
valida que se guardó (aparece en gvProductsSetting) y luego la elimina.
⚠ Best-effort: la semántica del combo 'wildcard' y las dependencias de ciudad pueden
requerir ajuste tras la primera corrida.
""")
def test_puntos_productos(login_webadmin):
    driver = login_webadmin
    wait = WebDriverWait(driver, 45)

    with allure.step("1. Ir a Adm. de puntos → solapa Productos"):
        _ir_a_puntos(wait)
        safe_click(wait, P.TAB_PRODUCTOS)
        time.sleep(1)

    with allure.step("2. Configurar una regla por ciudad random no existente"):
        existentes = {e.get_attribute("textContent").strip()
                      for e in driver.find_elements(*P.pr_filas_ciudad())}
        # wildcard: primera opción real (regla a nivel ciudad)
        wc = _opciones_reales(driver.find_element(*P.PR_DD_WILDCARD))
        if wc:
            Select(driver.find_element(*P.PR_DD_WILDCARD)).select_by_visible_text(wc[0].text)
            time.sleep(1)
        # ciudad: una opción "limpia" (sin 'TODOS') que no esté ya en la grilla
        ciudades = [o for o in _opciones_reales(driver.find_element(*P.PR_DD_CITY))
                    if "TODOS" not in o.text.upper()]
        ciudad = next((o.text.strip() for o in ciudades if o.text.strip() not in existentes), None)
        assert ciudad, "No hay una ciudad disponible que no esté ya en la grilla."
        Select(driver.find_element(*P.PR_DD_CITY)).select_by_visible_text(ciudad)
        time.sleep(1)
        if driver.find_elements(*P.PR_TXT_MARKUP):
            safe_send_keys(wait, P.PR_TXT_MARKUP, "1")
        allure.attach(f"Ciudad elegida: {ciudad}", "Ciudad", allure.attachment_type.TEXT)

    with allure.step("3. Agregar y confirmar que se guardó"):
        safe_click(wait, P.PR_BTN_AGREGAR)
        time.sleep(1.5)
        driver.find_elements(*P.TAB_PRODUCTOS) and safe_click(wait, P.TAB_PRODUCTOS)
        fila = wait.until(EC.presence_of_element_located(P.pr_celda_ciudad(ciudad)))
        assert fila is not None, f"La regla para '{ciudad}' no se guardó en la grilla."
        allure.attach(driver.get_screenshot_as_png(), "Agregada", allure.attachment_type.PNG)

    with allure.step("4. Borrar la regla agregada (cleanup) y verificar"):
        safe_click(wait, P.pr_borrar_por_ciudad(ciudad))
        wait.until(EC.visibility_of_element_located(P.PR_CONFIRM_SI))
        safe_click(wait, P.PR_CONFIRM_SI)
        time.sleep(1.5)
        wait.until_not(EC.presence_of_element_located(P.pr_celda_ciudad(ciudad)))
        assert not driver.find_elements(*P.pr_celda_ciudad(ciudad)), \
            f"La regla para '{ciudad}' seguía en la grilla tras borrarla."
        allure.attach(driver.get_screenshot_as_png(), "Borrada", allure.attachment_type.PNG)


# ──────────────────────────────────────────────────────────────────────────────
# SOLAPA 3 — CONFIGURACIÓN: validar que esté todo lo que tiene que estar
# ──────────────────────────────────────────────────────────────────────────────
@allure.feature("WebAdmin AMV Travel")
@allure.story("Adm. de puntos · Configuración: la solapa tiene todos sus controles")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("""
Valida (sin modificar) que la solapa Configuración expone: multiplicador de puntos,
toggle de habilitación del sistema, puntos a usuarios (toggle + %), puntos a files
no-online (toggle + %) y la grilla de Categorías de puntos con sus columnas y filas.
""")
def test_puntos_configuracion(login_webadmin):
    driver = login_webadmin
    wait = WebDriverWait(driver, 45)

    with allure.step("1. Ir a Adm. de puntos → solapa Configuración"):
        _ir_a_puntos(wait)
        safe_click(wait, P.TAB_CONFIG)
        time.sleep(1)

    with allure.step("2. Validar que están todos los controles clave"):
        controles = {
            "Habilitar sistema de puntos": P.CFG_CB_ENABLED,
            "Multiplicador de puntos": P.CFG_MULTIPLIER,
            "Toggle puntos a usuarios": P.CFG_CB_USER,
            "% puntos a usuarios": P.CFG_TXT_USER,
            "Toggle puntos a files no-online": P.CFG_CB_NONONLINE,
            "% files no-online": P.CFG_TXT_NONONLINE,
            "Grilla de categorías": P.CFG_GRID_CATEGORIES,
        }
        faltantes = [nombre for nombre, loc in controles.items() if not driver.find_elements(*loc)]
        assert not faltantes, f"Faltan controles en Configuración: {faltantes}"

    with allure.step("3. Validar columnas y filas de la grilla de categorías"):
        wait.until(EC.presence_of_element_located(P.CFG_GRID_CATEGORIES))
        cols = [c.get_attribute("textContent").strip()
                for c in driver.find_elements(*P.CFG_CATEGORIES_HEADERS)
                if c.get_attribute("textContent").strip()]
        faltan_cols = [c for c in P.CFG_COLUMNAS_CATEGORIES if c not in cols]
        assert not faltan_cols, f"Faltan columnas en Categorías: {faltan_cols}. Encontradas: {cols}"
        filas = driver.find_elements(*P.CFG_CATEGORIES_FILAS)
        assert len(filas) > 0, "La grilla de Categorías vino vacía."
        allure.attach(" | ".join(cols), "Columnas categorías", allure.attachment_type.TEXT)
        allure.attach(f"Categorías: {len(filas)}", "Filas", allure.attachment_type.TEXT)
        allure.attach(driver.get_screenshot_as_png(), "Configuracion", allure.attachment_type.PNG)
