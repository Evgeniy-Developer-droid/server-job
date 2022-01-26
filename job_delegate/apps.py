from django.apps import AppConfig


class JobDelegateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'job_delegate'

    def ready(self):
        import job_delegate.signals
