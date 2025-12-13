from django import forms

from apps.memberships.models import Membership


class MembershipForm(forms.ModelForm):
    class Meta:
        model = Membership
        fields = [
            "client",
            "type",
            "price",
            "description",
            "start_date",
            "end_date",
            "last_payment_at",
            "next_payment",
            "is_active",
        ]
        widgets = {
            "client": forms.Select(attrs={"class": "form-select"}),
            "type": forms.Select(attrs={"class": "form-select"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "start_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "end_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "last_payment_at": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
            "next_payment": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {
            "client": "Cliente",
            "type": "Tipo",
            "price": "Precio",
            "description": "Descripción",
            "start_date": "Fecha de inicio",
            "end_date": "Fecha de fin",
            "last_payment_at": "Último pago registrado",
            "next_payment": "Próximo pago",
            "is_active": "Activa",
        }
