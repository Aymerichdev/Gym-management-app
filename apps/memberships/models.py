from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Membership(models.Model):
    PRICE_MAP = {"basic": Decimal("25.00"), "plus": Decimal("40.00"), "vip": Decimal("60.00")}

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

    start_date = models.DateField(default=timezone.localdate)
    end_date = models.DateField(null=True, blank=True)

    last_payment_at = models.DateTimeField(null=True, blank=True)
    next_payment = models.DateField(blank=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.client} - {self.get_type_display()}"

    # Regla pro: solo una activa por cliente (implementarlo en lógica)
    # - En save() o en el servicio/endpoint:
    #   si self.is_active True => desactivar otras memberships del mismo client

    def clean(self):
        super().clean()
        errors = {}

        self.description = (self.description or "").strip()

        if self.type in self.PRICE_MAP:
            self.price = self.PRICE_MAP[self.type]

        if not self.next_payment:
            self.next_payment = self.start_date or timezone.localdate()

        today = timezone.localdate()

        if self.start_date and self.start_date > today:
            errors["start_date"] = "La fecha de inicio no puede ser futura."

        if self.end_date and self.start_date and self.end_date < self.start_date:
            errors["end_date"] = "La fecha de fin no puede ser anterior al inicio."

        if self.next_payment and self.start_date and self.next_payment < self.start_date:
            errors["next_payment"] = "El próximo pago no puede ser antes del inicio."

        if self.is_active and self.next_payment and self.next_payment < today:
            errors["next_payment"] = "Una membresía activa no puede tener próximo pago en el pasado."

        if self.end_date and self.end_date < today:
            self.is_active = False

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        result = super().save(*args, **kwargs)
        if self.is_active:
            Membership.objects.filter(client=self.client, is_active=True).exclude(pk=self.pk).update(
                is_active=False
            )
        return result

    def recalculate_payment_tracking(self):
        """Recalcula last_payment_at y next_payment con pagos confirmados."""

        from apps.payments.models import Payment
        from dateutil.relativedelta import relativedelta

        paid_payments = (
            self.payments.filter(status=Payment.Status.PAID, paid_at__isnull=False)
            .order_by("paid_at", "created_at")
        )

        base_date = self.start_date or timezone.localdate()
        last_paid = None

        for payment in paid_payments:
            base_date = max(base_date, payment.paid_at.date())
            base_date = base_date + relativedelta(months=payment.months_covered)
            last_paid = payment.paid_at

        if last_paid:
            self.last_payment_at = last_paid
            self.next_payment = base_date
            self.is_active = self.next_payment >= timezone.localdate()
            super().save(update_fields=["last_payment_at", "next_payment", "is_active"])
