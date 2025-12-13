# Gym Management App

Base monolítica en Django para la administración interna de un gimnasio pequeño
(~200 clientes). Incluye la estructura inicial de apps para usuarios, clientes,
membresías y pagos mensuales.

## Requisitos
- Python 3.11+
- Dependencias en `requirements.txt` (Django + driver de PostgreSQL)
- Acceso opcional a PostgreSQL; por defecto se usa SQLite para desarrollo local.

## Cómo ejecutar el proyecto (paso a paso)
1. Crea y activa un entorno virtual:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```
2. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Variables de entorno (elige el método que prefieras):
   - **Usar archivo `.env` (recomendado):**
     ```bash
     cp .env.example .env
     # Edita .env con tus valores
     ```
     El proyecto carga automáticamente `.env` al iniciar, sin sobreescribir variables ya exportadas en tu shell.
   - **O exportar a mano en la terminal:**
     ```bash
     export DB_ENGINE=django.db.backends.postgresql
     export DB_NAME=gym
     export DB_USER=gym_user
     export DB_PASSWORD=superseguro
     export DB_HOST=localhost
     export DB_PORT=5432
     export DJANGO_SECRET_KEY=usa-una-clave-segura
     export DJANGO_DEBUG=False
     export DJANGO_ALLOWED_HOSTS="localhost 127.0.0.1"
     ```
4. Ejecuta migraciones y crea un superusuario para entrar al panel admin:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```
5. Levanta el servidor de desarrollo:
   ```bash
   python manage.py runserver
   ```
6. Abre `http://127.0.0.1:8000/admin/` y entra con el superusuario que creaste para gestionar datos.

## Estructura de apps
- `apps.accounts`: usuario personalizado con roles (dueño, coach, staff) y hook para permisos.
- `apps.clients`: datos de clientes, coach asignado y notas.
- `apps.memberships`: catálogo de planes (precio, duración, estado).
- `apps.payments`: pagos mensuales con estado, método, comprobante y periodo asociado.

La arquitectura favorece vistas renderizadas en servidor; los templates viven en
`templates/` (crear según tus vistas). Usa el admin de Django para empezar a
operar sin escribir vistas adicionales.

## ¿Para qué sirve cada archivo/directorio?
Estructura breve del esqueleto actual para que sepas dónde extender la app:

- `manage.py`: punto de entrada para comandos de Django (runserver, migrate, createsuperuser, etc.).
- `requirements.txt`: dependencias mínimas del proyecto (Django y driver de PostgreSQL).
- `.gitignore`: exclusiones típicas de Python/Django (archivos de entorno, compilados, migraciones locales).

### Core del proyecto (`gym_manager/`)
- `gym_manager/__init__.py`: marca el paquete principal de configuración del proyecto.
- `gym_manager/settings.py`: configuración global (apps instaladas, BD, templates, estáticos, autenticación, etc.).
- `gym_manager/urls.py`: enrutador raíz; incluye rutas de admin y futuras vistas públicas/privadas.
- `gym_manager/asgi.py`: punto ASGI para despliegues asíncronos (ej. uvicorn/daphne).
- `gym_manager/wsgi.py`: punto WSGI para despliegues clásicos (gunicorn/uwsgi).

### Apps de dominio (`apps/`)
Cada subcarpeta es una app Django autocontenida. No se ha añadido lógica dentro de ellas todavía; solo están los archivos base para que completes la funcionalidad.

- `apps/accounts`: usuario personalizado con roles/permiso básico.
- `apps/clients`: datos del cliente y asignación a un coach.
- `apps/memberships`: catálogo de membresías/planes.
- `apps/payments`: registro de pagos mensuales vinculados a clientes y membresías.

#### Archivos de cada app (sin código agregado aún)
- `__init__.py`: marca el paquete Python de la app.
- `apps.py`: configuración de la app para que Django la registre.
- `models.py`: lugar para definir los modelos/entidades de BD de esa app.
- `admin.py`: donde registrarás los modelos para que aparezcan en el panel admin.
- `views.py`: donde colocarás vistas basadas en funciones o clases; están vacías para que las completes.
- (Cuando se creen) `migrations/`: carpeta que generará Django con las migraciones de los modelos; se crea al ejecutar `python manage.py makemigrations`.

> Nota: no hay carpeta separada llamada `backend/` porque el propio proyecto Django es el backend. Las vistas, templates y estáticos vivirán dentro de las apps o en carpetas globales como `templates/` y `static/` cuando las añadas.
