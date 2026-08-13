from django.apps import AppConfig


class MessengerConfig(AppConfig):
    name = 'messenger'

    def ready(self):
        from django.contrib.auth.models import Permission
        from django.contrib.contenttypes.models import ContentType
        from .models import Message

        ct = ContentType.objects.get_for_model(Message)

        Permission.objects.get_or_create(
            codename='messenger_read',
            name='Can read messenger',
            content_type=ct
        )

        Permission.objects.get_or_create(
            codename='messenger_write',
            name='Can write messenger',
            content_type=ct
        )
