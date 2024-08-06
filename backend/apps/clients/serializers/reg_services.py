import datetime

from apps.catalog.models import ServiceInformation
from apps.catalog.serializers import ServiceInfoSerializers
from apps.clients.models import RegistredServices
from apps.employees.models import Employees
from apps.employees.serializers import EmployeeSerializer
from django.utils import timezone
from rest_framework import serializers


class RegistredServiceSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра записи клиента на оказание услуги."""

    info_service = serializers.SerializerMethodField()
    info_doctor = serializers.SerializerMethodField()

    class Meta:
        model = RegistredServices
        fields = [
            "pk",
            "client",
            "service",
            "info_service",
            "date_services",
            "doctor",
            "info_doctor",
            "status_service",
            "status_paid",
            "is_analyz",
            "is_vizit",
        ]

    def get_info_service(self, obj):
        info_service = ServiceInformation.objects.get(pk=obj.service.pk)
        my_data = ServiceInfoSerializers(info_service, context=self.context).data
        return my_data

    def get_info_doctor(self, obj):
        info_doctor = Employees.objects.get(pk=obj.doctor.pk)
        my_data = EmployeeSerializer(info_doctor, context=self.context).data
        return my_data


class CreateRegistredServiceSerializer(RegistredServiceSerializer):
    """Сериализатор для записи клиента на оказание услуги."""

    def validate_date_services(self, value):
        """Валидация даты записи услуги"""
        dt = datetime.datetime.isoformat(value)
        iso_dt = datetime.datetime.fromisoformat(dt)

        if iso_dt <= timezone.now():
            raise serializers.ValidationError("Дата записи не может быть на сейчас или в прошлом.")
        return value


class UpdateRegistredServiceSerializer(RegistredServiceSerializer):
    """Сериализатора для внесения изменений в запись"""

    class Meta(RegistredServiceSerializer.Meta):
        read_only_fields = ["status_paid"]

    def validate_date_services(self, value):
        """Валидация даты записи услуги"""
        dt = datetime.datetime.isoformat(value)
        iso_dt = datetime.datetime.fromisoformat(dt)

        if iso_dt <= timezone.now():
            raise serializers.ValidationError("Дата записи не может быть на сейчас или в прошлом.")
        return value

    def validate_status_paid(self, value):
        """Запретить изменение status_paid"""

        instance = self.instance
        if instance and value != instance.status_paid:
            raise serializers.ValidationError("Нельзя менять статус оплаты.")
        return value

    def update(self, instance, validated_data):
        validated_data.pop("status_paid", None)  # Удаляем status_paid из данных для обновления
        return super().update(instance, validated_data)
