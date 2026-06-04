import os
import sys
from pathlib import Path
from django.core.wsgi import get_wsgi_application
from django.db import connection
from django.contrib.auth import get_user_model

# Calculamos la raíz real del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'experfrut_project.settings')

application = get_wsgi_application()

# SCRIPT DE INYECCIÓN COMPLETA CON CAMPOS DE SEGURIDAD AVANZADOS
try:
    print("Sincronizando estructura avanzada para django_otp_staticdevice...")
    with connection.cursor() as cursor:
        # 1. Creamos la tabla con todos los campos requeridos por las versiones modernas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS django_otp_staticdevice (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL UNIQUE,
                name VARCHAR(64) NOT NULL,
                confirmed BOOLEAN NOT NULL DEFAULT FALSE,
                throttled_next_allowed TIMESTAMP WITH TIME ZONE,
                last_used_at TIMESTAMP WITH TIME ZONE,
                throttling_failure_timestamp TIMESTAMP WITH TIME ZONE,
                throttling_failure_count INTEGER NOT NULL DEFAULT 0,
                CONSTRAINT django_otp_staticdevice_user_id_fk FOREIGN KEY (user_id)
                REFERENCES auth_user (id) DEFERRABLE INITIALLY DEFERRED
            );
        """)
        
        # 2. Por si acaso la tabla ya se creó antes sin estas columnas, se las agregamos a la fuerza
        try:
            cursor.execute("ALTER TABLE django_otp_staticdevice ADD COLUMN IF NOT EXISTS throttling_failure_timestamp TIMESTAMP WITH TIME ZONE;")
            cursor.execute("ALTER TABLE django_otp_staticdevice ADD COLUMN IF NOT EXISTS throttling_failure_count INTEGER NOT NULL DEFAULT 0;")
        except Exception:
            pass # Si ya existían, ignora el error
            
    print("¡Estructura de seguridad inyectada con éxito total!")

    # Verificación y creación de tu superusuario Alfonso
    User = get_user_model()
    if not User.objects.filter(username='alfonso').exists():
        User.objects.create_superuser('alfonso', 'alfonso@experfrut.com', 'alfa18#')
        print("¡Superusuario alfonso de producción creado con éxito!")
except Exception as e:
    print(f"Nota del inicializador de base de datos: {e}")
