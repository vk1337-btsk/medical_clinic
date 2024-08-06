from apps.clients.apps import ClientsConfig
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.clients.views import RegisterServiceViewSet

app_name = ClientsConfig.name


router_registered_services = DefaultRouter()
router_registered_services.register("history/service", RegisterServiceViewSet, basename="service")

urlpatterns = [
    path("me/service/", RegisterServiceViewSet.as_view({"post": "create"}), name="service-detail"),
    path("me/", include(router_registered_services.urls)),
]
