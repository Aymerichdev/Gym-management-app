from django.contrib import admin

from apps.payments.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "client",
        "period_start",
        "period_end",
        "amount",
        "status",
        "paid_at",
        "method",
    )
    list_filter = ("status", "method", "period_start")
    search_fields = ("client__first_name", "client__last_name", "invoice_number")
    raw_id_fields = ("client", "membership", "recorded_by")
    date_hierarchy = "period_start"
