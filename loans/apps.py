from django.apps import AppConfig

class FinancesConfig(AppConfig):
    name = 'loans'

    def ready(self):
        import loans.signals
