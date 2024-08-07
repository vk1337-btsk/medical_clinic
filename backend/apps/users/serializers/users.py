from apps.clients.serializers.clients import ClientSerializer
from apps.employees.serializers import EmployeeSerializer
from apps.users.models import Users
from core.messages import Messages
from djoser import serializers as djoser_serializers
from rest_framework import serializers as drf_serializers


class UserRegistrationSerializer(djoser_serializers.UserCreateSerializer):
    """Сериализатор регистрации пользователей"""

    password2 = drf_serializers.CharField(style={"input_type": "password"}, required=True, write_only=True)
    client = ClientSerializer(required=False, allow_null=True)
    employee = EmployeeSerializer(required=False, allow_null=True)

    class Meta:
        model = Users
        fields = [
            "email",
            "first_name",
            "last_name",
            "middle_name",
            "password",
            "password2",
            "date_birthday",
            "phone",
            "avatar",
            "is_client",
            "client",
            "is_employee",
            "employee",
        ]

    def validate(self, data):
        """Проводим валидацию данных"""

        password2 = data.pop("password2", None)

        if data.get("password") != password2:
            raise drf_serializers.ValidationError(Messages.MESSAGES_PASSWORD["not_match"])

        if data.get("is_client") is False and data.get("is_employee") is False:
            raise drf_serializers.ValidationError(Messages.MESSAGES_REGISTRATION["not_roles"])

        return data

    def create(self, validated_data):
        """Метод для сохранения нового пользователя"""

        client_data = validated_data.pop("client", None)
        employee_data = validated_data.pop("employee", None)

        user = super().create(validated_data)

        if user.is_client and client_data:
            self._create_client(user, client_data)

        if user.is_employee and employee_data:
            self._create_employee(user, employee_data)

        return user

    def _create_client(self, user, client_data):
        """Создает объект клиента"""

        client_serializer = ClientSerializer(data=client_data)
        if client_serializer.is_valid():
            client = client_serializer.save(user=user)
            user.client = client
            user.save()
        else:
            raise drf_serializers.ValidationError(client_serializer.errors)

    def _create_employee(self, user, employee_data):
        """Создает объект сотрудника"""

        employee_serializer = EmployeeSerializer(data=employee_data)
        if employee_serializer.is_valid():
            employee = employee_serializer.save(user=user)
            user.employee = employee
            user.save()
        else:
            raise drf_serializers.ValidationError(employee_serializer.errors)


class UserDetailSerializer(djoser_serializers.UserSerializer):

    class Meta:
        model = Users
        fields = [
            "id",
            "first_name",
            "last_name",
            "is_client",
            "is_employee",
        ]


class CurrentUserDetailSerializer(djoser_serializers.UserSerializer):
    client = ClientSerializer(required=False, allow_null=True)
    employee = EmployeeSerializer(required=False, allow_null=True)

    class Meta:
        model = Users
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "middle_name",
            "date_birthday",
            "is_client",
            "client",
            "is_employee",
            "employee",
        ]
