from django.apps import AppConfig


class PoliciesConfig(AppConfig):
    name = 'policies'
    
    def ready(self):
        import policies.signals
