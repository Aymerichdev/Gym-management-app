from django.contrib import admin

from apps.clients.models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "phone", "start_date")
    list_filter = ("start_date",)
    search_fields = ("first_name", "last_name", "email")
