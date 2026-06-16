from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    name = 'notifications'


class NotificationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "notifications"
 
    def ready(self):
        # シグナルを登録する
        import notifications.signals  # noqa: F401
 
