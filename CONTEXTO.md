# 🧭 CONTEXTO del proyecto — Preprod Regresión Funcional AMV Travel

> Documento vivo para retomar contexto en futuras conversaciones (con IA o el equipo).
> Última actualización: 2026-06-05.

---

## 1. Qué es esto

Suite de **regresión funcional automatizada** para **AMV Travel** sobre el entorno de
**preproducción**, hecha con **Pytest + Selenium** y reportes en **Allure**
(publicados en GitHub Pages).

- **Repo GitHub:** https://github.com/Alan2527/Preprod-Regresion-Funcional-AMVTravel
- **Carpeta local:** `C:\Users\alanh\Desktop\Preprod-Regresion-Funcional-AMVTravel-main`
- **Reporte Allure (GitHub Pages):** `https://alan2527.github.io/Preprod-Regresion-Funcional-AMVTravel/`
- **Versiones:** `pytest==9.0.3`, `selenium==4.44.0`, `allure-pytest==2.16.0` (Python 3.10)

### Entornos que se testean
- **Front (sitio público):** `https://preprod.amv.travel`
- **BackOffice (BO):** `https://preprod.bo.amv.travel`
- **WebAdmin (panel admin):** `https://preprod.amv.travel/administration/`

---

## 2. Estructura del repo

```
.
├── conftest.py            # Fixtures: driver + login_front / login_bo / login_webadmin
│                          #   + auto-marcado por carpeta + Allure environment
├── helpers.py             # safe_click, safe_send_keys, wait_table_rows
├── pytest.ini             # Config, descubrimiento (python_files=*.py), markers, addopts Allure
├── requirements.txt       # Versiones fijas
├── README.md              # Documentación de uso
├── CONTEXTO.md            # ESTE archivo
├── .gitignore
├── .github/workflows/
│   └── regresion.yml      # CI parametrizable (input "target") + cache + artifact + GitHub Pages
├── examples/
│   └── web.py             # Ejemplo histórico (fuera de la suite, excluido en norecursedirs)
├── pages/                 # PAGE OBJECTS (selectores centralizados)
│   ├── webadmin_home_page.py        # WebAdminHomePage
│   ├── webadmin_hotel_page.py       # WebAdminHotelPage
│   ├── webadmin_room_page.py        # WebAdminRoomPage
│   ├── bo_booking_inbox_page.py     # BoBookingInboxPage
│   ├── bo_payorder_page.py          # BoPayOrderPage (crear_op)
│   ├── bo_chargeorder_page.py       # BoChargeOrderPage (crear_oc)
│   ├── front_ofertas_page.py        # FrontOfertasPage
│   ├── front_hoteles_page.py        # FrontHotelesPage
│   ├── front_servicios_page.py      # FrontServiciosPage
│   ├── multidestino_page.py         # MultidestinoPage (+ helper esperar_fin_de_carga)
│   ├── tarifario_page.py            # TarifarioPage (COMPARTIDO por los 7 tests de tarifario)
│   ├── webadmin_amenities_page.py   # WebAdminAmenitiesPage
│   ├── webadmin_roomtype_page.py    # WebAdminRoomTypePage
│   ├── webadmin_category_page.py    # WebAdminCategoryPage
│   ├── webadmin_breakfast_page.py   # WebAdminBreakfastPage
│   └── webadmin_salon_page.py       # WebAdminSalonPage
├── bo/                    # Tests BackOffice
│   ├── bo_login_admin.py · login_noadmin.py   (tests de login, NO usan fixture de login)
│   ├── crear_op.py · crear_oc.py · generar_file.py
│   └── cotizaciones.py · reservas.py
├── web/
│   ├── inicio/            # login_admin, login_agencia (login tests), hoteles, ofertas, servicios
│   ├── tarifario/         # t_hoteles, t_ofertas, cruceros, excursiones, paquetes, traslados, cenashow
│   └── multidestino/      # multidestino
└── webadmin/
    ├── webadmin_login_admin.py
    ├── crear_hotel.py
    ├── crear_habitacion.py
    ├── crear_amenities.py
    ├── crear_tipos_de_habitacion.py
    ├── crear_categoria.py
    ├── crear_desayuno.py
    └── crear_salon.py
```

---

## 3. Convenciones (IMPORTANTE seguirlas)

- **Login centralizado por fixtures** (en `conftest.py`):
  - `login_front` → logueado en el Front.
  - `login_bo` → logueado en el BackOffice.
  - `login_webadmin` → logueado en Front y navegado a `/administration/`.
  - `logged_in_driver` → alias de `login_front` (compatibilidad con tests viejos del front).
  - Los **tests de login** (bo_login_admin, login_noadmin, web/inicio/login_*) **NO** usan
    estas fixtures (su propósito ES testear el login).
- **Helpers robustos** (`helpers.py`): usar `safe_click` / `safe_send_keys` en vez de
  click/send_keys crudos.
- **Page Objects**: los selectores van en `pages/`, NO inline en el test. El test orquesta
  y usa `P.LOCATOR` + métodos.
- **Credenciales por variables de entorno** (nunca hardcodeadas):
  | Variable | Uso |
  |---|---|
  | `AMV_USER` | Usuario (Front, BO y WebAdmin) |
  | `AMV_PASS` | Password Front/WebAdmin |
  | `BO_PASS` | Password BackOffice |
  | `AMV_AGENCIA_USER` | Usuario de agencia |
  - En CI vienen de **GitHub Secrets**. Localmente, `login_front`/webadmin tienen fallback
    a `Pablo@amv.travel` / `amvtest123` (solo para correr local).
- **Allure**: cada bloque lógico en `with allure.step(...)`. Evitar capturas duplicadas del
  mismo estado (preferir 1 captura representativa por paso).
- **Markers** (auto-asignados por carpeta vía hook en conftest): `front`, `bo`, `webadmin`.
  Hay además `smoke` registrado (sin usar aún).

---

## 4. Cómo correr

```bash
pip install -r requirements.txt

pytest                       # toda la suite
pytest -m bo                 # solo BackOffice
pytest -m front              # solo Front
pytest -m webadmin           # solo WebAdmin
pytest webadmin/crear_hotel.py::test_crear_hotel   # un test puntual

allure serve allure-results  # ver reporte local (requiere CLI de Allure)
```

### CI (GitHub Actions) — parametrizable
- Workflow: `.github/workflows/regresion.yml`. Corre en **push a main** y con **Run workflow**.
- Campo **`target`** en *Run workflow* (o el default en push) define qué corre:
  `webadmin/crear_hotel.py` · `-m bo` · `-m webadmin` · `bo/ web/` · etc.
- **Default actual del target:** `webadmin/` → **corre solo los tests de webadmin** (pedido de Alan).
  `default: 'webadmin/'` y `TARGET: ${{ github.event.inputs.target || 'webadmin/' }}`.
  Para la suite completa, poner `bo/ web/ webadmin/` en el input `target` del "Run workflow".
- Publica el reporte Allure en GitHub Pages y deja `allure-results` como artifact.
- ⚠️ El que ajusta el `target`/CI es **Alan** (manual cada vez que quiere probar algo),
  salvo que se pida cambiarlo.

---

## 5. Estado actual (qué está hecho)

### Infraestructura / calidad (✅ hecho)
- Centralización de login (fixtures) y helpers.
- `pytest.ini` con descubrimiento de archivos de nombre descriptivo + markers + Allure.
- README, .gitignore, requirements fijados, `web.py` movido a `examples/`.
- CI parametrizable con cache de pip y artifact.
- **Page Objects en las 3 capas** (Front, BO, WebAdmin) — toda la suite migrada a POM.
- Tarifario: `TarifarioPage` compartido por los 7 tests (gran reducción de duplicación).
- Migración conservadora de algunos `time.sleep` redundantes a esperas explícitas en BO.

### ⚠️ Rediseño del WebAdmin ("Climbs") — junio 2026
El preprod cambió de branding (la agencia ahora se llama **"Climbs"**, antes "AMV. TRAVEL")
y rediseñó las pantallas. Impactos en los tests (todos corregidos en local, pendientes de subir):
- `webadmin_login_admin.py`: la aserción de agencia ahora espera **"CLIMBS"**.
- Botones "Nuevo" de las listas, ahora con ids variados por pantalla:
  - Tipos de habitación: `id="btnAddNew"` · Desayuno: `name="ctl00$cphActions$btnNew"` ·
    Categorías: `name="ctl00$cphActions$btnAddNew"` · Salones: `id="btnAddNew"`.
- Submenú de Habitaciones: el `<span>` ahora dice **"Habitaciones"** (antes "Adm. de Habitaciones").
- Campos que pasaron a estar **ocultos** (`display:none`, los maneja el code-behind):
  - Hotel: `txtEmailNoti` (Emails Notif.) y `cbForResidents`/`cbForNonResidents` →
    se quitaron del flujo (el `safe_send_keys` sobre un campo oculto hacía Timeout 45s).
  - Habitación: `cbForResidents`/`cbForNonResidents` ocultos → solo se tilda Publicado.
- Nombres de pestañas del detalle cambiaron:
  - Hotel: la pestaña es **"Amenities"** (no "Servicios"); "Videos" (no "Video").
  - Habitación: pestañas reales **Detalle | Tarifas | Tarifario | Detalle del tarifario | Freesale**
    (antes el test esperaba "Tarifas & Freesale", que ya no existe).
- Barrio (distrito) del hotel: depende de la ciudad por postback y es **opcional**; el test
  ahora elige el primer barrio real si existe, o lo omite (Cachi puede no tener barrios).

### Tests WebAdmin (foco actual)
- `webadmin_login_admin.py` → fix "Climbs" aplicado (pendiente subir + corrida verde).
- `crear_hotel.py` → crea hotel y valida (info general, config, ubicación, descripción Quill,
  guardado con id dinámico, pestañas habilitadas, aparición en tabla).
  **Fix rediseño aplicado** (email_noti/checkboxes ocultos, pestaña Amenities, barrio opcional).
- `crear_habitacion.py` → **fix rediseño aplicado** (submenú "Habitaciones", pestaña "Tarifas",
  solo Publicado). Pendiente subir + confirmar corrida verde.
  - Pasos 14-15 (edades de menores `dpKidsFrom`/`dpKidsTo`) **comentados**: están rotos en la app.
- `crear_amenities.py` → **recién creado**, pendiente primera corrida verde.
  - Flujo: Menú Hoteles → Amenities → Nuevo → nombre dinámico (con fecha/hora) +
    4 traducciones requeridas (ES/EN/PT/IT) → Guardar → validar fila en `gvAmenities`.
  - Page Object: `WebAdminAmenitiesPage` (`traduccion(indice)` para ctrl0..ctrl3).
  - Validado estáticamente (`py_compile`, `--collect-only`, `--setup-plan`).
- `crear_tipos_de_habitacion.py` → **recién creado**, pendiente primera corrida verde.
  - Flujo: Menú Hoteles → Tipos de habitación → Nuevo → nombre dinámico + detalle →
    dejar Publicado tildado → Guardar → validar fila en la tabla.
  - Page Object: `WebAdminRoomTypePage`.
  - Validado estáticamente (`py_compile`, `--collect-only`, `--setup-plan`).
- `crear_categoria.py` → **recién creado**, pendiente primera corrida verde.
  - Flujo: Menú Hoteles → Categorías → Nuevo → nombre dinámico + orden (1) +
    4 traducciones (ES/EN/PT/IT) → Guardar → validar fila en la tabla.
  - Page Object: `WebAdminCategoryPage` (`traduccion(indice)` para ctrl0..ctrl3).
  - Validado estáticamente (`py_compile`, `--collect-only`, `--setup-plan`).
- `crear_desayuno.py` → **recién creado**, pendiente primera corrida verde.
  - Flujo: Menú Hoteles → Desayuno → Nuevo → nombre dinámico + 4 traducciones (ES/EN/PT/IT) +
    Publicado tildado → Guardar → validar fila en la tabla `gvTypes`.
  - Page Object: `WebAdminBreakfastPage` (`traduccion(indice)` para ctrl0..ctrl3).
  - Form modelado sobre Amenities (el __VIEWSTATE confirma `lvTranslations`); el HTML del
    form en sí no estaba disponible al crearlo.
  - Validado estáticamente (`py_compile`, `--collect-only`, `--setup-plan`).
- `crear_salon.py` → **recién creado**, pendiente primera corrida verde.
  - Flujo: Menú Hoteles → Salones → Nuevo → **elegir Ciudad (postback que recarga Hoteles)**
    → nombre dinámico + capacidad 200 + orden → elegir Hotel dependiente → Publicado →
    Guardar → validar fila en la tabla.
  - Page Object: `WebAdminSalonPage` (campos bajo `mainTabContainer$pnlDetails`; helper
    `hotel_option(texto)` para esperar el hotel tras el postback de ciudad).
  - Datos de prueba: Ciudad `Cachi | Argentina`, Hotel `Hosteria Cachi`.
  - Gotcha aplicado: el `ddCity` dispara postback full (onchange) → se elige ciudad
    primero y se espera a que aparezca el hotel dependiente antes de seguir.
  - Botón Nuevo de la lista: `id="btnAddNew"` (input button que hace location.href a
    detail.aspx). La grilla de la lista es `gvData`.
  - ⚠️ Salones tiene **lista y detalle separados**: al Guardar queda en `detail.aspx`
    (sin tabla), NO redirige a la lista. Hay que volver a Salones para validar la fila.
    (A diferencia de Amenities/Categoría/etc. que son lista+form en la misma página.)
  - ⚠️ Para volver: en `detail.aspx` el menú "Hoteles" ya está ABIERTO, así que se
    clickea **directo el span "Salones"** (NO el padre `MENU_HOTELES`, que colapsaría el
    acordeón y ocultaría el submenú). Luego se espera la URL de la lista
    (`/administration/meetingsalons/` y que NO contenga `detail.aspx`).
  - La validación de la fila usa el **sello de fecha/hora (ASCII)** y no el nombre con
    acentos, para evitar problemas de normalización Unicode en el match del `<td>`.
  - Completa también los editores **Quill** (Descripción + Especificaciones, pestaña ES)
    y el "Nombre" localizado de Descripción. Quill es un `div.ql-editor` contenteditable
    (no input): se escribe con `_escribir_quill` (click + send_keys), no con safe_send_keys.
  - Validado estáticamente (`py_compile`, `--collect-only`, `--setup-plan`).
  - El YML quedó apuntando a este test (ver sección CI).

---

## 6. Gotchas / aprendizajes (LEER antes de tocar WebAdmin)

1. **Buscador del WebAdmin y los `:` (dos puntos):** buscar por un nombre que incluye hora
   (`HH:MM:SS`) **devuelve 0 resultados** (parece tokenizar por `:`). Con 0 resultados, la
   GridView de ASP.NET **no renderiza** la `<table class="tablestyle">` → cualquier wait por
   la tabla hace timeout.
   - **Solución usada:** buscar por el nombre **sin la hora** (solo hasta la fecha) y luego
     validar la **fila exacta** por el nombre completo (que sí aparece en el `<td>`).

2. **Grilla envuelta por JS (`initGridScrollContainers`):** el panel envuelve cada
   `table.tablestyle` en un `div.grid-scroll-container` con overflow. Por eso
   `visibility_of_element_located` sobre la tabla puede dar **falso negativo**.
   - **Solución:** usar `presence_of_element_located` (no visibility) para tablas/filas.

3. **Postbacks de ASP.NET (WebForms):** muchos selects disparan postback (ej. ciudad→barrio,
   hotel→tipos). Conviene un pequeño `time.sleep(1)` o esperar el elemento dependiente.
   Hay un overlay global `#globalLoadingOverlay` durante la carga.

4. **Menú lateral acordeón:** al hacer click en el `<span>Hoteles</span>` padre se expande/colapsa
   el submenú (animación). Después del click al padre, esperar y clickear el submenú
   (`Adm. de Hoteles` / `Adm. de Habitaciones`). Locators de menú scoping a `ul#ctl00_ctrlMenu`.

5. **Pestañas (AjaxControlToolkit TabContainer):** validar con **match exacto**
   (`normalize-space()='...'`) y scope al contenedor (`HotelTabContainer` / `RoomTabContainer`)
   para no confundir, p.ej., "Tarifario" con "Detalle del tarifario".

6. **Editor de descripción = Quill:** el contenido va en `div.ql-editor` (contenteditable);
   se escribe con `send_keys` sobre ese div (no es un input/textarea normal).

7. **Migración masiva de `time.sleep`:** NO hacerla a ciegas. La mayoría son esperas
   intencionales de animaciones JS / postbacks sin condición DOM limpia. Migrar solo cuando
   haya una corrida verde en CI como red de seguridad.

8. **No se puede ejecutar contra preprod desde el entorno de la IA.** Todo se valida de forma
   **estática** (`py_compile`, `pytest --collect-only`, `pytest --setup-plan`). La confirmación
   real es la corrida en GitHub Actions.

---

- `crear_servicio.py` → **recién creado** (2026-06-10), pendiente primera corrida verde.
  - Flujo: Menú Servicios → Adm. de servicios → Crear servicio → formulario completo →
    Guardar → validar pestañas habilitadas → volver a lista → validar fila en tabla.
  - Datos: Tipo=Excursión, Ciudad=Cachi, Orden=2, Publicado, vidriera, Idioma ES+EN,
    Tags=Test, Opcional Regular+Privado, Edad 1-17, Gratis hasta 4, Cancelable, Horas 24.
  - 6 editores Quill rellenados (ES): Intro, Detalle, Nombre y Desc, Política, Encuentro, Destino.
  - Page Object: `WebAdminServicioPage`. Container `ServiciosTabContainer/pnlServicioDetails`.
  - Idioma y Tags usan TomSelect → helper `_tomselect_add` (JS API `ts.addItem`).
  - Validación de pestañas: CSS `.ajax__tab_disabled` dentro del contenedor → debe ser 0.
  - ✅ Campos **confirmados contra el DOM real** (2026-06-11, vía inspección del detail.aspx):
    los names inferidos estaban mal. Correcciones aplicadas en `WebAdminServicioPage`:
    | Inferido (rompía) | Real | Campo |
    |---|---|---|
    | `txtAgeFrom` | `txtKidsFrom` | Edad desde |
    | `txtAgeTo` | `txtKidsTo` | Edad hasta |
    | `txtFreeAge` | `txtKidsFreeTo` | Gratis hasta |
    | `cbCancelable` | `cbCancellable` | Cancelable (doble L) |
    | `txtHorasAntes` | `txtCancellableUpTo` | Horas antes |
    | `ctrlDestinationPointQuill` | `ctrlDropOffQuill` | Quill Punto de Destino |
    El que tiraba el TimeoutException era `txtAgeFrom` (step 16-20); `ctrlDropOffQuill`
    habría roto el step 21-26 después. `ctrlNameDescQuill$...$txtName` SÍ existe (OK).
  - Validado estáticamente (`py_compile`, `--collect-only`).

- `crear_tag.py` → **recién creado** (2026-06-18), pendiente primera corrida verde.
  - Flujo: Menú Servicios → Tags → "Nuevo" (abre modal) → nombre dinámico → Guardar →
    buscar y validar la fila en la tabla.
  - Page Object: `WebAdminTagPage`. Selectores confirmados contra el HTML real (qa.amv.travel,
    mismos IDs ASP.NET que preprod).
  - ⚠ El botón "Nuevo" (`id="btnAddNew"`) abre un **modal** (ModalPopupExtender vía
    `openModalExtension()`); el form está en `#ctl00_cph1_pnlPopup`. Input nombre
    `ctl00_cph1_txtName`, Guardar `ctl00_cph1_btnNewTag` (submit→postback).
  - Buscador `ctl00_cph1_txtSearch` + `ctl00_cph1_btnSearch`; tabla `ctl00_cph1_gvData`.
    La fila muestra el nombre con sufijo " #<id>" (ej: "...15:57:35 #7").
  - Validación: gotcha #1 (buscar por nombre SIN la hora) + validar fila por el sello.
  - El YML quedó apuntando a este test (default `webadmin/crear_tag.py`).
  - Validado estáticamente (`py_compile`, `--collect-only`).
  - ✅ **Corrida verde confirmada** (2026-06-18).

- `crear_tipo_servicio.py` → **recién creado** (2026-06-18), pendiente primera corrida verde.
  - Flujo: Menú Servicios → Tipos de servicio → "Nuevo" (form INLINE, no modal) →
    nombre dinámico + 4 traducciones (ES/EN/PT/IT) + orden + Publicado → Guardar →
    buscar y validar la fila en la tabla.
  - Page Object: `WebAdminTipoServicioPage` (servicetypes.aspx). Selectores confirmados
    contra el HTML real.
  - ⚠ Botón Nuevo = `ctl00$cphActions$btnNew` (es `btnNew`, NO `btnAddNew` como categoría).
  - Campos: `txtName$txtValue`, `lvTranslations$ctrl0..3$txtLocName$txtValue` (igual que
    categoría), `txtOrden$txtValue`, `cbPublicado`, `btnSave`. Tabla `gvServiceTypes`.
  - ⚠ `cbIsAdditional` ("Es servicio adicional") NO se toca: al tildarlo dispara un popup
    de confirmación (mpeIsAdditional). Se deja OFF.
  - Validación: gotcha #1 (buscar por nombre SIN la hora) + validar fila por el sello.
  - El YML quedó apuntando a este test (default `webadmin/crear_tipo_servicio.py`).
  - ⚠ El nombre se trunca server-side a ~50 chars → prefijo CORTO ("Tipo Servicio Test")
    + sello completo (fecha+hora de corrida). Total <50 o se comen los segundos.
  - Validado estáticamente (`py_compile`, `--collect-only`).

- `crear_vehiculo.py` → **recién creado** (2026-06-18), pendiente primera corrida verde.
  - Flujo: Menú Servicios → Vehículos → "Nuevo" (form INLINE) → nombre dinámico +
    4 traducciones (ES/EN/PT/IT) + Capacity From/To + Publicado → Guardar →
    buscar y validar la fila en la tabla.
  - Page Object: `WebAdminVehiculoPage` (vehicletypes/default.aspx). Idéntico a Tipos de
    servicio pero con `txtCapacityFrom$txtValue` / `txtCapacityTo$txtValue` en vez de orden.
  - Nuevo `cphActions$btnNew`, `txtName$txtValue`, `lvTranslations$ctrl0..3`, `cbPublicado`,
    `btnSave`. Tabla `gvTypes`. Selectores confirmados contra HTML real.
  - Nombre: prefijo corto "Vehiculo Test" + sello (regla del truncado a ~50).
  - El YML quedó apuntando a este test (default `webadmin/crear_vehiculo.py`).
  - Validado estáticamente (`py_compile`, `--collect-only`).

- `crear_caracteristicas.py` → **recién creado** (2026-06-18), pendiente primera corrida verde.
  - Flujo: Menú Servicios → Caracteristicas → "Nuevo" (form INLINE) → Nombre (4 idiomas) +
    Detalle (4 idiomas) + Orden + Publicado → Guardar → buscar y validar fila.
  - Page Object: `WebAdminCaracteristicaPage` (charasteristicsadmin.aspx).
  - ⚠ Nombre y Detalle son MULTI-IDIOMA: `lvNameTranslations$ctrl0..3$txtName$txtValue`
    (inputs) y `lvDetailTranslations$ctrl0..3$txtDetail$txtValue` (textareas). No hay un
    txtName único. Orden `txtOrden$txtValue`, `cbPublicado`, `btnSave`. Tabla `gvCharasteristics`.
  - Nombre ES = "Caract Test" + sello; resto idiomas = "test". Validación por sello.

- `crear_comodidades.py` → **recién creado** (2026-06-18), pendiente primera corrida verde.
  - Flujo: Menú Servicios → Comodidades → "Nuevo" (form INLINE) → nombre dinámico +
    4 traducciones (ES/EN/PT/IT) + Publicado → Guardar → buscar y validar fila.
  - Page Object: `WebAdminComodidadPage` (types/serviceamenities.aspx). Nombre único
    `txtName$txtValue` + `lvTranslations$ctrl0..3$txtLocName$txtValue` + `cbPublicado` +
    `btnSave`. Tabla `gvServiceAmenities`. Sin orden.
  - Nombre: "Comodidad Test" + sello. Lista ordenada alfabéticamente y paginada → la
    búsqueda es necesaria (gotcha #1).
  - Validado estáticamente (`py_compile`, `--collect-only`).
  - ⚠ El buscador de esta pantalla daba 0 resultados tras el postback de guardado →
    la validación re-navega a la lista fresca y busca la fila por sello (orden=1 → 1ª pág).
  - `crear_comodidades` quedó **verde**; `crear_caracteristicas` pendiente de confirmar el fix.

- `crear_servicio_incentivo.py` → **recién creado** (2026-06-18), pendiente primera corrida verde.
  - Flujo: Menú Servicios → Servicios de incentivo → "+ Agregar Servicio" (va a
    servicedetail.aspx, PÁGINA APARTE) → Nombre + Ciudad (Cachi) + Servicio Relacionado
    (Experiencia Colomé, dep. de ciudad por postback) + Tipo (Excursión) + Destino
    (Buenos Aires) + Orden + Destacado + Publicado + Detalle ES (Nombre + Quill) →
    Guardar → validar fila en la lista (re-navegando, la lista NO tiene buscador).
  - Page Object: `WebAdminServicioIncentivoPage`. Campos bajo
    `tabsIncentiveService$pnlDetails$`: `txtName`, `ddlCity`, `ddlService`, `ddlServiceType`,
    `ddlDestination`, `txtDisplayOrder$txtValue`, `chkGreat` (Destacado), `cbPublished`,
    `ctrlIncentiveDetailQuill$rptrLanguages$ctl00$txtName` + Quill ES, `btnSave`.
    Lista `gvIncentiveService`, botón "+ Agregar Servicio" (location.href a servicedetail.aspx).
  - Validado estáticamente (`py_compile`, `--collect-only`).

---

## 6.bis Tests de Circuitos (2026-06-18, recién creados)

- **Paquete / Oportunidad / Travel Sale** comparten estructura (grid `gvReceptiveTours`,
  form `TourTabContainer/pnlDetails`). Page Object compartido `WebAdminTourPage` con
  helpers `llenar_tour`, `escribir_quill`, `validar_solapas`. Listas:
  receptivetours/ · opportunities/ · travelsale/. Buscador `txtSearch`/`btnSearch`.
  - `crear_paquete.py` → solapas validadas: Detalle, Imagenes, Videos, Destinos.
  - `crear_oportunidad.py` → Detalle, Imagenes, Destinos, **Agencias** (⚠ NO tiene Videos).
  - `crear_travel_sale.py` → Detalle, Imagenes, Videos, Destinos.
  - Campos requeridos del form: txtName, txtMarkup, txtTotalRate, txtExtraRate,
    txtRateMin, txtNights, txtOrden (todos `$txtValue`). Vigencia = flatpickr (`js-datepicker`,
    se setea por JS). Moneda=Dollar, Tipo=VIP. Quill "Nombre y Descripción" ES.
- `crear_serie.py` → form `SerieTabContainer` (más simple: Nombre+Orden+Publicado+Quill;
  solo Nombre requerido). Solapas: Detalle, Paquetes, Salidas, Tarifas, Cupos.
  Grid `gvSeries`, buscador `txtSearchName`/`btnSearch`. `txtOrden` SIN `$txtValue`.
- `reporte_circuitos.py` → customtours/. Solo valida que `gvData` exista y tenga filas
  (rowstyle/altrowstyle) > 0. No crea nada.
- Validación de solapas: cada solapa esperada existe (`id=..._pnlX_tab`) + 0 elementos
  con `.ajax__tab_disabled` en el contenedor (mismo enfoque que crear_servicio).
- Nombres con prefijo corto + sello (regla del truncado ~50). Validación de fila por sello.
- El YML quedó corriendo los 5 juntos. Validados estáticamente (`py_compile`, `--collect-only`).

## 6.ter Tests de Cruceros (2026-06-19, recién creados)

- `crear_crucero.py` → `WebAdminCruceroPage` (cruises/detail.aspx, `CruiseTabContainer`).
  Detalle: nombre, Moneda=Dollar, Min/Max rate=0, Flota=Antartida, Ciudad salida=Ushuaia,
  Ciudad llegada=Buenos Aires, orden, Publicado, Quill ES. Solapas validadas: Detalle,
  Imagenes, Destinos, Salidas, Cabinas, Politicas. Grid `gvCruises`, buscador txtSearch.
- `crear_cabina.py` → `WebAdminCabinaPage` (cruisecabs/detail.aspx, `tabContainer` minúscula).
  Detalle: nombre, Cruise=Crucero Antarpply, Moneda=Dollar, Min rate=0, Capacidad=4,
  Tipo=A Stella, Publicado, Quill ES. Solapas: Detalle, Imagenes, Tarifas (pnlCabRates).
  Grid `gvCabs`.
- `crear_flota.py` y `crear_tipo_cabina.py` → `WebAdminCruceroSimplePage` (compartido).
  INLINE (lista+form misma página, grid `gvTypes`, botón `cphActions$btnNew`). Form mínimo:
  Nombre + Publicado. Flotas=cruises/cruisenavies.aspx, Tipos de Cabinas=cruisecabs/
  cruisecabtypes.aspx. Validan la fila en la MISMA pantalla (buscador + sello).
- Reutilizan `escribir_quill` y `validar_solapas` de `webadmin_tour_page`.
- El YML quedó corriendo los 4 juntos. Validados (`py_compile`, `--collect-only`).

## 6.quater Tests de Agencias (2026-06-19, recién creados)

- `crear_tipo_usuario.py` → usertypes.aspx INLINE (gvUserTypes). Nombre+Detalle+Publicado.
- `crear_galeria_pax.py` → passengergallerydetail.aspx (mainTabContainer). txtDetail+agencia+
  fecha+publicado. Vuelve a passengergalleries.aspx (gvData) y valida fila.
- `crear_corporativo.py` → corpdetail.aspx (CorpTabContainer). Solapas Detalle / Config. de
  productos (pnlProductSetting). Requeridos: name/address/comment/email/phone/rewardPointTotal.
- `crear_cliente_corporativo.py` → corpcustomerdetail.aspx (CustomerTabContainer). name/lastname/
  email/username/pass + ddlCorps/ddlWebUserType/ddlCurrency. Guarda directo (sin modal email).
- `crear_usuario.py` → customers/detail.aspx (CustomerTabContainer). ⚠ COMPLEJO: "Guardar" está
  deshabilitado; se usa "Guardar y enviar email" (btnShowPopUp) → MODAL (txtModalEmail/
  txtModalVendorEmail) → "Confirmar" (btnModalConfirm). Password manual (chkEnablePassword + txtPass,
  posible popup btnConfirmPass). Tipo=Cliente, País=España, Moneda=Dollar, Agencia=primera.
- `crear_agencia.py` → ⚠ COMPLEJO 2 pasos: form Agencia (AgencyTabContainer, btnSavePopUp) →
  modal "Sí" (ubicado por TEXTO, best-effort) → form Usuario admin (mismo CustomerTabContainer,
  reusa WebAdminUsuarioPage) → guardar con modal → validar agencia en gvAgencies.
- Helper `_sel_primera` (primera opción real) y `_sel_texto` en los tests; reusan escribir_quill/
  validar_solapas de webadmin_tour_page. Emails únicos por timestamp.
- ⚠ usuario y agencia son best-effort (modales no estaban 100% en el HTML); probable iteración.

## 7. Pendientes / próximos pasos posibles

- Confirmar corrida **verde** de `crear_hotel.py` y `crear_habitacion.py` (target `-m webadmin`).
  - Verificar valores: hotel `value=15474`, tipo de habitación `value=1`, y los `value` de
    categoría/desayuno/ciudad/barrio del hotel; y el texto exacto de las pestañas.
- Más flujos de WebAdmin (ej.: editar hotel/habitación, etc.).
- Limpieza conservadora de `time.sleep` (después de tener red de seguridad en CI).
- (Opcional) Marcar un subconjunto `smoke` para corridas rápidas.

---

## 8. Datos útiles de la app (para tests)

- Hotel de prueba usado en habitaciones: `value=15474` ("Test QA").
- Ciudad usada en hotel: `value=10259` (Cachi) · Barrio: `value=1161` (Molinos).
- Categoría hotel: `value=5` (5★) · Desayuno: `value=7`.
- Tipo de habitación: `value=1` (Standard).
- Las pestañas del detalle de **hotel**: Proveedores, Imágenes, Video(s), Habitaciones,
  Servicios, Puntos de interés, Políticas.
- Las pestañas del detalle de **habitación**: Tarifas & Freesale, Tarifario,
  Detalle del tarifario, Freesale.
