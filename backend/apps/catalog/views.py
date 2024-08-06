from apps.catalog.models import ServiceInformation, ServiceСategories
from apps.catalog.serializers import (
    CategorySerializer,
    DoctorsSerializer,
    ServiceInfoSerializers,
)
from apps.employees.models import Employees
from core.permissions import IsAdminOrManager, IsAuthenticated
from rest_framework import response, views, viewsets
from rest_framework.permissions import AllowAny


class CatalogListAPIView(views.APIView):
    """Представление для вывода главной страницы каталога услуг и докторов."""

    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        categories = ServiceСategories.objects.all()
        serializer = CategorySerializer(categories, many=True, context={"request": request})
        return response.Response(
            {
                "list_categories": serializer.data,
            }
        )


class CategoriesViewSet(viewsets.ModelViewSet):
    """ViewSet для управления категориями услуг."""

    queryset = ServiceСategories.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsAdminOrManager]
        return [permission() for permission in permission_classes]

    def get_serializer_context(self):
        return {"request": self.request}


class ServicesInfoViewSet(viewsets.ModelViewSet):
    """ViewSet для управления информацией об услугах."""

    queryset = ServiceInformation.objects.all()
    serializer_class = ServiceInfoSerializers

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminOrManager]
        return [permission() for permission in permission_classes]

    def get_serializer_context(self):
        return {"request": self.request}


class DoctorsInfoViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для управления информацией работающих докторах."""

    queryset = Employees.objects.all()
    serializer_class = DoctorsSerializer
    permission_classes = [AllowAny]

    def get_serializer_context(self):
        return {"request": self.request}
