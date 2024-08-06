import datetime
import random

import factory
import pytest
import pytz
from requests import session
from apps.catalog.models import ServiceInformation, ServiceСategories
from apps.clients.models import Clients, RegistredServices
from apps.employees.models import Employees
from apps.users.management.commands import my_loaddata
from apps.users.models import Users
from django.contrib.auth.models import Group
from faker import Faker
from rest_framework.test import APIClient


COUNT_CATEGORIES = 5
COUNT_SERVICES = 5
COUNT_CLIENTS = 5
COUNT_EMPLOYEES = 5
COUNT_MANAGERS = 1
COUNT_ADMINS = 1
SPECIFIC_PAIRS = [
    ("user_client1", "user_employee1"),
    ("user_client1", "user_employee2"),
    ("user_client2", "user_employee1"),
    ("user_client2", "user_employee2"),
    ("user_client_employee1", "user_manager"),
]

fake = Faker()


class UsersFactory(factory.django.DjangoModelFactory):
    """Фабрика для создания пользователей."""

    class Meta:
        model = Users
        skip_postgeneration_save = True

    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall("set_password", "password")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    middle_name = factory.Faker("first_name")
    date_birthday = factory.Faker("date_of_birth")
    phone = factory.LazyAttribute(lambda x: fake.phone_number()[:15])
    is_client = False
    is_employee = False
    is_active = True
    is_staff = False
    is_superuser = True


class EmployeesFactory(factory.django.DjangoModelFactory):
    """Фабрика для создания пользовтелей-работников."""

    class Meta:
        model = Employees
        skip_postgeneration_save = True

    user = factory.SubFactory(UsersFactory, is_employee=True)
    id_employee = factory.Sequence(lambda n: n)
    job_title = factory.Faker("job")
    specializations = factory.Faker("word")
    experience = factory.Faker("time_delta")
    education = factory.Faker("word")


class ClientsFactory(factory.django.DjangoModelFactory):
    """Фабрика для создания пользовтелей-клиентов."""

    class Meta:
        model = Clients
        skip_postgeneration_save = True

    user = factory.SubFactory(UsersFactory, is_client=True)
    passport_id = factory.Faker("random_number", digits=8)
    passport_date = factory.Faker("date")
    country = factory.Faker("country")
    city = factory.Faker("city")
    street = factory.Faker("street_address")
    blood_group = factory.Faker("random_element", elements=["A", "B", "AB", "O"])


class СategoriesFactory(factory.django.DjangoModelFactory):
    """Фабрика для создания категорий услуг."""

    class Meta:
        model = ServiceСategories
        skip_postgeneration_save = True

    title = factory.Sequence(lambda n: f"Категория № {n}.")
    description = factory.Faker("text")


class ServiceInformationFactory(factory.django.DjangoModelFactory):
    """Фабрика для создания оказываемых услуг."""

    class Meta:
        model = ServiceInformation
        skip_postgeneration_save = True

    title = factory.Faker("sentence", nb_words=4)
    general_info = factory.Faker("text")
    additional_info = factory.Faker("text")
    duration = factory.Faker("time_delta")
    preparation = factory.Faker("paragraph")
    price = factory.Faker("random_int", min=1000, max=10000)
    discount = factory.Faker("random_int", min=0, max=100)


class RegistredServicesFactory(factory.django.DjangoModelFactory):
    """Фабрика для создания зарегистрированных услуг пользователя"""

    class Meta:
        model = RegistredServices
        skip_postgeneration_save = True

    client = factory.SubFactory(ClientsFactory)
    service = factory.SubFactory(ServiceInformationFactory)
    date_services = factory.LazyFunction(
        lambda: fake.date_time_between(start_date="-1y", end_date="+1y", tzinfo=pytz.UTC)
    )
    doctor = factory.SubFactory(EmployeesFactory)
    status_service = factory.LazyFunction(lambda: fake.random_element(RegistredServices.StatusServices.values))
    status_paid = factory.Faker("boolean")
    is_analyz = factory.Faker("boolean")
    is_vizit = factory.Faker("boolean")


@pytest.fixture
def specific_pairs(
    user_client1,
    user_client2,
    user_employee1,
    user_employee2,
    user_client_employee1,
    user_manager,
):
    """Фикстура для возврата specific_pairs с реальными объектами пользователей."""
    return [
        (user_client1, user_employee1),
        (user_client1, user_employee2),
        (user_client2, user_employee1),
        (user_client2, user_employee2),
        (user_client_employee1, user_manager),
    ]


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def groups_and_permissions(django_db_blocker):
    """Фикстура для создания Group и Permission в тестовой базе."""

    with django_db_blocker.unblock():
        try:
            command = my_loaddata.Command()
            command.handle()
        except Exception as e:
            pytest.fail(f"Ошибка при загрузке данных: {e}")


@pytest.fixture
def create_user_with_role(groups_and_permissions):
    """Универсальная фикстура для создания пользователя с определённой ролью."""

    def _create_user_with_role(roles: list):
        user = UsersFactory.create()

        for role in roles:
            if role == "Managers":
                user.is_employee = True
                user.is_superuser = False
                role_instance = EmployeesFactory.create(user=user)
                user.employee = role_instance
            elif role == "Employees":
                user.is_employee = True
                user.is_superuser = False
                role_instance = EmployeesFactory.create(user=user)
                user.employee = role_instance
            elif role == "Clients":
                user.is_client = True
                user.is_superuser = False
                role_instance = ClientsFactory.create(user=user)
                user.client = role_instance
            elif role == "Admins":
                user.is_staff = True
            else:
                pytest.fail(f"Неизвестная роль: {role}")

            try:
                group = Group.objects.get(name=role)
            except Group.DoesNotExist:
                pytest.fail(f"Группы '{role}' не существует.")

            user.groups.set([group])
            user.user_permissions.set(group.permissions.all())

        user.save()

        return user

    return _create_user_with_role


@pytest.fixture
def create_categories_and_services():
    """Универсальная фикстура для создания списка категорий услуг."""

    def _create_categories(count_categories: int = COUNT_CATEGORIES, count_services: int = COUNT_SERVICES):

        categories = СategoriesFactory.create_batch(count_categories)

        services = []
        for category in categories:
            service_information = ServiceInformationFactory.create_batch(count_services)
            for service in service_information:
                service.categories.set([category])
                service.save()
            services.extend(service_information)

        return [categories, services]

    return _create_categories


@pytest.fixture
def create_employees(create_user_with_role):
    """Универсальная фикстура для создания списка пользователей работников."""

    def _create_employees(count_employees: int = COUNT_EMPLOYEES):

        employees = []
        for _ in range(count_employees):
            employee = create_user_with_role(["Employees"])
            employee.save()
            employees.append(employee)

        return employees

    return _create_employees


@pytest.fixture
def create_clients(create_user_with_role):
    """Универсальная фикстура для создания списка пользователей клиентов."""

    def _create_clients(count_clients: int = COUNT_CLIENTS):

        clients = []
        for _ in range(count_clients):
            client = create_user_with_role(["Clients"])
            client.save()
            clients.append(create_user_with_role(["Clients"]))

        return clients

    return _create_clients


@pytest.fixture
def anonymous_user():
    """Фикстура для создания неавторизованного пользователя."""

    return APIClient()


@pytest.fixture
def user_admin(create_user_with_role):
    """Фикстура для создания пользователя-администратора."""

    admin = create_user_with_role(roles=["Admins"])
    admin.save()

    return admin


@pytest.fixture
def user_manager(create_user_with_role):
    """Фикстура для создания пользователя-менедежра."""

    manager = create_user_with_role(roles=["Managers"])
    manager.save()

    return manager


@pytest.fixture
def user_employee1(create_user_with_role):
    """Фикстура для создания пользователя-работника 1."""

    employee = create_user_with_role(roles=["Employees"])
    employee.save()

    return employee


@pytest.fixture
def user_employee2(create_user_with_role):
    """Фикстура для создания пользователя-работника 2."""

    employee = create_user_with_role(roles=["Employees"])
    employee.save()

    return employee


@pytest.fixture
def user_client1(create_user_with_role):
    """Фикстура для создания пользователя-клиента 1."""

    client = create_user_with_role(roles=["Clients"])
    client.save()

    return client


@pytest.fixture
def user_client2(create_user_with_role):
    """Фикстура для создания пользователя-клиента 2."""

    client = create_user_with_role(roles=["Clients"])
    client.save()

    return client


@pytest.fixture
def user_client_employee1(create_user_with_role):
    """Фикстура для создания пользователя клиента и работника 1."""

    client_employee = create_user_with_role(roles=["Clients", "Employees"])
    client_employee.save()

    return client_employee


@pytest.fixture
def user_client_employee2(create_user_with_role):
    """Фикстура для создания пользователя клиента и работника 2."""

    client_employee = create_user_with_role(roles=["Clients", "Employees"])
    client_employee.save()

    return client_employee


@pytest.fixture
def category_service_info(create_categories_and_services):
    """Фикстура для создания 1 категорий услуг и включённую в неё 1 услугу."""

    return create_categories_and_services(1, 1)


@pytest.fixture
def categories_services_info(create_categories_and_services):
    """Фикстура для создания определённого количества категорий услуг и включённых в неё услуг."""

    return create_categories_and_services()


@pytest.fixture
def employees(create_employees):
    """Фикстура для создания списка пользователей-работников."""

    return create_employees()


@pytest.fixture
def clients(create_clients):
    """Фикстура для создания списка пользователей-работников."""

    return create_clients()


@pytest.fixture
def create_register_service():
    """Универсальная фикстура для регистрации услуги у клиента."""

    def _create_register_service(user_client, user_employee, service):

        register_service = RegistredServicesFactory.create(
            client=user_client.client, doctor=user_employee.employee, service=service
        )
        return register_service

    return _create_register_service


@pytest.fixture
def register_service(create_register_service, user_client1, user_employee1, category_service_info):
    """Фикстура для создания 1 зарегистрированной услуги у 1 клиента и работника."""

    categories, services = category_service_info
    service = services[0]

    return create_register_service(user_client1, user_employee1, service)


@pytest.fixture
def register_services(
    create_register_service,
    clients,
    employees,
    specific_pairs,
    categories_services_info,
):
    """Фикстура для создания пользователей клиента и работника, категории услуг, услуг и зарегистрированной услуги."""

    register_services = []
    categories, services = categories_services_info

    for client, employee in specific_pairs:
        service = random.choice(services)
        register_services.append(create_register_service(client, employee, service))

    for client in clients:
        random_service = random.choice(services)
        random_employee = random.choice(employees)
        register_services.append(create_register_service(client, random_employee, random_service))

    return register_services
