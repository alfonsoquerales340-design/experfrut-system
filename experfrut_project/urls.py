from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from two_factor.urls import urlpatterns as tf_urls

from tienda.views import index, registrar_salida, dashboard_vendas, analista_ia, ai_test, dashboard_avanzado

urlpatterns = [
    # 1. Admin (Jazzmin se acopla aquí) - Le agregamos la barra explícita para evitar desvíos
    path('admin/', admin.site.urls),

    # 2. Service Worker (CRÍTICO para la instalación en el móvil de los stockers)
    path('sw.js', TemplateView.as_view(template_name="sw.js", content_type='application/javascript'), name='sw.js'),

    # 3. Rutas de la aplicación Experfrut
    path('', index, name='index'), 
    path('dashboard/', dashboard_vendas, name='dashboard'),
    path('registrar-salida/', registrar_salida, name='registrar_salida'),
    path('analista-ia/', analista_ia, name='analista_ia'),
    path('api/ai/', ai_test, name='api_ai_test'),  # Nombre único para evitar conflictos de reversión
    path('dashboard-avanzado/', dashboard_avanzado, name='dashboard_avanzado'),

    # 4. Seguridad 2FA y Huella (WebAuthn) - Lo ponemos al final de las rutas fijas
    path('', include((tf_urls, 'two_factor'), namespace='two_factor_apps')), 
]

# Servir archivos multimedia (fotos de frutas) y estáticos en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    # En producción Railway, WhiteNoise sirve los estáticos de forma nativa.
    # Solo dejamos multimedia activo si se requiere.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
