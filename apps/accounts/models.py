from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Roles(models.TextChoices):
        OWNER = "owner", "Administrador"
        COACH = "coach", "Coach"
        STAFF = "staff", "Recepción"

    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.COACH,
        help_text="Rol que determina permisos y visibilidad dentro del panel.",
    )

    def __str__(self) -> str:
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"
