import os
import sys
from pathlib import Path
from django.core.wsgi import get_wsgi_application
from django.core.management import call_command
from django.contrib.auth import get_user_model

# Calculamos la raíz real del proyecto (donde están manage.py y tienda)
BASE_DIR = Path(__file__).resolve().parent.parent

# Inyectamos de forma absoluta la raíz principal en el sistema de Python
sys.path.append(str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'experfrut_project.settings')

application = get_wsgi_application()

# SCRIPT TEMPORAL PARA CORRER MIGRACIONES Y CREAR TU ADMINISTRADOR
try:
    # 1. Fuerza a Django a crear todas las tablas de seguridad e inventario faltantes en Postgres
    print("Ejecutando migraciones en producción...")
    call_command('migrate', interactive=False)
    print("¡Migraciones completadas exitosamente!")

    # 2. Configurado para Alfonso con credenciales de producción de Experfrut
    User = get_user_model()
    if not User.objects.filter(username='alfonso').exists():
        User.objects.create_superuser('alfonso', 'alfonso@experfrut.com', 'alfa18#')
        print("¡Superusuario de producción creado con éxito!")
except Exception as e:
    print(f"Nota del inicializador: {e}")
