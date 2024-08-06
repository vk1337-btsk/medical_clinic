from apps.catalog.apps import CatalogConfig
from apps.catalog.views import (
    CatalogListAPIView,
    CategoriesViewSet,
    DoctorsInfoViewSet,
    ServicesInfoViewSet,
)
from django.urls import include, path
from rest_framework.routers import DefaultRouter


app_name = CatalogConfig.name

router_services = DefaultRouter()
router_services.register("service", ServicesInfoViewSet, basename="service")

router_categories = DefaultRouter()
router_categories.register("category", CategoriesViewSet, basename="category")

router_doctors = DefaultRouter()
router_doctors.register("doctor", DoctorsInfoViewSet, basename="doctor")


urlpatterns = [
    path("", CatalogListAPIView.as_view(), name="catalog"),
    path("", include(router_categories.urls)),
    path("", include(router_services.urls)),
    path("", include(router_doctors.urls)),
]
