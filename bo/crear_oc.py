import pytest
import allure
import time
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from helpers import safe_click, safe_send_keys, wait_table_rows
from pages.bo_chargeorder_page import BoChargeOrderPage as P


# =========================
# TEST
# =========================

@allure.feature("Tesorería BackOffice")
@allure.story("Crear Orden de Cobro")
@allure.severity(allure.severity_level.CRITICAL)
def test_crear_orden_cobro(login_bo):
    driver = login_bo

    wait = WebDriverWait(driver, 25)

    # ==========================================
    # 2. NAVEGACIÓN
    # ==========================================
    with allure.step("2. Navegación"):
        safe_click(wait, P.MENU)
        safe_click(wait, P.SUBMENU)

        allure.attach(driver.get_screenshot_as_png(), "2_Navegacion", allure.attachment_type.PNG)

    # ==========================================
    # 3. NUEVO
    # ==========================================
    with allure.step("3. Nuevo"):
        safe_click(wait, P.LINK_NUEVO)
        allure.attach(driver.get_screenshot_as_png(), "3_Nuevo", allure.attachment_type.PNG)

    # ==========================================
    # 4. PAYMENT REF
    # ==========================================
    with allure.step("4. PaymentRef"):
        Select(wait.until(EC.element_to_be_clickable(P.DD_PAYMENT_REFS)))\
            .select_by_visible_text("01C - TRANSFERENCIA CLIENTE DEL EXTERIOR 000001")

        allure.attach(driver.get_screenshot_as_png(), "4_PaymentRef", allure.attachment_type.PNG)

    # ==========================================
    # 5. CURRENCY
    # ==========================================
    with allure.step("5. Currency"):
        Select(wait.until(EC.element_to_be_clickable(P.DD_CURRENCY)))\
            .select_by_visible_text("USD")

        allure.attach(driver.get_screenshot_as_png(), "5_Currency", allure.attachment_type.PNG)

    # ==========================================
    # 6. ABRIR MODAL
    # ==========================================
    with allure.step("6. Abrir modal cliente"):
        safe_click(wait, P.TXT_CUSTOMER)

        try:
            safe_click(wait, P.ICON_MAGNIFIER)
        except:
            pass

        allure.attach(driver.get_screenshot_as_png(), "6_Modal", allure.attachment_type.PNG)

    # ==========================================
    # 7. BUSCAR
    # ==========================================
    with allure.step("7. Buscar cliente"):
        search = wait.until(EC.visibility_of_element_located(P.INPUT_SEARCH))
        search.clear()
        search.send_keys("hectours")

        allure.attach(driver.get_screenshot_as_png(), "7_Busqueda", allure.attachment_type.PNG)

    # ==========================================
    # 8. SELECCIONAR CLIENTE
    # ==========================================
    with allure.step("8. Seleccionar cliente"):
        wait_table_rows(wait, P.DATA_CUSTOMERS_SELECTOR)

        fila = wait.until(EC.element_to_be_clickable(P.FILA_CLIENTE))

        driver.execute_script("arguments[0].click();", fila)

        # 🔥 esperar que cierre el modal
        wait.until(EC.invisibility_of_element_located(P.DATA_CUSTOMERS))

        allure.attach(driver.get_screenshot_as_png(), "8_Cliente", allure.attachment_type.PNG)

    # ==========================================
    # 9. CAJA
    # ==========================================
    with allure.step("9. Caja"):
        Select(wait.until(EC.element_to_be_clickable(P.DD_CASHFLOW)))\
            .select_by_visible_text("CAJA CHICA U$D")

        allure.attach(driver.get_screenshot_as_png(), "9_Caja", allure.attachment_type.PNG)

    # ==========================================
    # 10. DETALLE
    # ==========================================
    with allure.step("10. Detalle"):
        safe_send_keys(wait, P.TXT_DETAIL, "Test automático")

        allure.attach(driver.get_screenshot_as_png(), "10_Detalle", allure.attachment_type.PNG)

    # ==========================================
    # 11. MONTO
    # ==========================================
    with allure.step("11. Monto"):
        safe_send_keys(wait, P.TXT_AMOUNT, "9000")

        allure.attach(driver.get_screenshot_as_png(), "11_Monto", allure.attachment_type.PNG)

    # ==========================================
    # 12. GUARDAR
    # ==========================================
    with allure.step("12. Guardar"):
        safe_click(wait, P.BTN_SAVE)
        time.sleep(3)

        allure.attach(driver.get_screenshot_as_png(), "12_Guardado", allure.attachment_type.PNG)

    # ==========================================
    # 13. SCROLL A TABLA
    # ==========================================
    with allure.step("13. Scroll a tabla imputación"):

        tabla = wait.until(EC.presence_of_element_located(P.TBL_ALLOCATION))

        driver.execute_script("arguments[0].scrollIntoView(true);", tabla)
        time.sleep(2)

        allure.attach(driver.get_screenshot_as_png(), "13_Scroll", allure.attachment_type.PNG)

    # ==========================================
    # 14. CLICK IMPUTAR (ROBUSTO PRO)
    # ==========================================
    with allure.step("14. Click imputar (multi-strategy)"):

        clicked = False

        # 🔹 1. Intentar por ID dinámico
        try:
            boton = wait.until(EC.presence_of_element_located(P.IMPUTAR_LINK))
            driver.execute_script("arguments[0].click();", boton)
            clicked = True
        except:
            pass

        # 🔹 2. Fallback: icono interno
        if not clicked:
            try:
                icono = wait.until(EC.presence_of_element_located(P.IMPUTAR_ICONO))
                driver.execute_script("arguments[0].click();", icono)
                clicked = True
            except:
                pass

        # 🔹 3. Fallback PRO: ejecutar postback directo
        if not clicked:
            try:
                boton = wait.until(EC.presence_of_element_located(P.IMPUTAR_POSTBACK))

                href = boton.get_attribute("href")

                # ejecutar el postback manualmente
                driver.execute_script(href)
                clicked = True
            except:
                pass

        if not clicked:
            allure.attach(driver.get_screenshot_as_png(), "ERROR_IMPUTAR", allure.attachment_type.PNG)
            pytest.fail("No se pudo hacer click en imputar")

        # En vez de un sleep fijo, esperamos a que el postback rinda la grilla interna.
        wait.until(EC.presence_of_element_located(P.TABLA_INTERNA))

        allure.attach(driver.get_screenshot_as_png(), "14_Click_Imputar", allure.attachment_type.PNG)

    # ==========================================
    # 15. VALIDAR TABLA INTERNA
    # ==========================================
    with allure.step("15. Validar tabla interna"):

        tabla_interna = wait.until(EC.presence_of_element_located(P.TABLA_INTERNA))

        wait.until(EC.presence_of_element_located(P.CELDA_TABLA_INTERNA))

        allure.attach(driver.get_screenshot_as_png(), "15_Tabla_Interna", allure.attachment_type.PNG)

    # ==========================================
    # 16. INGRESAR FECHA HOY
    # ==========================================
    with allure.step("16. Ingresar fecha actual"):

        fecha_hoy = datetime.now().strftime("%d/%m/%Y")

        safe_send_keys(wait, P.TXT_RECEIPT_DATE, fecha_hoy)

        allure.attach(driver.get_screenshot_as_png(), "16_Fecha", allure.attachment_type.PNG)

    # ==========================================
    # 17. APROBAR Y APLICAR
    # ==========================================
    with allure.step("17. Aprobar y aplicar recibo"):

        boton_aprobar = wait.until(EC.presence_of_element_located(P.BTN_APROBAR))

        driver.execute_script("arguments[0].click();", boton_aprobar)

        # En vez de un sleep fijo, esperamos a que el botón desaparezca (fin del proceso).
        wait.until(EC.invisibility_of_element_located(P.BTN_APROBAR))

        allure.attach(driver.get_screenshot_as_png(), "17_Click_Aprobar", allure.attachment_type.PNG)

    # ==========================================
    # 18. VALIDAR QUE DESAPARECIÓ
    # ==========================================
    with allure.step("18. Validar botón desapareció"):

        wait.until(EC.invisibility_of_element_located(P.BTN_APROBAR))

        allure.attach(driver.get_screenshot_as_png(), "18_Final", allure.attachment_type.PNG)
