# Regresión Funcional — AMV Travel (Preprod)

Suite de **regresión funcional automatizada** para AMV Travel sobre el entorno de
**preproducción**, construida con **Pytest + Selenium** y reportes en **Allure**.

## 🧱 Stack

- **Pytest** — runner de tests
- **Selenium** — automatización del navegador (Chrome headless)
- **Allure** — reportes con pasos, capturas y diagnósticos

## 📁 Estructura

```
.
├── conftest.py        # Fixtures: driver + login_front / login_bo / login_webadmin
├── helpers.py         # Utilidades: safe_click, safe_send_keys, wait_table_rows
├── pytest.ini         # Configuración, descubrimiento de tests y markers
├── requirements.txt   # Dependencias con versiones fijas
├── bo/                # Tests del BackOffice (preprod.bo.amv.travel)
├── web/               # Tests del sitio público (preprod.amv.travel)
│   ├── inicio/
│   ├── tarifario/
│   └── multidestino/
└── webadmin/          # Tests del panel WebAdmin (/administration/)
```

## 🔐 Variables de entorno (credenciales)

Las credenciales **no** se hardcodean: se leen del entorno (en CI, desde *GitHub Secrets*).

| Variable            | Uso                                  |
|---------------------|--------------------------------------|
| `AMV_USER`          | Usuario (Front, BO y WebAdmin)       |
| `AMV_PASS`          | Contraseña del Front / WebAdmin      |
| `BO_PASS`           | Contraseña del BackOffice            |
| `AMV_AGENCIA_USER`  | Usuario de agencia (login agencia)   |

Ejemplo (PowerShell):

```powershell
$env:AMV_USER = "tu_usuario@amv.travel"
$env:AMV_PASS = "tu_password"
$env:BO_PASS  = "tu_password_bo"
```

## ▶️ Cómo correr los tests

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Correr toda la suite:

```bash
pytest
```

Correr por grupo (markers):

```bash
pytest -m bo          # solo BackOffice
pytest -m front       # solo sitio público
pytest -m webadmin    # solo WebAdmin
```

Correr un archivo o test puntual:

```bash
pytest webadmin/webadmin_login_admin.py
pytest bo/crear_op.py::test_crear_orden_pago
```

## 📊 Ver el reporte de Allure (local)

Requiere tener instalado el [CLI de Allure](https://allurereport.org/docs/install/).

```bash
pytest                         # genera ./allure-results
allure serve allure-results    # abre el reporte en el navegador
```

## 🤖 CI (GitHub Actions)

El workflow `.github/workflows/regresion.yml` corre la suite en cada push a `main`
(o manualmente con *Run workflow*) y publica el reporte de Allure en **GitHub Pages**.

> El comando de ejecución dentro del workflow se ajusta según qué se quiera probar
> (por ejemplo, `pytest -m smoke` o un archivo puntual).

## 🧩 Convenciones

- **Login centralizado:** usá las fixtures `login_front`, `login_bo` o
  `login_webadmin` en vez de reescribir el login en cada test.
- **Interacciones robustas:** usá `safe_click` / `safe_send_keys` de `helpers.py`.
- **Allure:** envolvé cada bloque lógico en `with allure.step(...)` y adjuntá una
  captura por paso (evitá capturas duplicadas del mismo estado).
