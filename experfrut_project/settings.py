import os
from pathlib import Path
import dj_database_url
from django.utils.translation import gettext_lazy as _

# Rutas del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Seguridad básica
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-5#4*^3zx(xjix)4nqmpyq*$=w#t%_#yl&-5m(s^ov7lilr9ybk')

# Configuración de DEBUG dinámico
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Dominio y Hosts permitidos
ALLOWED_HOSTS = ['*', 'web-production-c14c2.up.railway.app', 'localhost', '127.0.0.1']

# Configuración del proyecto interno (Apuntando a la carpeta real 'app')
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
ROOT_URLCONF = 'app.urls'
WSGI_APPLICATION = 'app.wsgi.application'

# ==============================================================================
# 2. DEFINICIÓN DE APLICACIONES
# ==============================================================================
INSTALLED_APPS = [
    'jazzmin',  # <-- SIEMPRE primero para cambiar el diseño del admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Tus aplicaciones e integraciones de seguridad
    'tienda',
    'django_otp',
    'django_otp.plugins.otp_totp',
    'axes',
]

# ==============================================================================
# 3. MIDDLEWARES (Orden estricto de ejecución)
# ==============================================================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Soporte de archivos estáticos
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',  # Verificación en dos pasos
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware',  # Protección contra fuerza bruta
]

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

# ==============================================================================
# 5. BASE DE DATOS
# ==============================================================================
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        ssl_require=False if os.environ.get('LOCAL_DEVELOPMENT') else True
    )
}

# Conexiones confiables para CSRF (Railway y Ngrok)
CSRF_TRUSTED_ORIGINS = [
    'https://theatrics-facsimile-entrench.ngrok-free.dev',
    'https://web-production-c14c2.up.railway.app'
]

# ==============================================================================
# 6. ARCHIVOS ESTÁTICOS Y MULTIMEDIA
# ==============================================================================
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Idioma y Zona Horaria
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# ==============================================================================
# 7. CONFIGURACIÓN DE JAZZMIN (Interfaz Gráfica)
# ==============================================================================
JAZZMIN_SETTINGS = {
    "site_title": "Experfrut Admin",
    "site_header": "Experfrut",
    "site_brand": "Experfrut Management",
    "welcome_sign": "Bem-vindo ao Experfrut",
    "copyright": "Experfrut Ltd",
    "search_model": ["auth.User"],
    "user_avatar": None,

    "topmenu_links": [
        {"name": "Ir para a Loja", "url": "index", "icon": "fas fa-store", "new_window": False},
        {"name": "Gráficas BI", "url": "dashboard_avanzado", "icon": "fas fa-chart-line", "new_window": False},
        {"model": "auth.User"},
    ],

    "usermenu_links": [
        {"name": "Gráficas BI", "url": "dashboard_avanzado", "icon": "fas fa-chart-pie", "new_window": False},
        {"name": "Ir para a Loja", "url": "index", "icon": "fas fa-store", "new_window": False},
    ],

    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": False,
    "custom_css": None,
    "custom_js": None,
    "show_ui_builder": False,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
}

# ==============================================================================
# 8. CONFIGURACIÓN DE SEGURIDAD AVANZADA (HTTPS / PROXY)
# ==============================================================================
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin"
