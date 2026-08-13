from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .models import Message

@receiver(post_migrate)
def create_messenger_permissions(sender, **kwargs):
    if sender.name != "messenger":
        return

    ct = ContentType.objects.get_for_model(Message)

    Permission.objects.get_or_create(
        codename="messenger_read",
        name="Can read messenger",
        content_type=ct,
    )
    Permission.objects.get_or_create(
        codename="messenger_write",
        name="Can write messenger",
        content_type=ct,
    )
