"""
Page Object del flujo de reserva de Servicios (sitio público).
Centraliza los selectores de búsqueda, cards, detalle, pasajeros, carrito y checkout.
"""

from selenium.webdriver.common.by import By


class FrontServiciosPage:
    # --- Búsqueda ---
    TAB_SERVICIOS = (By.CSS_SELECTOR, "a[href='#tabServices']")
    DDL_CIUDAD = (By.CSS_SELECTOR, "#ctl00_cphMainSlider_ctl00_ctrlServiceSearchControl_updServicesCity .ts-control")
    OPCION_BARILOCHE = (By.XPATH, "//div[contains(@class, 'option') and contains(text(), 'Bariloche')] | //div[contains(text(), 'Bariloche')]")
    DDL_TIPO = (By.CSS_SELECTOR, "#ctl00_cphMainSlider_ctl00_ctrlServiceSearchControl_updServicesOptionals .ts-control")
    OPCION_EXCURSION = (By.XPATH, "//div[contains(@class, 'option') and contains(text(), 'Excursión')] | //div[contains(text(), 'Excursión')]")
    BTN_SEARCH = (By.ID, "ctl00_cphMainSlider_ctl00_ctrlServiceSearchControl_btnSearch")

    # --- Cards de resultados ---
    CARD = (By.CSS_SELECTOR, "div.panelShadow.col-sm-6")
    CARD_IMG = (By.CSS_SELECTOR, "img[style*='width: 450px']")
    CARD_NOMBRE = (By.CSS_SELECTOR, "h4.h4Span")
    CARD_TABLA = (By.CSS_SELECTOR, "table[style*='text-align:center'], table[style*='text-align: center']")
    CARD_DESC = (By.CSS_SELECTOR, "div.divservlimit")
    CARD_BTN = (By.CSS_SELECTOR, "a.apreload.btn.btnGray.pink-btn")

    # --- Detalle ---
    DET_NOMBRE = (By.CSS_SELECTOR, "h3.h3ServiceName")
    DET_IMG = (By.CSS_SELECTOR, "img.popu")
    DET_DETALLES = (By.CSS_SELECTOR, "div.detailsdiv")
    DET_TABLA = (By.CSS_SELECTOR, "table.table.table-bordered.table-striped")

    # --- Pasajeros ---
    DD_PAX_1 = (By.NAME, "ctl00$cphMainSlider$lvServiceRates$ctrl0$ctrlPaxQuantityControl$ddPax")
    DD_PAX_2 = (By.NAME, "ctl00$cphMainSlider$lvServiceRates$ctrl1$ctrlPaxQuantityControl$ddPax")

    # --- Carrito / reserva ---
    CART_COUNT = (By.ID, "lblCartCount")
    BTN_RESERVAR = (By.ID, "ctl00_cphMainSlider_lnkBookService")
    CART_ANCHOR = (By.ID, "AncoreShoppingCart")
    BTN_FINALIZAR = (By.ID, "btnFinalizar")

    # --- Checkout ---
    INPUT_REFERENCIA = (By.NAME, "ctl00$cphMain$txtReference")
    INPUT_COMENTARIO = (By.NAME, "ctl00$cphMain$txtComment")
    BTN_SUCCESS = (By.CSS_SELECTOR, "a.btn.btn-success.apreload")
    INPUT_COMENTARIO_1 = (By.NAME, "ctl00$cphMain$lvBooking$ctrl0$ctrlBookingServiceDetailControl$txtDetail")
    INPUT_COMENTARIO_2 = (By.NAME, "ctl00$cphMain$lvBooking$ctrl1$ctrlBookingServiceDetailControl$txtDetail")
    PAX_NAME = (By.ID, "ctl00_cphMain_lvPassengersData_ctrl0_txtName")
    PAX_SURNAME = (By.ID, "ctl00_cphMain_lvPassengersData_ctrl0_txtSurName")
    PAX_PASSPORT = (By.ID, "ctl00_cphMain_lvPassengersData_ctrl0_txtPassport")
    PAX_BIRTHDAY = (By.ID, "ctl00_cphMain_lvPassengersData_ctrl0_txtBirthday")
    PAX_NATIONALITY = (By.ID, "ctl00_cphMain_lvPassengersData_ctrl0_txtNationality")
    PAX_QUANTITY = (By.ID, "ctl00_cphMain_txtPaxQuantity")
    CHK_TERMINOS = (By.ID, "ctl00_cphMain_cbxTermsAndConditions")
    BTN_CONFIRMAR = (By.XPATH, "//input[@id='ctl00_cphMain_btnSaveBook' and @type='button' and @value='Confirmar reserva']")

    # --- Validación final ---
    TAB_BOOKING = (By.CSS_SELECTOR, "a[href='#tabBooking']")
    TABLA_BOOKING = (By.ID, "tableTab1")
