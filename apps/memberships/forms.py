from django import forms
from django.utils import timezone

from apps.memberships.models import Membership


class MembershipForm(forms.ModelForm):
    class Meta:
        model = Membership
        fields = [
            "client",
            "type",
            "description",
            "start_date",
            "end_date",
            "is_active",
        ]
        widgets = {
            "client": forms.Select(attrs={"class": "form-select"}),
            "type": forms.Select(attrs={"class": "form-select"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "start_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "end_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {
            "client": "Cliente",
            "type": "Tipo",
            "description": "Descripción",
            "start_date": "Fecha de inicio",
            "end_date": "Fecha de fin",
            "is_active": "Activa",
        }

    price_display = forms.DecimalField(
        label="Precio",
        required=False,
        disabled=True,
        decimal_places=2,
        max_digits=8,
        widget=forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mostrar el precio calculado según el tipo, sin permitir edición.
        initial_price = None
        instance = kwargs.get("instance")
        if self.data.get("type"):
            initial_price = Membership.PRICE_MAP.get(self.data.get("type"))
        elif instance and instance.type:
            initial_price = instance.PRICE_MAP.get(instance.type, instance.price)
        elif self.initial.get("type"):
            initial_price = Membership.PRICE_MAP.get(self.initial["type"])
        self.fields["price_display"].initial = initial_price
        self.fields["start_date"].initial = self.initial.get("start_date") or timezone.localdate()
