import os
import sys
from pathlib import Path
import dj_database_url
from django.utils.translation import gettext_lazy as _

# 1. CONFIGURACIÓN BASE
BASE_DIR = Path(__file__).resolve().parent.parent
# Removimos la línea de inserción de 'app' que desviaba el enrutador de Django
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-tu-clave-secreta-aqui')

DEBUG = False

ALLOWED_HOSTS = ['*']

# 2. APLICACIONES INSTALADAS
INSTALLED_APPS = [
    # Interfaz de administración moderna
    #'jazzmin',
    
    # Aplicaciones nativas de Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Librerías de seguridad y autenticación
    'django_otp',
    'django_otp.plugins.otp_totp',
    'two_factor',
    'axes',
    'tienda', 
]

# 3. MIDDLEWARES (ORDENADOS CORRECTAMENTE)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Manejo eficiente de archivos estáticos
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',          # Seguridad de doble factor
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware',              # Bloqueo de ataques de fuerza bruta
]

ROOT_URLCONF = 'experfrut_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'experfrut_project.wsgi.application'

# 4. BASE DE DATOS POSTGRESQL (PRODUCCIÓN)
DATABASE_URL = os.environ.get('DATABASE_URL')

DATABASES = {
    'default': dj_database_url.config(
        default=DATABASE_URL,
        conn_max_age=600,
        ssl_require=True
    )
}

# 5. VALIDACIÓN DE CONTRASEÑAS
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 6. CONFIGURACIÓN DE RESPALDO DE AUTENTICACIÓN (CORREGIDO SIN ESPACIOS EXTRA)
AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# 7. CONFIGURACIÓN DE IDIOMA Y HORARIO
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# 8. ARCHIVOS ESTÁTICOS Y ENLACE DE CONEXIÓN WHITENOISE
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Añadimos el motor de almacenamiento de WhiteNoise para compresión y caché en servidores virtuales
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 9. CONFIGURACIÓN EXTRA DE SEGURIDAD (AXES)
AXES_FAILURE_LIMIT = 5
AXES_COOLDOWN = 1  # 1 hora de bloqueo si fallan intentos
AXES_LOCKOUT_TEMPLATE = 'axes/lockout.html'

# 10. PERSONALIZACIÓN VISUAL (JAZZMIN RESUMIDO)
JAZZMIN_SETTINGS = {
    "site_title": "Experfrut Admin",
    "site_header": "Experfrut",
    "site_brand": "Experfrut Management",
    "welcome_sign": "Bienvenido al Sistema de Gestión de Experfrut",
    "copyright": "Experfrut Ltd",
    "search_model": ["auth.User"],
    "user_avatar": None,
    "topmenu_links": [
        {"name": "Inicio", "url": "admin:index", "permissions": ["auth.view_user"]},
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "theme": "default",
}
