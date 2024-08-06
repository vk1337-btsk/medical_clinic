import os
from django.core.management.base import BaseCommand
from django.core.serializers import serialize
from apps.catalog.models import ServiceInformation, ServiceСategories
from apps.clients.models import Clients, RegistredServices
from django.contrib.auth.models import Group, Permission
from apps.users.models import Users
from apps.employees.models import Employees


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
    help = "Создаёт фикстуры из БД"

    def handle(self, *args, **kwargs):

        for data in DICT_FIXTURES.values():

            name_file = data["name"]
            queryset = data["queryset"]

            fixture_path = os.path.join("fixtures", f"{name_file}.json")

            data_from_db = serialize("json", queryset.objects.all(), indent=4)

            with open(fixture_path, "w", encoding="utf-8") as f:
                f.write(data_from_db)

            self.stdout.write(self.style.SUCCESS(f"Фикстура сохранена в {fixture_path}"))
