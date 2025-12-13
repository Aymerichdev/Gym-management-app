from django.conf import settings
from django.db import models
from django.utils import timezone


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pendiente"
        PAID = "paid", "Pagado"
        OVERDUE = "overdue", "Vencido"

    membership = models.ForeignKey(
        "memberships.Membership",
        on_delete=models.CASCADE,
        related_name="payments",
    )

    amount = models.DecimalField(max_digits=8, decimal_places=2)
    months_covered = models.PositiveIntegerField(default=1)

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    paid_at = models.DateTimeField(null=True, blank=True)

    method = models.CharField(max_length=40, blank=True)  # efectivo, tarjeta, sinpe...
    invoice_number = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)

    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="recorded_payments",
    )

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.membership} - {self.amount} ({self.status})"
