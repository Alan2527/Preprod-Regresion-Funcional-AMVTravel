"""
Page Object de Reservas en el WebAdmin (booking/).

La sección Reservas del panel de administración tiene DOS pantallas de solo
lectura (no hay nada que crear): se valida que las grillas existan, traigan las
columnas esperadas y no vengan vacías.

- Adm. de Reservas → /administration/booking/default.aspx      (con filtro de fechas)
- Canceladas       → /administration/booking/defaultcancel.aspx (sin filtro)

Ambas usan la MISMA GridView `ctl00_cph1_gvBooks` con las mismas columnas.

Selectores confirmados contra el HTML real (qa.amv.travel, mismos IDs ASP.NET
que preprod).
"""
from selenium.webdriver.common.by import By


class WebAdminReservasPage:

    # ── Menú lateral: Reservas (acordeón) → submenús ──────────────────────────
    MENU_RESERVAS = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'javascript:void')]"
        "//span[normalize-space()='Reservas']")
    SUBMENU_ADM = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'/administration/booking/default.aspx')]"
        "//span[normalize-space()='Adm. de Reservas']")
    SUBMENU_CANCELADAS = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'/administration/booking/defaultcancel.aspx')]"
        "//span[normalize-space()='Canceladas']")

    # ── URLs (para esperar la navegación) ─────────────────────────────────────
    URL_ADM = "/administration/booking/default.aspx"
    URL_CANCELADAS = "/administration/booking/defaultcancel.aspx"

    # ── Grilla principal (idéntica en ambas pantallas) ────────────────────────
    TABLA = (By.ID, "ctl00_cph1_gvBooks")
    # Filas de datos (la GridView usa rowstyle / altrowstyle).
    FILAS = (By.CSS_SELECTOR,
        "#ctl00_cph1_gvBooks tr.rowstyle, #ctl00_cph1_gvBooks tr.altrowstyle")
    # Celdas de la fila de encabezado (primera <tr> de la GridView).
    HEADERS = (By.CSS_SELECTOR,
        "#ctl00_cph1_gvBooks tr:first-child th, #ctl00_cph1_gvBooks tr:first-child td")

    # Columnas que la tabla DEBE traer.
    COLUMNAS_ESPERADAS = [
        "Código", "Fecha / Hora", "Fecha de confirmación", "Total",
        "Usuario", "Agencia", "Disponibilidad", "Editar",
    ]

    # ── Filtro por rango de fechas (solo en Adm. de Reservas) ─────────────────
    FILTRO_DESDE = (By.ID, "ctl00_cph1_dpFrom_txtDateTime")
    FILTRO_HASTA = (By.ID, "ctl00_cph1_dpTo_txtDateTime")
    BTN_FILTRAR = (By.ID, "ctl00_cph1_btnFilter")
