import os
import sys
from pathlib import Path
from django.core.wsgi import get_wsgi_application
from django.contrib.auth import get_user_model

# Calculamos la raíz real del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'experfrut_project.settings')

application = get_wsgi_application()

# SCRIPT TEMPORAL ÚNICAMENTE PARA EL SUPERUSUARIO
try:
    User = get_user_model()
    if not User.objects.filter(username='alfonso').exists():
        User.objects.create_superuser('alfonso', 'alfonso@experfrut.com', 'alfa18#')
        print("¡Superusuario de producción creado con éxito!")
except Exception as e:
    print(f"Nota del creador de usuario: {e}")
