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

# SCRIPT DE INYECCIÓN COMPLETA CON MARCAS DE TIEMPO (created_at)
try:
    print("Sincronizando campos de tiempo para django_otp_staticdevice...")
    with connection.cursor() as cursor:
        # 1. Creamos la tabla incluyendo las marcas de tiempo requeridas
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
                created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT django_otp_staticdevice_user_id_fk FOREIGN KEY (user_id)
                REFERENCES auth_user (id) DEFERRABLE INITIALLY DEFERRED
            );
        """)
        
        # 2. Inyectamos las columnas directamente por si la tabla ya existía de antes
        try:
            cursor.execute("ALTER TABLE django_otp_staticdevice ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP;")
            cursor.execute("ALTER TABLE django_otp_staticdevice ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP;")
        except Exception:
            pass
            
    print("¡Estructura de tiempo inyectada con éxito total!")

    # Verificación y creación de tu superusuario Alfonso
    User = get_user_model()
    if not User.objects.filter(username='alfonso').exists():
        User.objects.create_superuser('alfonso', 'alfonso@experfrut.com', 'alfa18#')
        print("¡Superusuario alfonso de producción creado con éxito!")
except Exception as e:
    print(f"Nota del inicializador de base de datos: {e}")
