from django.db import models
from django.utils import timezone


class Membership(models.Model):
    class Type(models.TextChoices):
        BASIC = "basic", "Básica"
        PLUS = "plus", "Plus"
        VIP = "vip", "VIP"

    client = models.ForeignKey(
        "clients.Client",
        on_delete=models.CASCADE,
        related_name="memberships",
    )

    type = models.CharField(max_length=20, choices=Type.choices)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(blank=True)

    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)

    last_payment_at = models.DateTimeField(null=True, blank=True)
    next_payment = models.DateField()

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.client} - {self.get_type_display()}"

    # Regla pro: solo una activa por cliente (implementarlo en lógica)
    # - En save() o en el servicio/endpoint:
    #   si self.is_active True => desactivar otras memberships del mismo client
