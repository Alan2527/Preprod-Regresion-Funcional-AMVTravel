"""
Page Object compartido del Tarifario (sitio público).

Centraliza los helpers que estaban duplicados en los 7 tests de tarifario:
espera de fin de carga (postback ASP.NET + jQuery), cambio de destino en el
Tom Select, y los buscadores JS de los botones Ver/Cerrar Tarifario + chequeo
de íconos. Los pasos específicos de cada producto quedan en cada test.
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TarifarioPage:
    BTN_BUSCAR = (By.ID, "ctl00_cphMainSlider_ctrlTariffFilterControl_lnkView")

    def __init__(self, driver, timeout=20):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def esperar_fin_de_carga(self):
        """Espera a que terminen loaders, el postback de ASP.NET y jQuery."""
        try:
            self.wait.until(EC.invisibility_of_element_located((
                By.XPATH,
                "//*[contains(translate(text(), 'CARGANDO', 'cargando'), 'cargando') "
                "or contains(@class, 'loading') or contains(@class, 'spinner')]"
            )))
        except Exception:
            pass
        try:
            self.wait.until(lambda d: d.execute_script(
                "return (typeof Sys === 'undefined') || "
                "(typeof Sys.WebForms === 'undefined') || "
                "(Sys.WebForms.PageRequestManager.getInstance().get_isInAsyncPostBack() === false);"
            ))
        except Exception:
            pass
        try:
            self.wait.until(lambda d: d.execute_script(
                "return (typeof jQuery === 'undefined') || (jQuery.active === 0);"
            ))
        except Exception:
            pass
        time.sleep(1)

    def cambiar_destino(self, destino_actual, nuevo_destino):
        """Cambia el destino en el selector custom (Tom Select)."""
        xpath_dropdown = f"//div[contains(@class, 'ts-control') and contains(., '{destino_actual}')]"
        dropdown = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath_dropdown)))
        self.driver.execute_script("arguments[0].click();", dropdown)
        time.sleep(1)

        xpath_opcion = f"//div[contains(@class, 'option') and contains(text(), '{nuevo_destino}')]"
        opcion = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath_opcion)))
        self.driver.execute_script("arguments[0].click();", opcion)
        self.esperar_fin_de_carga()

    def buscar_boton_ver(self):
        """Busca por texto el link 'Ver Tarifario' (robusto ante IDs dinámicos)."""
        return self.wait.until(lambda d: d.execute_script("""
            var links = document.querySelectorAll('a');
            for (var i=0; i<links.length; i++) {
                var text = (links[i].textContent || links[i].innerText || "").toLowerCase();
                if (text.includes('ver tarifario')) { return links[i]; }
            }
            return null;
        """), message="No se encontró el botón 'Ver Tarifario'.")

    def buscar_boton_cerrar(self):
        """Busca por texto el link 'Cerrar Tarifario'."""
        return self.wait.until(lambda d: d.execute_script("""
            var links = document.querySelectorAll('a');
            for (var i=0; i<links.length; i++) {
                var text = (links[i].textContent || links[i].innerText || "").toLowerCase();
                if (text.includes('cerrar tarifario')) { return links[i]; }
            }
            return null;
        """), message="No se encontró el botón 'Cerrar Tarifario'.")

    def check_icono(self, elemento, direccion):
        """True si el elemento contiene un ícono chevron en la dirección indicada."""
        return self.driver.execute_script(
            f"return arguments[0].querySelector('i[class*=\"chevron-{direccion}\"]') !== null;",
            elemento,
        )
