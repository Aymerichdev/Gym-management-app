from django.contrib import admin

from apps.clients.models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "status", "coach")
    list_filter = ("status", "coach")
    search_fields = ("first_name", "last_name", "email")
    raw_id_fields = ("coach",)
