from django.apps import AppConfig


class PostConfig(AppConfig):
    verbose_name = 'Posts'
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'post'

    def ready(self):
        try:
            import post.signals
        except ImportError:
            pass
