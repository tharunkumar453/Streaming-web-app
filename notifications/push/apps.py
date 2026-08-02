from django.apps import AppConfig


class PushConfig(AppConfig):
    name = "push"

class NotificationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "notifications"

    def ready(self):
        from . import firebase_config