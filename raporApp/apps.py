from django.apps import AppConfig


class RaporappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'raporApp'

    def ready(self):
        import raporApp.signals