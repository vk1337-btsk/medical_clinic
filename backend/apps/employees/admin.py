from apps.employees.models import Employees
from django.contrib import admin


@admin.register(Employees)
class EmployeesAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "user",
        "id_employee",
        "job_title",
        "specializations",
    )
    list_filter = (
        "specializations",
        "job_title",
    )
    search_fields = (
        "specializations",
        "job_title",
    )
