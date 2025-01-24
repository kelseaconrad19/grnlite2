from django.apps import AppConfig


class GrnliteConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "grnlite"


class MyAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "my_app"
