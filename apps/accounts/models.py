from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Roles(models.TextChoices):
        OWNER = "owner", "Administrador"
        COACH = "coach", "Coach"

    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.COACH,
    )
