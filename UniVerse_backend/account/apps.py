from django.apps import AppConfig


class AccountConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "account"


from django.apps import AppConfig

class YourAppConfig(AppConfig):
    name = 'account'

    def ready(self):
        import account.signals
