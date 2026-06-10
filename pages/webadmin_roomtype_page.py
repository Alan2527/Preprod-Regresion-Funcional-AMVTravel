"""
Page Object de la creacion de Tipos de Habitacion en el WebAdmin.
Centraliza la navegacion del menu lateral, los campos del formulario
(nombre + detalle + publicado), el boton de guardar y la tabla.
"""

from selenium.webdriver.common.by import By


class WebAdminRoomTypePage:
    # --- Navegacion (menu lateral) ---
    # "Hoteles" es el padre acordeon (href javascript:void(3)); "Tipos de habitacion" su submenu.
    MENU_HOTELES = (By.XPATH, "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'javascript:void(3)')]//span[normalize-space()='Hoteles']")
    SUBMENU_TIPOS_HAB = (By.XPATH, "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'/administration/types/roomtypes.aspx')]//span[normalize-space()='Tipos de habitación']")

    # Boton "Nuevo" (input submit en el header de acciones).
    BTN_NUEVO = (By.NAME, "ctl00$cphActions$btnNew")

    # --- Formulario ---
    TXT_NAME = (By.NAME, "ctl00$cph1$txtName$txtValue")
    TXT_DETAIL = (By.NAME, "ctl00$cph1$txtDetail$txtValue")
    CB_PUBLICADO = (By.ID, "ctl00_cph1_cbPublicado")

    # --- Guardar ---
    BTN_GUARDAR = (By.NAME, "ctl00$cph1$btnSave")

    # --- Tabla / validacion ---
    TABLA = (By.CSS_SELECTOR, "table.tablestyle")

    @staticmethod
    def fila_por_nombre(nombre):
        # El nombre completo (con fecha/hora) aparece tal cual en el <td>; normalize-space
        # tolera el padding/whitespace del HTML de la grilla.
        return (By.XPATH, f"//table[contains(@class,'tablestyle')]//td[contains(normalize-space(), \"{nombre}\")]")
