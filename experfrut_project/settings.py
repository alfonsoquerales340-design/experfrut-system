import os
import dj_database_url
from pathlib import Path
from django.utils.translation import gettext_lazy as _

# ==============================================================================
# 1. CONFIGURACIÓN BÁSICA Y RUTAS
# ==============================================================================
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-5#4*^3zx(xjix)4nqmpyq*$=w#t%_#yl&-5m(s^ov7lilr9ybk'

DEBUG = False

# Permitir conexiones locales y de red (Ngrok incluido)
# Configuración de URLs permitidas (El '*' incluye ngrok, localhost y Render automáticamente)
ALLOWED_HOSTS = ['*']

# Configuración de archivos estáticos
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') 

# Configuración de archivos multimedia (imágenes cargadas por usuarios)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Configuración del proyecto interno de Django
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
ROOT_URLCONF = 'experfrut_project.urls'
WSGI_APPLICATION = 'experfrut_project.wsgi.application'

# Confianza para túneles externos
CSRF_TRUSTED_ORIGINS = ['https://theatrics-facsimile-entrench.ngrok-free.dev']

# ==============================================================================
# 2. DEFINICIÓN DE APLICACIONES
# ==============================================================================
INSTALLED_APPS = [
    'tienda',
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'django_otp',
    'django_otp.plugins.otp_static',
    'django_otp.plugins.otp_totp',
    'two_factor',
    'two_factor.plugins.webauthn',
    'axes',
]

# ==============================================================================
# 3. MIDDLEWARE Y AUTENTICACIÓN
# ==============================================================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # <-- Ponla aquí exacto
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',
    'django.contrib.auth.backends.ModelBackend',
]

LOGIN_URL = 'two_factor:login'
LOGIN_REDIRECT_URL = '/'

# ==============================================================================
# 4. TEMPLATES
# ==============================================================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'tienda', 'templates'),
        ], 
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
# 5. BASE DE DATOS Y LOCALIZACIÓN
# ==============================================================================
DATABASES = {
    'default': dj_database_url.config(
        default= 'sqlite:///db.sqlite3',
        conn_max_age=600
    )
}
# ==============================================================================
# 6. ARCHIVOS ESTÁTICOS
# ==============================================================================
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') 

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==============================================================================
# 7. JAZZMIN SETTINGS
# ==============================================================================
JAZZMIN_SETTINGS = {
    "site_title": "Experfrut Admin",
    "site_header": "Experfrut",
    "site_brand": "Experfrut",
    "welcome_sign": "Bem-vindo ao Experfrut",
    "copyright": "Experfrut Ltd",
    "search_model": ["auth.User", "tienda.Hortifruti"],
    
    # 1. MENÚ SUPERIOR (Navegación principal)
    "topmenu_links": [
        # Redirige directo al index de la tienda usando el name='index' de tu urls.py
        {"name": "Ir para a Loja", "url": "index", "permissions": ["auth.view_user"], "icon": "fas fa-store", "new_window": False},
        # Redirige al dashboard avanzado usando el name='dashboard_avanzado'
        {"name": "Gráficas BI", "url": "dashboard_avanzado", "icon": "fas fa-chart-line", "new_window": False},
        {"model": "auth.User"},
    ],

    # 2. MENÚ DE USUARIO (Desplegable de Account)
    "usermenu_links": [
        {
            "name": "Configurar Biometria (Digital)", 
            "url": "/account/two_factor/setup/", 
            "icon": "fas fa-fingerprint",
            "permissions": ["auth.view_user"]
        },
        # Enlaces corregidos con los nombres de ruta para evitar errores 404
        {"name": "Gráficas BI", "url": "dashboard_avanzado", "icon": "fas fa-chart-pie", "new_window": False},
        {"name": "Ir para a Loja", "url": "index", "icon": "fas fa-store", "new_window": False},
    ],

    "show_sidebar": True,
    "navigation_expanded": False,

    # 3. ICONOS DEL MENÚ LATERAL
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "tienda.Hortifruti": "fas fa-apple-alt",
        "tienda.MovimientoInventario": "fas fa-exchange-alt", 
        "tienda.StockPorSucursal": "fas fa-map-marker-alt",
        "two_factor.phonedevice": "fas fa-mobile-alt",
    },

    "changeform_format": "horizontal_tabs",
    "related_modal_active": True,
    "use_google_fonts_cdn": True,

    "custom_css": "tienda/css/custom_admin.css", 
    "custom_js": None,
    "show_ui_builder": False,
}
# ==============================================================================
# 8. CONFIGURACIÓN DE SEGURIDAD (2FA Y HUELLA) - ACTUALIZADO
# ==============================================================================

# Identidad del servidor para WebAuthn
TWO_FACTOR_WEBAUTHN_RP_NAME = 'Experfrut'

# IMPORTANTE: El RP_ID debe coincidir con el dominio que usas.
# Cuando uses ngrok, cámbialo a 'theatrics-facsimile-entrench.ngrok-free.dev'
TWO_FACTOR_WEBAUTHN_RP_ID = 'theatrics-facsimile-entrench.ngrok-free.dev'

TWO_FACTOR_WEBAUTHN_AUTHENTICATORS = 'two_factor.plugins.webauthn.models.WebAuthnDevice'

TWO_FACTOR_METHODS = (
    'generator',
    'webauthn',
)

TWO_FACTOR_METHOD_LABELS = {
    'generator': _('Código generado por aplicación'),
    'webauthn': _('Huella digital / Llave de seguridad'),
}

TWO_FACTOR_WEBAUTHN_SETUP_TEMPLATE = 'two_factor/setup.html'

# --- CONFIGURACIÓN PARA TÚNELES HTTPS (NGROK) ---
# Esto permite que Django confíe en el túnel seguro de ngrok para la biometría
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin"

# Al final de tu archivo settings.py (fuera del diccionario), añade esto:
JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-dark",
    "accent": "accent-primary",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "default",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}
