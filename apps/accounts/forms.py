from django import forms
from django.contrib.auth import get_user_model


User = get_user_model()


class CoachCreateForm(forms.ModelForm):
    """Minimal form to register coach accounts without granting staff access."""

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }
        labels = {
            "username": "Usuario",
            "first_name": "Nombre",
            "last_name": "Apellido",
            "email": "Correo",
        }

    def save(self, commit=True):
        coach = super().save(commit=False)
        coach.role = User.Roles.COACH
        coach.is_staff = False
        coach.is_superuser = False
        coach.is_active = True
        coach.set_unusable_password()
        if commit:
            coach.save()
        return coach
