from django.db import models
from django.contrib.auth.models import User, Group

class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    avatar = models.TextField(blank=True, null=True)
    phone = models.TextField(blank=True, null=True)

    # Role_id > auth_group.id
    role = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="profiles"
    )

    def __str__(self):
        return f"{self.user.username} Profile"
