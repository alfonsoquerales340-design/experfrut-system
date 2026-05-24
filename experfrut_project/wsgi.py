
import os
import sys
from pathlib import Path
from django.core.wsgi import get_wsgi_application

# Añadir la raíz al camino de Python para que encuentre 'app'
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'experfrut_project.settings')

application = get_wsgi_application()
