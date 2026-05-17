from django.apps import AppConfig

class YourAppConfig(AppConfig):
    name = 'gorevApp'

    def ready(self):
        import gorevApp.signals
