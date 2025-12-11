from django.db import models


class Membership(models.Model):
    name = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration_months = models.PositiveSmallIntegerField(default=1)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Membresía"
        verbose_name_plural = "Membresías"

    def __str__(self) -> str:
        return self.name
