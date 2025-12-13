from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("role", User.Roles.OWNER)
        return super().create_superuser(username, email, password, **extra_fields)


class User(AbstractUser):
    class Roles(models.TextChoices):
        OWNER = "owner", "Administrador"
        COACH = "coach", "Coach"

    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.COACH,
    )

    objects = CustomUserManager()
