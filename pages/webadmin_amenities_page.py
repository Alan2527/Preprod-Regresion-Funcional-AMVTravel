"""
Page Object de la creacion de Amenities en el WebAdmin.
Centraliza la navegacion del menu lateral, los campos del formulario (nombre +
las 4 traducciones por idioma), el boton de guardar y la tabla de amenities.
"""

from selenium.webdriver.common.by import By


class WebAdminAmenitiesPage:
    # --- Navegacion (menu lateral) ---
    # "Hoteles" es el padre acordeon (href javascript:void(3)); "Amenities" su submenu.
    MENU_HOTELES = (By.XPATH, "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'javascript:void(3)')]//span[normalize-space()='Hoteles']")
    SUBMENU_AMENITIES = (By.XPATH, "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'/administration/types/amenities.aspx')]//span[normalize-space()='Amenities']")

    # Boton "Nuevo" (vive en el contenedor de acciones del header: cphActions).
    BTN_NUEVO = (By.ID, "ctl00_cphActions_btnNew")

    # --- Formulario ---
    TXT_NAME = (By.NAME, "ctl00$cph1$txtName$txtValue")

    # Traducciones por idioma: ctrl0=Espanol, ctrl1=English, ctrl2=Portuguese, ctrl3=Italian.
    @staticmethod
    def traduccion(indice):
        return (By.NAME, f"ctl00$cph1$lvTranslations$ctrl{indice}$txtLocName$txtValue")

    # --- Guardar ---
    BTN_GUARDAR = (By.NAME, "ctl00$cph1$btnSave")

    # --- Tabla / validacion ---
    TABLA = (By.CSS_SELECTOR, "table.tablestyle")

    @staticmethod
    def fila_por_nombre(nombre):
        # El nombre completo (con fecha/hora) aparece tal cual en el <td>; usamos
        # normalize-space para tolerar el padding/whitespace del HTML de la grilla.
        return (By.XPATH, f"//table[contains(@class,'tablestyle')]//td[contains(normalize-space(), \"{nombre}\")]")
