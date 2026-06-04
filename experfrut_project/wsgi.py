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

# SCRIPT ULTRA FORZADO CON SQL PARA LA TABLA DE SEGURIDAD
try:
    print("Inyectando tabla django_otp_staticdevice vía SQL directo...")
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS django_otp_staticdevice (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL UNIQUE,
                name VARCHAR(64) NOT NULL,
                confirmed BOOLEAN NOT NULL DEFAULT FALSE,
                throttled_next_allowed TIMESTAMP WITH TIME ZONE,
                last_used_at TIMESTAMP WITH TIME ZONE,
                CONSTRAINT django_otp_staticdevice_user_id_fk FOREIGN KEY (user_id)
                REFERENCES auth_user (id) DEFERRABLE INITIALLY DEFERRED
            );
        """)
    print("¡Tabla django_otp_staticdevice inyectada con éxito total!")

    # Verificación y creación de tu superusuario Alfonso
    User = get_user_model()
    if not User.objects.filter(username='alfonso').exists():
        User.objects.create_superuser('alfonso', 'alfonso@experfrut.com', 'alfa18#')
        print("¡Superusuario alfonso de producción creado con éxito!")
except Exception as e:
    print(f"Nota del inicializador de base de datos: {e}")
