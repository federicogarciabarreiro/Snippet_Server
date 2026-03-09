# Snippets (Server Project)

## ES - Que es esta carpeta
Esta carpeta contiene muestras publicas de codigo del proyecto servidor.
El objetivo es mostrar capacidad tecnica con ejemplos claros y reutilizables.

## EN - What this folder is
This folder contains public code samples from the server project.
The goal is to show technical capability with clear and reusable examples.

---

## ES - 01 FastAPI Security And Gate
Archivo: `01_fastapi_security_and_gate.py`

Paso a paso:
1. Define el esquema OAuth2 para tokens Bearer.
2. Decodifica el JWT usando `SECRET_KEY` y algoritmo.
3. Valida que el token tenga `sub` (user id).
4. Busca el usuario en base de datos y valida que este activo.
5. Implementa middleware de puerta global (`/login`) para proteger docs y rutas privadas.
6. Permite rutas publicas puntuales (`/login`, `/health`, auth basica, estaticos).

## EN - 01 FastAPI Security And Gate
File: `01_fastapi_security_and_gate.py`

Step by step:
1. Defines OAuth2 schema for Bearer tokens.
2. Decodes JWT using `SECRET_KEY` and algorithm.
3. Validates token contains `sub` (user id).
4. Loads user from database and checks active status.
5. Implements a global access gate middleware (`/login`) for docs and private routes.
6. Allows specific public routes (`/login`, `/health`, basic auth, static files).

---

## ES - 02 Commerce Checkout And Webhook
Archivo: `02_commerce_checkout_and_webhook.py`

Paso a paso:
1. Crea una orden `pending` con formato compatible con Stripe (`checkout_session_id`).
2. Inserta `order_items` y calcula subtotal/total.
3. Registra evento webhook simulado con idempotencia por `stripe_event_id`.
4. Marca la orden como `paid` solo si corresponde.
5. Acredita inventario del usuario en `user_inventory`.
6. Marca evento como procesado (`is_processed=true`).

## EN - 02 Commerce Checkout And Webhook
File: `02_commerce_checkout_and_webhook.py`

Step by step:
1. Creates a `pending` order with Stripe-compatible shape (`checkout_session_id`).
2. Inserts `order_items` and calculates subtotal/total.
3. Stores simulated webhook event with idempotency by `stripe_event_id`.
4. Marks order as `paid` only when appropriate.
5. Credits user inventory in `user_inventory`.
6. Marks event as processed (`is_processed=true`).

---

## ES - 03 React Multiapp API
Archivo: `03_react_multiapp_api.jsx`

Paso a paso:
1. Crea un cliente HTTP unico con token Bearer opcional.
2. Encapsula errores HTTP en excepciones claras.
3. Separa modulos de API para ecommerce y backoffice.
4. Reutiliza el mismo cliente para auth, catalogo, checkout, entitlements y RPC admin.

## EN - 03 React Multiapp API
File: `03_react_multiapp_api.jsx`

Step by step:
1. Creates one HTTP client with optional Bearer token.
2. Wraps HTTP failures into clear exceptions.
3. Splits API modules for ecommerce and backoffice.
4. Reuses the same client for auth, catalog, checkout, entitlements, and admin RPC.

---

## ES - 04 Unity WebGL Coroutine API
Archivo: `04_unity_webgl_coroutine_api.cs`

Paso a paso:
1. Usa `UnityWebRequest` sin SDK externos (compatible WebGL).
2. Implementa login con `WWWForm` y endpoints JSON.
3. Maneja telemetria Unity: iniciar sesion, registrar eventos y cerrar sesion.
4. Incluye token Bearer en headers cuando existe.
5. Devuelve callbacks de exito/error para integracion simple en juego.

## EN - 04 Unity WebGL Coroutine API
File: `04_unity_webgl_coroutine_api.cs`

Step by step:
1. Uses `UnityWebRequest` with no external SDKs (WebGL-friendly).
2. Implements login via `WWWForm` and JSON endpoints.
3. Handles Unity telemetry: start session, append events, end session.
4. Adds Bearer token headers when available.
5. Returns success/error callbacks for easy game integration.

---

## ES - 05 Supabase Schema RPC
Archivo: `05_supabase_schema_rpc.sql`

Paso a paso:
1. Define tablas core para ordenes, items y eventos de webhook.
2. Aplica restricciones (`check`) para proteger integridad de datos.
3. Implementa RPC idempotente para eventos Stripe.
4. Usa `security definer` y `search_path` fijo para mayor control operativo.

## EN - 05 Supabase Schema RPC
File: `05_supabase_schema_rpc.sql`

Step by step:
1. Defines core tables for orders, items, and webhook events.
2. Adds integrity constraints (`check`) to protect data quality.
3. Implements idempotent Stripe-event RPC.
4. Uses `security definer` and fixed `search_path` for operational safety.
