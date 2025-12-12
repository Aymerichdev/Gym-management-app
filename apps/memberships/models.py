from decimal import Decimal
from django.db import models
from django.utils import timezone


class Membership(models.Model):
    class Type(models.TextChoices):
        BASIC = "basic", "Básica"
        PLUS = "plus", "Plus"
        VIP = "vip", "VIP"

    # TODO Ajustes reales de open gym
    TYPE_PRICES = {
        Type.BASIC: Decimal("20000.00"),
        Type.PLUS:  Decimal("30000.00"),
        Type.VIP:   Decimal("45000.00"),
    }

    client = models.ForeignKey(
        "clients.Client",
        on_delete=models.CASCADE,
        related_name="memberships",
    )

    type = models.CharField(max_length=20, choices=Type.choices)

    # Se calcula automáticamente según el tipo
    price = models.DecimalField(max_digits=8, decimal_places=2, editable=False)

    description = models.TextField(blank=True)

    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)

    last_payment_at = models.DateTimeField(null=True, blank=True)
    next_payment = models.DateField()

    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.price = self.TYPE_PRICES.get(self.type, Decimal("0.00"))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.client} - {self.get_type_display()}"

    # TODO: solo una activa por cliente (implementarlo en lógica)
    # - En save() o en el servicio/endpoint:
    #   si self.is_active True => desactivar otras memberships del mismo client
