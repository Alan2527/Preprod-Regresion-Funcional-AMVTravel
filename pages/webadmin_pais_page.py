"""
Page Object de Países en el WebAdmin (Ubicación → Paises, types/country.aspx).

Pantalla de SOLO LECTURA (no tiene botón de crear): se valida que la grilla
`gvCountries` traiga las columnas esperadas y no venga vacía, y que estén los
controles de búsqueda/filtro. Mismo criterio que Reservas / Reporte de Circuitos.

Selectores confirmados contra el DOM real (qa.amv.travel, mismos IDs ASP.NET que
preprod).
"""
from selenium.webdriver.common.by import By


class WebAdminPaisPage:

    # ── Menú lateral: Ubicación (acordeón) → Paises ───────────────────────────
    MENU_UBICACION = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'javascript:void')]"
        "//span[normalize-space()='Ubicación']")
    SUBMENU_PAISES = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'/administration/types/country.aspx')]"
        "//span[normalize-space()='Paises']")

    URL = "/administration/types/country.aspx"

    # ── Grilla ────────────────────────────────────────────────────────────────
    TABLA = (By.ID, "ctl00_cph1_gvCountries")
    FILAS = (By.CSS_SELECTOR,
        "#ctl00_cph1_gvCountries tr.rowstyle, #ctl00_cph1_gvCountries tr.altrowstyle")
    # Fila de encabezado (la GridView la renderiza como tr.headstyle con <th>).
    HEADERS = (By.CSS_SELECTOR,
        "#ctl00_cph1_gvCountries tr.headstyle th, #ctl00_cph1_gvCountries th")

    COLUMNAS_ESPERADAS = [
        "Nombre", "Continente", "Publicado", "Mostrar en el sitio", "Editar",
    ]

    # ── Búsqueda / filtros ────────────────────────────────────────────────────
    TXT_SEARCH = (By.NAME, "ctl00$cph1$txtSearch")
    BTN_SEARCH = (By.NAME, "ctl00$cph1$btnSearch")
    DD_STATUS = (By.NAME, "ctl00$cph1$ddStatus")
