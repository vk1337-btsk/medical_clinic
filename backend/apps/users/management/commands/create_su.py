import os

from apps.users.models import Users
from django.core.management import BaseCommand
from dotenv import load_dotenv


load_dotenv()


class Command(BaseCommand):

    @staticmethod
    def create_superuser():
        user = Users.objects.create(
            email=os.environ.get("EMAIL"),
            username=os.environ.get("USERNAME"),
            first_name=os.environ.get("FIRST_NAME"),
            last_name=os.environ.get("LAST_NAME"),
            middle_name=os.environ.get("MIDDLE_NAME"),
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )
        user.set_password(os.environ.get("PASSWORD"))
        user.save()

    def handle(self, *args, **options):
        self.create_superuser()
