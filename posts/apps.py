from django.apps import AppConfig
from django.conf import settings


class PostsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "posts"

    def ready(self):
        if settings.SCHEDULER_DEFAULT:
            from . import runapscheduler
            runapscheduler.start()