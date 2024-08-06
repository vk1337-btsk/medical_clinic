from apps.catalog.models import ServiceInformation, ServiceСategories
from apps.employees.models import Employees
from rest_framework import serializers


class ServiceInfoSerializers(serializers.ModelSerializer):
    """Сериализатор информации об услугах."""

    # url = serializers.HyperlinkedIdentityField(view_name="catalog:service_detail", lookup_field="pk")

    class Meta:
        model = ServiceInformation
        fields = (
            "pk",
            # "url",
            "categories",
            "title",
            "general_info",
            "additional_info",
            "preparation",
            "duration",
            "price",
            "discount",
        )


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий услуг."""

    services = ServiceInfoSerializers(required=False, many=True)

    class Meta:
        model = ServiceСategories
        fields = [
            "pk",
            "title",
            "description",
            # "url",
            "services",
        ]


class DoctorsSerializer(serializers.ModelSerializer):
    """Сериализатор работающих докторов."""

    class Meta:
        model = Employees
        fields = [
            "job_title",
            "specializations",
            "experience",
            "education",
        ]


class CatalogSerializer(serializers.Serializer):
    """Сериализатор каталога услуг и работающих докторов."""

    categories = serializers.SerializerMethodField()

    class Meta:
        fields = ["categories"]

    def get_categories(self, obj):
        categories = ServiceСategories.objects.all()
        return CategorySerializer(categories, many=True, context=self.context).data
