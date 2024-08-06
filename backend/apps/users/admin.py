from apps.users.models import Users
from django.contrib import admin


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "email",
        "display_fio",
        "date_birthday",
        "is_client",
        "is_employee",
        "is_superuser",
        "is_staff",
        "is_active",
    )
    list_filter = ("email",)
    search_fields = ("email",)

    def display_fio(self, obj):
        return f"{obj.first_name} {obj.last_name} {obj.middle_name}"

    display_fio.short_description = "ФИО"
