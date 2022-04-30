from django.apps import AppConfig


class NinjaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ninja'

    def ready(self) -> None:
        import ninja.signals
