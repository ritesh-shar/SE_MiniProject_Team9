from django.apps import AppConfig


class DispatchConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dispatch'
    verbose_name = 'Dispatch Tracking'

    def ready(self):
        # Register dispatch signals and audit trail hooks (BBMS-F-042, BBMS-NF-005)
        import dispatch.signals  # noqa
        import dispatch.audit_hooks  # noqa
