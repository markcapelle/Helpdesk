from django.db import models
from django.contrib.auth.models import User, Group
from cloudinary.models import CloudinaryField

class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    avatar = CloudinaryField('avatar', blank=True, null=True)
    country_code = models.CharField(max_length=10, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)


    # Role_id > auth_group.id
    role = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="profiles"
    )

    def formatted_phone(self):
        if not self.phone:
            return ""

        raw = self.phone.replace(" ", "")

        # Optional: add (0) formatting only for display
        if raw.startswith("0"):
            raw = f"(0){raw[1:]}"
        else:
            raw = f"(0){raw}"

        return f"{self.country_code} {raw}"

    def is_admin(self):
        return self.user.groups.filter(name__iexact="administrator").exists()




    def __str__(self):
        return f"{self.user.username} Profile"

