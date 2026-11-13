from django.apps import AppConfig


class AuditConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'audit'
    verbose_name = 'Audit Trail'

    def ready(self):
        # Connect auth signal handlers (SR-004)
        import audit.signals  # noqa
