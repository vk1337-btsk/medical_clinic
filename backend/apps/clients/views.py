from apps.clients.models import RegistredServices
from apps.clients.serializers.reg_services import RegistredServiceSerializer
from core.permissions import IsAdmin, IsAuthenticated, IsOwnerOrAdmin
from django.db.models import Q
from rest_framework import viewsets


class RegisterServiceViewSet(viewsets.ModelViewSet):
    """ViewSet для управления просмотра и управления зарегистрированными услугами."""

    serializer_class = RegistredServiceSerializer

    def get_permissions(self):
        if self.action in "list":
            permission_classes = [IsAuthenticated]
        elif self.action == "retrieve":
            permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
        elif self.action == "destroy":
            permission_classes = [IsAdmin]
        else:
            permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        queryset = RegistredServices.objects.none()

        if self.action == "list":
            if user.is_superuser:
                queryset = RegistredServices.objects.all().order_by("-date_services")
            elif user.is_client and not user.is_employee:
                queryset = RegistredServices.objects.filter(client=user.client.pk).order_by("-date_services")
            elif user.is_employee and not user.is_client:
                queryset = RegistredServices.objects.filter(doctor=user.employee.pk).order_by("-date_services")
            elif user.is_client and user.is_employee:
                queryset = RegistredServices.objects.filter(
                    Q(client=user.client.pk) | Q(doctor=user.employee.pk)
                ).order_by("-date_services")
        else:
            queryset = RegistredServices.objects.all()

        return queryset

    def get_serializer_context(self):
        return {"request": self.request}
