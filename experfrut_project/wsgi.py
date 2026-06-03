import os
import sys
from pathlib import Path
from django.core.wsgi import get_wsgi_application

# Calculamos la raíz real del proyecto (donde están manage.py y tienda)
BASE_DIR = Path(__file__).resolve().parent.parent

# Inyectamos de forma absoluta la raíz principal en el sistema de Python
sys.path.append(str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'experfrut_project.settings')

application = get_wsgi_application()
