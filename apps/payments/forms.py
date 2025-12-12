from django import forms

from apps.payments.models import Payment


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = [
            "membership",
            "amount",
            "period_start",
            "period_end",
            "status",
            "paid_at",
            "method",
            "invoice_number",
            "notes",
            "recorded_by",
        ]
        widgets = {
            "membership": forms.Select(attrs={"class": "form-select"}),
            "amount": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "period_start": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "period_end": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "paid_at": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),
            "method": forms.TextInput(attrs={"class": "form-control", "placeholder": "efectivo, tarjeta, sinpe"}),
            "invoice_number": forms.TextInput(attrs={"class": "form-control", "placeholder": "Folio o recibo"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "recorded_by": forms.Select(attrs={"class": "form-select"}),
        }
        labels = {
            "membership": "Membresía",
            "amount": "Monto",
            "period_start": "Periodo inicio",
            "period_end": "Periodo fin",
            "status": "Estado",
            "paid_at": "Pagado el",
            "method": "Método de pago",
            "invoice_number": "Factura/recibo",
            "notes": "Notas",
            "recorded_by": "Registrado por",
        }
