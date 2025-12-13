from django.contrib import admin

from apps.payments.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "membership",
        "amount",
        "months_covered",
        "status",
        "paid_at",
        "method",
    )
    list_filter = ("status", "method", "created_at")
    search_fields = ("membership__client__first_name", "membership__client__last_name", "invoice_number")
    raw_id_fields = ("membership", "recorded_by")
    date_hierarchy = "created_at"
