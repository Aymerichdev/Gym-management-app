from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pendiente"
        PAID = "paid", "Pagado"
        OVERDUE = "overdue", "Vencido"

    class Method(models.TextChoices):
        CASH = "cash", "Efectivo"
        CARD = "card", "Tarjeta"
        SINPE = "sinpe", "Sinpe"
        OTHER = "other", "Otro"

    membership = models.ForeignKey(
        "memberships.Membership",
        on_delete=models.CASCADE,
        related_name="payments",
    )

    amount = models.DecimalField(max_digits=8, decimal_places=2)
    months_covered = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    paid_at = models.DateTimeField(null=True, blank=True)

    method = models.CharField(max_length=40, blank=True, choices=Method.choices)
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

    def clean(self):
        super().clean()
        errors = {}

        if self.amount is not None and self.amount <= 0:
            errors["amount"] = "El monto debe ser mayor a 0."

        if self.months_covered is not None and not (1 <= self.months_covered <= 24):
            errors["months_covered"] = "Los meses cubiertos deben estar entre 1 y 24."

        if self.status == self.Status.PAID:
            if not self.paid_at:
                self.paid_at = timezone.now()
        else:
            self.paid_at = None

        if self.status != self.Status.PAID and self.paid_at:
            errors["paid_at"] = "Solo pagos marcados como Pagado pueden tener fecha de pago."

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        from dateutil.relativedelta import relativedelta

        self.full_clean()
        result = super().save(*args, **kwargs)

        if self.status == self.Status.PAID:
            membership = self.membership
            today = timezone.localdate()
            base_date = max(membership.next_payment, today)
            membership.last_payment_at = self.paid_at
            membership.next_payment = base_date + relativedelta(months=self.months_covered)
            membership.is_active = membership.next_payment >= today
            membership.save(update_fields=["last_payment_at", "next_payment", "is_active"])

        return result
