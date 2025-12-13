import re

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Client(models.Model):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=30, blank=True)
    start_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def clean(self):
        super().clean()
        errors = {}

        self.first_name = (self.first_name or "").strip()
        self.last_name = (self.last_name or "").strip()
        self.email = (self.email or "").strip().lower()

        if self.start_date and self.start_date > timezone.localdate():
            errors["start_date"] = "La fecha de inicio no puede ser futura."

        phone = (self.phone or "").strip()
        if phone:
            digits = re.sub(r"\D", "", phone)
            if len(digits) == 8:
                phone = f"{digits[:4]}-{digits[4:]}"
            self.phone = phone
            if not re.match(r"^\d{4}-\d{4}$", self.phone):
                errors["phone"] = "Usa el formato 8888-8888."
        else:
            self.phone = ""

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
