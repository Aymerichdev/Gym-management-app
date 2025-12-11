from django.contrib import admin

from apps.memberships.models import Membership


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "duration_months", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)
