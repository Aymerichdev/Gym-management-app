from django.contrib import admin

from apps.memberships.models import Membership


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = (
        "client",
        "type",
        "price",
        "next_payment",
        "is_active",
    )
    list_filter = ("type", "is_active", "next_payment")
    search_fields = ("client__first_name", "client__last_name")
    raw_id_fields = ("client",)
