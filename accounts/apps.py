from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        from .signals import create_profile  # Import your signal handler
        from django.db.models.signals import post_save
        from .models import User  # Import the User model

        post_save.connect(create_profile, sender=User) 
