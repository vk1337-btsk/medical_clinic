import json

from apps.catalog.models import ServiceInformation, ServiceСategories
from apps.clients.models import Clients, RegistredServices
from apps.employees.models import Employees
from apps.users.models import Users
from config.settings import BASE_DIR
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.db import connection


DICT_FIXTURES = {
    "groups": {"name": "001_groups", "queryset": Group},
    "permissions": {"name": "002_permissions", "queryset": Permission},
    "users": {"name": "003_users", "queryset": Users},
    "clients": {"name": "004_clients", "queryset": Clients},
    "employees": {"name": "005_employees", "queryset": Employees},
    "service_categories": {"name": "006_service_categories", "queryset": ServiceСategories},
    "service_information": {"name": "007_service_information", "queryset": ServiceInformation},
    "register_services": {"name": "008_register_services", "queryset": RegistredServices},
}


class Command(BaseCommand):
    help = "Кастомная команда для заполнения таблиц в БД"

    @staticmethod
    def read_fixtures_json(filename: str) -> list:
        """Retrieve data from a fixture file in JSON format"""
        with open(f"{BASE_DIR}/fixtures/{filename}.json", encoding="UTF-8") as file:
            data = json.load(file)
        return data

    def fill_table_permissions(self):
        """Fill the Permissions table with data"""
        with connection.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE auth_permission RESTART IDENTITY CASCADE;")
        # self.stdout.write(Permission.objects.all())

        permissions_data = Command.read_fixtures_json(DICT_FIXTURES["permissions"]["name"])
        permissions = []
        for permission in permissions_data:
            content_type_id = permission["fields"]["content_type"]
            content_type = ContentType.objects.get(id=content_type_id)
            permissions.append(
                Permission(
                    name=permission["fields"]["name"],
                    content_type=content_type,
                    codename=permission["fields"]["codename"],
                )
            )

        Permission.objects.bulk_create(permissions)

    def fill_table_groups(self):
        """Fill the Groups table with data"""
        with connection.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE auth_group RESTART IDENTITY CASCADE;")
            cursor.execute("TRUNCATE TABLE auth_group_permissions RESTART IDENTITY CASCADE;")

        groups_data = Command.read_fixtures_json(DICT_FIXTURES["groups"]["name"])
        groups = []
        group_permissions = []

        for group in groups_data:
            group_instance = Group(name=group["fields"]["name"])
            group_instance.save()
            groups.append(group_instance)

            permission_ids = group["fields"]["permissions"]
            group_permissions.append((group_instance, permission_ids))

        for group_instance, permission_ids in group_permissions:
            permissions = Permission.objects.filter(id__in=permission_ids)
            group_instance.permissions.set(permissions)

    def handle(self, *args, **kwargs):

        self.stdout.write("Заполняем все таблицы...")

        self.stdout.write('Заполняем таблицу "permissions"...')
        self.fill_table_permissions()
        self.stdout.write(self.style.SUCCESS('Таблица "permissions" успешно заполнена...'))

        self.stdout.write('Заполняем таблицу "groups"...')
        self.fill_table_groups()
        self.stdout.write(self.style.SUCCESS('Таблица "groups" успешно заполнена...'))
