# Gym Management App

Base monolítica en Django para la administración interna de un gimnasio pequeño
(~200 clientes). Incluye la estructura inicial de apps para usuarios, clientes,
membresías y pagos mensuales.

## Requisitos
- Python 3.11+
- Dependencias en `requirements.txt` (Django + driver de PostgreSQL)
- Acceso opcional a PostgreSQL; por defecto se usa SQLite para desarrollo local.

## Configuración rápida
1. Crea y activa un entorno virtual.
2. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Exporta variables de entorno según tu base de datos (opcional):
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
4. Ejecuta migraciones y crea un superusuario:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```
5. Levanta el servidor de desarrollo:
   ```bash
   python manage.py runserver
   ```

## Estructura de apps
- `apps.accounts`: usuario personalizado con roles (dueño, coach, staff) y hook para permisos.
- `apps.clients`: datos de clientes, coach asignado y notas.
- `apps.memberships`: catálogo de planes (precio, duración, estado).
- `apps.payments`: pagos mensuales con estado, método, comprobante y periodo asociado.

La arquitectura favorece vistas renderizadas en servidor; los templates viven en
`templates/` (crear según tus vistas). Usa el admin de Django para empezar a
operar sin escribir vistas adicionales.
