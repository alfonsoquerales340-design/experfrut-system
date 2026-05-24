from django.apps import AppConfig

class RaizConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'  # Le decimos a Django que el contenedor global se llama 'app'
