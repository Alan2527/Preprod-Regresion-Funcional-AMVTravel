"""
Page Object de Colaboradores en el WebAdmin
(Contenidos → Colaboradores, collaborators/default.aspx).

"Nuevo" (`btnAddNew`) navega a collaborators/detail.aspx (TourTabContainer/pnlDetails):
Nombre + Apellido + Puesto + Área + Email + Teléfono + Sucursal (ddBranch) + Publicado.
La firma (imagen) es un panel aparte y OPCIONAL → no se toca.

⚠ La lista NO tiene buscador y pagina (~25/pág) → la validación de la fila es
best-effort (re-navega y busca el sello en la página visible).

Selectores confirmados contra el DOM real (qa.amv.travel).
"""
from selenium.webdriver.common.by import By

_B = "ctl00$cph1$TourTabContainer$pnlDetails$"
_ID = "ctl00_cph1_TourTabContainer_pnlDetails_"


class WebAdminCollaboratorPage:

    MENU_CONTENIDOS = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'javascript:void')]"
        "//span[normalize-space()='Contenidos']")
    SUBMENU = (By.XPATH,
        "//ul[@id='ctl00_ctrlMenu']//a[contains(@href,'/administration/collaborators/default.aspx')]"
        "//span[normalize-space()='Colaboradores']")

    URL_LISTA = "/administration/collaborators/default.aspx"
    URL_DETALLE = "collaborators/detail.aspx"

    BTN_NUEVO = (By.ID, "btnAddNew")

    # ⚠ Estos campos NO llevan sufijo $txtValue (a diferencia de otros forms).
    TXT_NAME = (By.NAME, f"{_B}txtName")
    TXT_LASTNAME = (By.NAME, f"{_B}txtLastName")
    TXT_JOB = (By.NAME, f"{_B}txtJobPosition")
    TXT_AREA = (By.NAME, f"{_B}txtArea")
    TXT_EMAIL = (By.NAME, f"{_B}txtEmail")
    TXT_PHONE = (By.NAME, f"{_B}txtPhone")
    DD_SUCURSAL = (By.NAME, f"{_B}ddBranch")
    CB_PUBLICADO = (By.ID, f"{_ID}cbPublished")
    BTN_GUARDAR = (By.NAME, f"{_B}SaveButton")

    TABLA = (By.ID, "ctl00_cph1_gvCollaborators")

    @staticmethod
    def fila_por_nombre(nombre):
        return (By.XPATH,
            f"//table[@id='ctl00_cph1_gvCollaborators']//td[contains(normalize-space(),\"{nombre}\")]")
