"""
Validación de pantallas de SOLO LECTURA del WebAdmin (Finanzas, Contenidos, Widget).

Criterio (pedido de Alan): "cuando no hay nada que crear, revisamos que las tablas
traigan todo lo que tienen que traer" → se valida que cada grilla exista, traiga TODAS
las columnas esperadas y no venga vacía. Mismo enfoque que Reservas / Países.

Se resuelve con un test parametrizado (un caso = una pantalla) para no duplicar el
mismo flujo de validación de grilla siete veces.
"""
import time
import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from helpers import safe_click


# (nombre, menú padre, url del submenú, id de la grilla, columnas esperadas)
CASOS = [
    ("Finanzas · Monedas", "Finanzas",
     "/administration/Currency/Currency.aspx", "ctl00_cph1_gvCurrency",
     ["Nombre", "Código", "Fecha de Actualización", "Cotización", "Publicado", "Editar"]),
    ("Finanzas · Cotizaciones", "Finanzas",
     "/administration/CurrencyExchange/CurrencyExchange.aspx", "ctl00_cph1_gvCurrency",
     ["Moneda", "Cotización", "Cotización Travel Sale", "Cotización Oportunidades",
      "Aplica", "Editar", "Borrar"]),
    ("Finanzas · Tipos de Tarifa", "Finanzas",
     "/administration/types/ratetypes.aspx", "ctl00_cph1_gvRateTypes",
     ["Nombre", "Publicado", "Editar"]),
    ("Ubicación · Puntos de Interés", "Ubicación",
     "/administration/benchmarks/default.aspx", "ctl00_cph1_gvData",
     ["Imagen", "Nombre", "Orden", "Publicado", "Editar", "Borrar"]),
    ("Contenidos · Configuración", "Contenidos",
     "/administration/settings/Default.aspx",
     "ctl00_cph1_SettingsTabContainer_pnlGeneral_gvSettings",
     ["Nombre", "Valor", "Editar", "Borrar"]),
    ("Contenidos · Avisos Web", "Contenidos",
     "/administration/popup/default.aspx", "ctl00_cph1_gvPopUp",
     ["ID", "Imagen", "Nombre", "Orden", "Publicado", "Editar", "Borrar"]),
    ("Widget · Clientes Mayoristas", "Widget",
     "/administration/widget/default.aspx", "ctl00_cph1_gvWholesaleClients",
     ["Name", "Market", "Hoteles", "Servicios", "Multidestinos", "Ofertas",
      "Cotizaciones", "Reservas", "Tarifario", "Autologin"]),
    ("Widget · Reservas", "Widget",
     "/administration/widget/booking/default.aspx", "ctl00_cph1_gvBooks",
     ["Código", "Fecha / Hora", "Fecha de confirmación", "Total", "Usuario",
      "Agencia Mayorista", "Agencia Minorista", "Disponibilidad", "Editar"]),
]


@allure.feature("WebAdmin AMV Travel")
@allure.story("Finanzas/Contenidos/Widget: grillas de solo lectura traen columnas y filas")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize("nombre,menu,url,grid_id,columnas", CASOS, ids=[c[0] for c in CASOS])
def test_grid_readonly(login_webadmin, nombre, menu, url, grid_id, columnas):
    driver = login_webadmin
    wait = WebDriverWait(driver, 45)

    with allure.step(f"1. Navegar a {nombre}"):
        menu_loc = (By.XPATH,
            f"//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'javascript:void')]"
            f"//span[normalize-space()='{menu}']")
        sub_loc = (By.XPATH,
            f"//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'{url}')]")
        safe_click(wait, menu_loc)
        time.sleep(1)  # animación del acordeón
        safe_click(wait, sub_loc)
        wait.until(EC.url_contains(url))

    with allure.step("2. Validar columnas de la grilla"):
        wait.until(EC.presence_of_element_located((By.ID, grid_id)))
        time.sleep(1)
        cols = [c.get_attribute("textContent").strip()
                for c in driver.find_elements(By.CSS_SELECTOR, f"#{grid_id} th")
                if c.get_attribute("textContent").strip()]
        faltantes = [c for c in columnas if c not in cols]
        assert not faltantes, f"{nombre}: faltan columnas {faltantes}. Encontradas: {cols}"
        allure.attach(" | ".join(cols), "Columnas", allure.attachment_type.TEXT)

    with allure.step("3. Validar que la grilla no viene vacía"):
        filas = driver.find_elements(
            By.CSS_SELECTOR, f"#{grid_id} tr.rowstyle, #{grid_id} tr.altrowstyle")
        assert len(filas) > 0, f"{nombre}: la grilla vino vacía (sin filas)."
        allure.attach(f"Filas: {len(filas)}", "Filas", allure.attachment_type.TEXT)
        allure.attach(driver.get_screenshot_as_png(), "Grilla", allure.attachment_type.PNG)


@allure.feature("WebAdmin AMV Travel")
@allure.story("Finanzas · Tipos de Cambio: la pantalla carga con sus controles")
@allure.severity(allure.severity_level.MINOR)
@allure.description("""
Tipos de Cambio (ChangeRate) no tiene grilla ni un identificador único creable
(rango de fechas + valor) → smoke: la pantalla carga y expone sus controles clave
(botón 'Nuevo' y el 'Guardar' de valores por defecto).
""")
def test_tipos_de_cambio_smoke(login_webadmin):
    driver = login_webadmin
    wait = WebDriverWait(driver, 45)
    url = "/administration/ChangeRate/ChangeRate.aspx"

    with allure.step("1. Navegar a Finanzas → Tipos de Cambio"):
        safe_click(wait, (By.XPATH,
            "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'javascript:void')]"
            "//span[normalize-space()='Finanzas']"))
        time.sleep(1)
        safe_click(wait, (By.XPATH,
            f"//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'{url}')]"))
        wait.until(EC.url_contains(url))

    with allure.step("2. La pantalla expone sus controles clave"):
        nuevo = driver.find_elements(By.ID, "ctl00_cphActions_btnNew")
        guardar = driver.find_elements(By.ID, "ctl00_cph1_tabDefaults_pnlDefaultsDetails_btnDefaults")
        assert nuevo or guardar, "Tipos de Cambio no muestra sus controles (Nuevo / Guardar defaults)."
        allure.attach(driver.get_screenshot_as_png(), "Pantalla", allure.attachment_type.PNG)
