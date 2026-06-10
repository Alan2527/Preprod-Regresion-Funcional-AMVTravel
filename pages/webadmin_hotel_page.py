"""
Page Object de la creación/edición de Hoteles en el WebAdmin.
Centraliza la navegación del menú, los campos del formulario (Información
General, Configuración, Ubicación y Descripción), las pestañas del detalle y
la búsqueda en la tabla de hoteles.
"""

from selenium.webdriver.common.by import By


class WebAdminHotelPage:
    # --- Navegación (menú lateral) ---
    MENU_HOTELES = (By.XPATH, "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'javascript:void(3)')]//span[normalize-space()='Hoteles']")
    SUBMENU_ADM_HOTELES = (By.XPATH, "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'/administration/hotels/default.aspx')]//span[normalize-space()='Adm. de Hoteles']")
    BTN_NUEVO = (By.ID, "ctl00_cphActions_btnNew")

    # --- Información general ---
    TXT_NAME = (By.NAME, "ctl00$cph1$HotelTabContainer$pnlHotelDetails$txtName$txtValue")
    DD_CATEGORY = (By.NAME, "ctl00$cph1$HotelTabContainer$pnlHotelDetails$ddHotelCategory")
    TXT_DISPLAY_ORDER = (By.NAME, "ctl00$cph1$HotelTabContainer$pnlHotelDetails$txtDisplayOrder")
    DD_BREAKFAST = (By.NAME, "ctl00$cph1$HotelTabContainer$pnlHotelDetails$ddBreakfastType")

    # --- Configuración y opciones (checkboxes visibles del form) ---
    # cbForResidents / cbForNonResidents existen pero están en un div display:none
    # (los maneja el code-behind con sus defaults), por eso NO se tocan acá.
    CHECKBOXES = [
        (By.NAME, "ctl00$cph1$HotelTabContainer$pnlHotelDetails$cbPublicado"),
        (By.NAME, "ctl00$cph1$HotelTabContainer$pnlHotelDetails$cbGreat"),
        (By.NAME, "ctl00$cph1$HotelTabContainer$pnlHotelDetails$cbSuggested"),
        (By.NAME, "ctl00$cph1$HotelTabContainer$pnlHotelDetails$cbFamilyPlan"),
    ]
    # "Observaciones" es visible; "Emails Notif." (txtEmailNoti) ahora está oculto
    # (div display:none) y su validador está deshabilitado -> NO se completa.
    TXT_OBSERVATION = (By.NAME, "ctl00$cph1$HotelTabContainer$pnlHotelDetails$txtObservation")

    # --- Ubicación y contacto ---
    TXT_ADDRESS = (By.NAME, "ctl00$cph1$HotelTabContainer$pnlHotelDetails$txtAddress$txtValue")
    DD_CITY = (By.NAME, "ctl00$cph1$HotelTabContainer$pnlHotelDetails$ddlCity")
    DD_DISTRICT = (By.NAME, "ctl00$cph1$HotelTabContainer$pnlHotelDetails$ddlDistrict")
    TXT_EMAIL = (By.NAME, "ctl00$cph1$HotelTabContainer$pnlHotelDetails$txtEmail$txtValue")
    TXT_WEB = (By.NAME, "ctl00$cph1$HotelTabContainer$pnlHotelDetails$txtWeb")
    TXT_ADMIN = (By.NAME, "ctl00$cph1$HotelTabContainer$pnlHotelDetails$txtAdmin")

    # --- Descripción (editor Quill) ---
    QL_EDITOR = (By.CSS_SELECTOR, "div.ql-editor")

    # --- Guardar ---
    BTN_GUARDAR = (By.XPATH, "(//input[@value='Guardar'] | //button[@value='Guardar'])[1]")

    # --- Pestañas del detalle (deben estar habilitadas) ---
    # Pestañas reales del detalle de hotel (match parcial en tab_locator).
    TAB_NAMES = ["Proveedores", "Imagenes", "Video", "Habitaciones", "Amenities", "Puntos de", "Politicas"]

    @staticmethod
    def tab_locator(nombre_parcial):
        # Acotado al contenedor de pestañas del hotel para no chocar con el menú lateral.
        return (By.XPATH, f"//div[contains(@id,'HotelTabContainer')]//span[contains(normalize-space(), '{nombre_parcial}')]")

    # --- Tabla / búsqueda de hoteles ---
    TXT_SEARCH = (By.NAME, "ctl00$cph1$txtSearch")
    BTN_SEARCH = (By.NAME, "ctl00$cph1$btnSearch")
    TABLA = (By.CSS_SELECTOR, "table.tablestyle")

    @staticmethod
    def fila_por_nombre(nombre):
        return (By.XPATH, f"//table[contains(@class,'tablestyle')]//td[contains(., \"{nombre}\")]")
