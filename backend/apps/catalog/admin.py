from re import A
from django.contrib import admin
from apps.catalog.models import ServiceInformation, ServiceСategories


@admin.register(ServiceСategories)
class ServiceСategoriesAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "title",
        "description",
    )
    list_filter = ("title",)
    search_fields = ("title",)


@admin.register(ServiceInformation)
class ServiceInformationAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "title",
        "price",
        "discount",
    )
    list_filter = ("title",)
    search_fields = ("title",)
