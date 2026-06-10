"""
Page Object de la creación/edición de Habitaciones en el WebAdmin.
Centraliza la navegación del menú, los campos del formulario, las pestañas del
detalle y la búsqueda en la tabla de habitaciones.
"""

from selenium.webdriver.common.by import By


class WebAdminRoomPage:
    # --- Navegación (menú lateral) ---
    MENU_HOTELES = (By.XPATH, "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'javascript:void(3)')]//span[normalize-space()='Hoteles']")
    SUBMENU_ADM_HAB = (By.XPATH, "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'/administration/rooms/default.aspx')]//span[normalize-space()='Habitaciones']")
    BTN_NUEVO = (By.ID, "btnAddNew")

    # --- Formulario ---
    TXT_NAME = (By.NAME, "ctl00$cph1$RoomTabContainer$pnlRoomDetails$txtName$txtValue")
    DD_HOTEL = (By.NAME, "ctl00$cph1$RoomTabContainer$pnlRoomDetails$ddlHotel")
    TXT_CAPACIDAD = (By.NAME, "ctl00$cph1$RoomTabContainer$pnlRoomDetails$txtCapacidad")
    CB_EXTRA_BED = (By.NAME, "ctl00$cph1$RoomTabContainer$pnlRoomDetails$cbExtraBed")
    DD_ROOM_TYPE = (By.NAME, "ctl00$cph1$RoomTabContainer$pnlRoomDetails$ddlRoomType")
    CB_PUBLICADO = (By.NAME, "ctl00$cph1$RoomTabContainer$pnlRoomDetails$cbPublicado")
    CB_FOR_RESIDENTS = (By.NAME, "ctl00$cph1$RoomTabContainer$pnlRoomDetails$cbForResidents")
    CB_FOR_NON_RESIDENTS = (By.NAME, "ctl00$cph1$RoomTabContainer$pnlRoomDetails$cbForNonResidents")
    # Campos de edades de menores (actualmente rotos en la app -> se dejan documentados)
    DP_KIDS_FROM = (By.NAME, "ctl00$cph1$RoomTabContainer$pnlRoomDetails$dpKidsFrom$txtDateTime")
    DP_KIDS_TO = (By.NAME, "ctl00$cph1$RoomTabContainer$pnlRoomDetails$dpKidsTo$txtDateTime")

    # Checkboxes que deben quedar tildados
    CHECKBOXES = [CB_EXTRA_BED, CB_PUBLICADO, CB_FOR_RESIDENTS, CB_FOR_NON_RESIDENTS]

    # --- Guardar ---
    BTN_GUARDAR = (By.XPATH, "(//input[@value='Guardar'] | //button[@value='Guardar'])[1]")

    # --- Pestañas del detalle (deben estar habilitadas tras guardar) ---
    # Reales: Detalle | Tarifas | Tarifario | Detalle del tarifario | Freesale
    TAB_NAMES = ["Tarifas", "Tarifario", "Detalle del tarifario", "Freesale"]

    @staticmethod
    def tab_locator(nombre):
        # Match exacto (normalize-space) acotado al contenedor de pestañas de la
        # habitación, para no confundir "Tarifario" con "Detalle del tarifario", etc.
        return (By.XPATH, f"//div[contains(@id,'RoomTabContainer')]//span[normalize-space()='{nombre}']")

    # --- Tabla / búsqueda ---
    TXT_SEARCH = (By.NAME, "ctl00$cph1$txtSearch")
    BTN_SEARCH = (By.NAME, "ctl00$cph1$btnSearch")
    TABLA = (By.CSS_SELECTOR, "table.tablestyle")

    @staticmethod
    def fila_por_nombre(nombre):
        return (By.XPATH, f"//table[contains(@class,'tablestyle')]//td[contains(., \"{nombre}\")]")
