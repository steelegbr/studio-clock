from django.apps import AppConfig


class StudioClockConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "studioclock"

    def ready(self):
        import studioclock.signals  # noqa: F401
