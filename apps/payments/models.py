from django.conf import settings
from django.db import models
from django.utils import timezone


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pendiente"
        PAID = "paid", "Pagado"
        OVERDUE = "overdue", "Vencido"

    client = models.ForeignKey(
        "clients.Client",
        on_delete=models.CASCADE,
        related_name="payments",
    )
    membership = models.ForeignKey(
        "memberships.Membership",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payments",
    )
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    period_start = models.DateField()
    period_end = models.DateField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    paid_at = models.DateTimeField(null=True, blank=True)
    method = models.CharField(max_length=40, blank=True, help_text="Efectivo, tarjeta, transferencia, etc.")
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

    class Meta:
        ordering = ["-period_start", "client"]
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"
        constraints = [
            models.UniqueConstraint(
                fields=["client", "period_start", "period_end"],
                name="unique_payment_per_period",
            )
        ]

    def __str__(self) -> str:
        return f"Pago {self.client} {self.period_start:%Y-%m} - {self.get_status_display()}"
