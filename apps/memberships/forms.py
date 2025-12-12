from django import forms

from apps.memberships.models import Membership


class MembershipForm(forms.ModelForm):
    class Meta:
        model = Membership
        fields = ["name", "price", "duration_months", "description", "is_active"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "duration_months": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {
            "name": "Nombre",
            "price": "Precio",
            "duration_months": "Duración (meses)",
            "description": "Descripción",
            "is_active": "Activa",
        }
