import os
import sys
from pathlib import Path
from django.core.wsgi import get_wsgi_application
from django.contrib.auth import get_user_model
from django.core.management import call_command

# Calculamos la raíz real del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'experfrut_project.settings')

application = get_wsgi_application()

# SCRIPT TEMPORAL PARA FORZAR TABLAS DE OTP Y SUPERUSUARIO
try:
    print("Corriendo migración forzada aislada para componentes OTP...")
    # Sincroniza las tablas de seguridad directamente saltándose el historial falso
    call_command('migrate', 'django_otp', interactive=False)
    call_command('migrate', 'otp_totp', interactive=False)
    print("¡Tablas de seguridad OTP inyectadas con éxito!")

    # Verificación y creación de tu superusuario Alfonso
    User = get_user_model()
    if not User.objects.filter(username='alfonso').exists():
        User.objects.create_superuser('alfonso', 'alfonso@experfrut.com', 'alfa18#')
        print("¡Superusuario de producción creado con éxito!")
except Exception as e:
    print(f"Nota del inicializador de base de datos: {e}")
