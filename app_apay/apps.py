from django.apps import AppConfig

class AppApayConfig(AppConfig):
    name = 'app_apay'

    def ready(self):
        import app_apay.signals
