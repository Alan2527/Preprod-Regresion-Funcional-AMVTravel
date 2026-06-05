"""
Page Object del flujo de reserva de Hoteles (sitio público).
Centraliza los selectores de la búsqueda, configuración de pasajeros, filtros,
card de resultados, detalle del hotel y confirmación de reserva.
"""

from selenium.webdriver.common.by import By


class FrontHotelesPage:
    # --- Búsqueda ---
    TAB_HOTELES = (By.CSS_SELECTOR, "a[href='#tabHotels']")
    INPUT_DESTINO = (By.ID, "ctl00_cphMainSlider_ctl00_ctrlHotelSearchControl_searchDestination")
    OPCION_BARILOCHE = (By.XPATH, "//*[contains(text(), 'Bariloche, Argentina')]")
    INPUT_CALENDARIO = (By.ID, "txtCalendar")
    BTN_SEARCH = (By.ID, "btnSearch")

    # --- Pasajeros ---
    BTN_PASAJEROS = (By.XPATH, "//span[contains(@class, 'pink-btn') and contains(@class, 'passengerQuantity-botton')]")
    BTN_ROOMS = (By.XPATH, "//span[@onclick=\"QuantityModify(+1,'rooms')\"]")
    BTN_ADULTS = (By.XPATH, "//span[@onclick=\"QuantityModify(1,'adults')\"]")
    BTN_CHILDREN = (By.XPATH, "//span[@onclick=\"ChildrenModify(true)\"]")
    CHILD_AGE_1 = (By.ID, "childrenAge1")
    CHILD_AGE_2 = (By.ID, "childrenAge2")

    # --- Resultados / filtros ---
    DISPONIBILIDAD = (By.XPATH, "//span[@title='Disponibilidad']")
    FILTRO_ZONA = (By.XPATH, "//span[@title='Zona Catedral ']")
    FILTRO_APART = (By.XPATH, "//span[@title='Apart']")
    FILTRO_AIRE = (By.XPATH, "//span[@title='Aire Acondicionado']")
    BTN_APLICAR_FILTROS = (By.ID, "ctl00_cphSideMain_lnkFilter")
    PANEL_RESULTADOS = (By.ID, "ctl00_cphMain_updMainPanel")

    # --- Card del hotel ---
    CARD_IMG = (By.CSS_SELECTOR, "img[style*='height: 200px']")
    CARD_NOMBRE = (By.CSS_SELECTOR, "div[style*='font-size: 20px'] span")
    CARD_RATING = (By.CSS_SELECTOR, "div.single-car-rating")
    CARD_ZONA = (By.CSS_SELECTOR, "div[style*='color: #6B72F2'] i")
    CARD_DESC = (By.CSS_SELECTOR, "div[style*='margin-top: 2px'] p")
    CARD_DISPONIBLE = (By.CSS_SELECTOR, "div#True.available-hotel")
    CARD_PRECIO = (By.CSS_SELECTOR, "div[style*='background-color: #444444']")
    BTN_VER_MAS = (By.CSS_SELECTOR, "a#verMasbtn.btn.pink-btn.apreload")

    # --- Detalle del hotel ---
    DET_NOMBRE = (By.CSS_SELECTOR, "h2.h2name")
    DET_RATING = (By.CSS_SELECTOR, "div.rating.clearfix")
    DET_IMAGENES = (By.CSS_SELECTOR, "img.newSlide")
    DET_DESCRIPCION = (By.XPATH, '//*[@id="aspnetForm"]/article/div[1]/div[2]/div[2]/div[4]')
    DET_AMENITIES = (By.ID, "ctl00_cphMain_amenitiesList")
    DET_NAV_TABS = (By.CSS_SELECTOR, "ul.nav.nav-tabs")
    DET_OFERTA = (By.CSS_SELECTOR, "h2.smallh2")
    DET_TABLA_PRECIOS = (By.CSS_SELECTOR, "table.table.table-bordered.table-striped")
    DET_POLITICAS = (By.CSS_SELECTOR, "div.fleft")

    # --- Reserva ---
    BTN_SUMAR_HAB = (By.ID, "72260-185813-105-1-2-Integration-26611-suma")
    INPUT_CANTIDAD = (By.ID, "185813")
    BTN_GUARDAR = (By.XPATH, "//input[contains(@onclick, 'Guardar(185813')]")
