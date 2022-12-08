from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings

User = get_user_model()


# @receiver(post_save, sender=User)
def save_post(sender, instance, created, **kwargs):
    if created:
        msg = 'User created'
    else:
       msg = 'User updated'

    send_mail(
        'User notification using signal',
        msg,
        settings.DEFAULT_FROM_EMAIL,
        [instance.email],
        fail_silently=False,
    )
