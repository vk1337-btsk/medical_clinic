from django.contrib import admin
from apps.clients.models import Clients, RegistredServices


@admin.register(Clients)
class ClientsAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "user",
        "passport_id",
        "passport_date",
    )
    list_filter = (
        "user",
        "passport_id",
        "passport_date",
    )
    search_fields = (
        "user",
        "passport_id",
        "passport_date",
    )


@admin.register(RegistredServices)
class RegisterServicesAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "client",
        "service",
        "date_services",
        "doctor",
        "status_service",
        "status_paid",
        "is_analyz",
        "is_vizit",
    )
