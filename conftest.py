import os
import sys
import time
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Permite `import helpers` desde cualquier test, sin importar la subcarpeta.
sys.path.insert(0, os.path.dirname(__file__))

FRONT_URL = "https://preprod.amv.travel"
BO_URL = "https://preprod.bo.amv.travel"


# =================================================================
# DRIVER
# =================================================================
@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    drv = webdriver.Chrome(options=options)
    yield drv
    drv.quit()


# =================================================================
# CREDENCIALES
# =================================================================
def _get_credentials(user_var, pass_var, default_user=None, default_pass=None):
    """Lee credenciales del entorno (GitHub Secrets) con fallback opcional."""
    usuario = os.environ.get(user_var, default_user)
    password = os.environ.get(pass_var, default_pass)
    if not usuario or not password:
        pytest.fail(f"Faltan credenciales en el entorno: {user_var} / {pass_var}")
    return usuario, password


# =================================================================
# FIXTURES DE LOGIN
#   Devuelven un `driver` ya autenticado en cada destino, evitando
#   reescribir el login en cada test.
# =================================================================
@pytest.fixture
def login_front(driver):
    """Driver logueado en el sitio público (preprod.amv.travel)."""
    wait = WebDriverWait(driver, 20)
    usuario, password = _get_credentials("AMV_USER", "AMV_PASS")

    with allure.step("Login en el Front (preprod.amv.travel)"):
        driver.get(f"{FRONT_URL}/login.aspx")
        wait.until(EC.visibility_of_element_located((By.ID, "txtUser"))).send_keys(usuario)
        driver.find_element(By.ID, "txtPassword").send_keys(password)
        btn = wait.until(EC.presence_of_element_located((By.ID, "btnLogin")))
        driver.execute_script("arguments[0].click();", btn)
        wait.until(lambda d: "login" not in d.current_url.lower())
        time.sleep(3)

    return driver


@pytest.fixture
def login_bo(driver):
    """Driver logueado en el BackOffice (preprod.bo.amv.travel)."""
    wait = WebDriverWait(driver, 20)
    usuario, password = _get_credentials("AMV_USER", "BO_PASS")

    with allure.step("Login en el BackOffice (preprod.bo.amv.travel)"):
        driver.get(f"{BO_URL}/login")
        wait.until(EC.visibility_of_element_located((By.ID, "txtUser"))).send_keys(usuario)
        driver.find_element(By.ID, "txtPassword").send_keys(password)
        driver.find_element(By.ID, "btnLogin").click()
        wait.until(EC.url_contains("/main"))

    return driver


@pytest.fixture
def login_webadmin(login_front):
    """Driver logueado en el Front y navegado al panel WebAdmin (/administration/)."""
    driver = login_front
    wait = WebDriverWait(driver, 30)

    with allure.step("Navegar al WebAdmin (/administration/)"):
        driver.get(f"{FRONT_URL}/administration/")
        wait.until(EC.url_contains("/administration"))

    return driver


# Alias retrocompatible: tests antiguos que usaban `logged_in_driver`.
@pytest.fixture
def logged_in_driver(login_front):
    return login_front


# =================================================================
# AUTO-MARCADO POR CARPETA
#   Marca cada test según su ubicación: @bo / @front / @webadmin.
#   Permite correr suites selectivas: `pytest -m bo`, `pytest -m front`, etc.
# =================================================================
def pytest_collection_modifyitems(config, items):
    for item in items:
        path = str(item.fspath).replace("\\", "/")
        if "/bo/" in path:
            item.add_marker(pytest.mark.bo)
        elif "/webadmin/" in path:
            item.add_marker(pytest.mark.webadmin)
        elif "/web/" in path:
            item.add_marker(pytest.mark.front)


# =================================================================
# ALLURE ENVIRONMENT
# =================================================================
def pytest_sessionfinish(session, exitstatus):
    """Genera environment.properties para el panel 'Environment' de Allure."""
    allure_dir = "allure-results"
    if not os.path.exists(allure_dir):
        os.makedirs(allure_dir)

    env_file = os.path.join(allure_dir, "environment.properties")
    with open(env_file, "w", encoding="utf-8") as f:
        f.write("Entorno=QA\n")
        f.write("Navegador=Chrome (Headless)\n")
        f.write("URL_Frontend=https://preprod.amv.travel/\n")
        f.write("Framework=Pytest+Selenium\n")
