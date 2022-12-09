from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Posts


@receiver(post_save, sender=Posts)
def save_post(sender, instance, created, **kwargs):

    # get auth user 
    # import inspect
    # for frame_record in inspect.stack():
    #     if frame_record[3]=='get_response':
    #         request = frame_record[0].f_locals['request']
    #         break
    # else:
    #     request = None
    # print(request.user)

    if created:
        msg = 'Post created'
    else:
       msg = 'Post updated'

    send_mail(
        'Post notification using signal',
        msg,
        settings.DEFAULT_FROM_EMAIL,
        [instance.email],
        fail_silently=False,
    )
