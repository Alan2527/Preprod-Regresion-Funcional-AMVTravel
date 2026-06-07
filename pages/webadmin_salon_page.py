"""
Page Object de la creacion de Salones (meeting salons) en el WebAdmin.
Centraliza la navegacion del menu lateral, los campos del formulario
(nombre, capacidad, orden, ciudad, hotel, publicado), guardar y la tabla.

Particularidad: el select de Ciudad dispara un postback (onchange) que recarga
la lista de Hoteles -> hay que elegir ciudad y esperar a que aparezca el hotel.
"""

from selenium.webdriver.common.by import By


class WebAdminSalonPage:
    # --- Navegacion (menu lateral) ---
    # "Hoteles" es el padre acordeon (href javascript:void(3)); "Salones" su submenu.
    MENU_HOTELES = (By.XPATH, "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'javascript:void(3)')]//span[normalize-space()='Hoteles']")
    SUBMENU_SALONES = (By.XPATH, "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'/administration/meetingsalons/')]//span[normalize-space()='Salones']")

    # Boton "Nuevo" en la lista: <input type="button" value="+ Agregar Nuevo"
    # onclick="location.href='detail.aspx'"> (navega, no es postback).
    BTN_NUEVO = (By.ID, "btnAddNew")

    # --- Formulario (todo bajo mainTabContainer$pnlDetails) ---
    TXT_NAME = (By.NAME, "ctl00$cph1$mainTabContainer$pnlDetails$txtName$txtValue")
    TXT_CAPACITY = (By.NAME, "ctl00$cph1$mainTabContainer$pnlDetails$txtCapacity$txtValue")
    TXT_ORDER = (By.NAME, "ctl00$cph1$mainTabContainer$pnlDetails$txtDisplayOrder$txtValue")
    DD_CITY = (By.NAME, "ctl00$cph1$mainTabContainer$pnlDetails$ddCity")
    DD_HOTEL = (By.NAME, "ctl00$cph1$mainTabContainer$pnlDetails$ddHotel")
    CB_PUBLICADO = (By.ID, "ctl00_cph1_mainTabContainer_pnlDetails_cbPublicado")

    # --- Editores enriquecidos multi-idioma (pestaña ES = ctl00) ---
    # "Descripción": tiene un "Nombre" por idioma + un editor Quill.
    DESC_NOMBRE_ES = (By.NAME, "ctl00$cph1$mainTabContainer$pnlDetails$ctrlDescriptionQuill$rptrLanguages$ctl00$txtName")
    # El area editable real de Quill es el div.ql-editor dentro del contenedor.
    DESC_QUILL_ES = (By.CSS_SELECTOR, "#ctl00_cph1_mainTabContainer_pnlDetails_ctrlDescriptionQuill_rptrLanguages_ctl00_txtQuill_editor .ql-editor")
    # "Especificaciones": solo editor Quill por idioma.
    ESP_QUILL_ES = (By.CSS_SELECTOR, "#ctl00_cph1_mainTabContainer_pnlDetails_ctrlServicesQuill_rptrLanguages_ctl00_txtQuill_editor .ql-editor")

    # --- Guardar ---
    BTN_GUARDAR = (By.NAME, "ctl00$cph1$mainTabContainer$pnlDetails$btnSave")

    # --- Tabla / validacion ---
    TABLA = (By.CSS_SELECTOR, "table.tablestyle")

    @staticmethod
    def hotel_option(texto):
        # Opcion del select de hoteles que aparece despues del postback de ciudad.
        return (By.XPATH, f"//select[@name='ctl00$cph1$mainTabContainer$pnlDetails$ddHotel']/option[contains(normalize-space(), \"{texto}\")]")

    @staticmethod
    def fila_por_nombre(nombre):
        # El nombre completo (con fecha/hora) aparece tal cual en el <td>; normalize-space
        # tolera el padding/whitespace del HTML de la grilla.
        return (By.XPATH, f"//table[contains(@class,'tablestyle')]//td[contains(normalize-space(), \"{nombre}\")]")
