"""
Page Object de la creacion de Tipos de Desayuno (breakfast types) en el WebAdmin.
Centraliza la navegacion del menu lateral, los campos del formulario
(nombre + las 4 traducciones por idioma), publicado, guardar y la tabla.
"""

from selenium.webdriver.common.by import By


class WebAdminBreakfastPage:
    # --- Navegacion (menu lateral) ---
    # "Hoteles" es el padre acordeon (href javascript:void(3)); "Desayuno" su submenu.
    MENU_HOTELES = (By.XPATH, "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'javascript:void(3)')]//span[normalize-space()='Hoteles']")
    SUBMENU_DESAYUNO = (By.XPATH, "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'/administration/hotels/breakfasttypes.aspx')]//span[normalize-space()='Desayuno']")

    # Boton "Nuevo".
    BTN_NUEVO = (By.NAME, "ctl00$cph1$btnNew")

    # --- Formulario ---
    TXT_NAME = (By.NAME, "ctl00$cph1$txtName$txtValue")
    CB_PUBLICADO = (By.ID, "ctl00_cph1_cbPublicado")

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
        # El nombre completo (con fecha/hora) aparece tal cual en el <td>; normalize-space
        # tolera el padding/whitespace del HTML de la grilla.
        return (By.XPATH, f"//table[contains(@class,'tablestyle')]//td[contains(normalize-space(), \"{nombre}\")]")
