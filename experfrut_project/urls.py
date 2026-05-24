from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from two_factor.urls import urlpatterns as tf_urls

# Importamos tus vistas directamente desde la raíz (Quitamos "tienda.")
from views import index, registrar_salida, dashboard_vendas, analista_ia, ai_test, dashboard_avanzado

urlpatterns = [
    # 1. Admin
    path('admin/', admin.site.urls),

    # 2. Seguridad 2FA y Huella (WebAuthn)
    # Forma limpia de incluir las rutas para evitar el error urls.E004
    path('', include(tf_urls)), 

    # 3. Service Worker (CRÍTICO para el móvil)
    path('sw.js', TemplateView.as_view(template_name="sw.js", content_type='application/javascript'), name='sw.js'),

    # 4. Rutas de Experfrut
    path('', index, name='index'), 
    path('dashboard/', dashboard_vendas, name='dashboard'),
    path('registrar-salida/', registrar_salida, name='registrar_salida'),
    path('analista-ia/', analista_ia, name='analista_ia'),
    path('api/ai/', ai_test, name='ai_test'),
    # Nueva ruta para el dashboard de Business Intelligence
    path('dashboard-avanzado/', dashboard_avanzado, name='dashboard_avanzado'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
