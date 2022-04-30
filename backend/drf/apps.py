from django.apps import AppConfig


class DRFConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'drf'

    def ready(self) -> None:
        import drf.signals
