from django.apps import AppConfig


class HfntrConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hfntr'

    def ready(self):
        import hfntr.signals
