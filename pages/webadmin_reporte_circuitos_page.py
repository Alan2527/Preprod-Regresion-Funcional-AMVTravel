"""
Page Object del Reporte de Circuitos en el WebAdmin (customtours/).
Sólo se valida que la tabla principal exista y tenga contenido (no vacía).

Selectores confirmados contra el HTML real (preprod.amv.travel).
"""
from selenium.webdriver.common.by import By


class WebAdminReporteCircuitosPage:

    # ── Menú lateral: Circuitos (acordeón) → Reporte Circuitos ────────────────
    MENU_CIRCUITOS = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'javascript:void')]"
        "//span[normalize-space()='Circuitos']")
    SUBMENU_REPORTE = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'/administration/customtours/')]"
        "//span[normalize-space()='Reporte Circuitos']")

    # ── Tabla principal ───────────────────────────────────────────────────────
    TABLA = (By.ID, "ctl00_cph1_gvData")
    # Filas de datos (la GridView usa rowstyle / altrowstyle).
    FILAS = (By.CSS_SELECTOR, "#ctl00_cph1_gvData tr.rowstyle, #ctl00_cph1_gvData tr.altrowstyle")
