from apps.catalog.models import ServiceInformation
from apps.employees.models import Employees
from apps.users.models import Users
from django.db.models import (
    CASCADE,
    DO_NOTHING,
    BooleanField,
    CharField,
    DateField,
    DateTimeField,
    ForeignKey,
    IntegerField,
    Model,
    OneToOneField,
    TextChoices,
)
from django.dispatch import receiver
from django.utils.translation import gettext
from django.db.models.signals import pre_save


NULLABLE = {"null": True, "blank": True}


class Clients(Model):

    user = OneToOneField(Users, on_delete=CASCADE, related_name="client", db_comment="Клиент", **NULLABLE)
    passport_id = IntegerField(verbose_name="Данные паспорта", db_comment="Даннаые паспорта")
    passport_date = DateField(verbose_name="Дата выдачи паспорта", db_comment="Дата выдачи паспорта")
    country = CharField(max_length=255, verbose_name="Страна", db_comment="Страна", **NULLABLE)
    city = CharField(max_length=255, verbose_name="Город", db_comment="Город", **NULLABLE)
    street = CharField(max_length=255, verbose_name="Улица", db_comment="Улица", **NULLABLE)
    blood_group = CharField(max_length=2, verbose_name="Группа крови", db_comment="Группа крови", **NULLABLE)

    def __str__(self):
        return f"{self.user} {self.passport_id}"

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        db_table = "_us_clients"
        db_table_comment = "Клиенты"
        ordering = ["passport_id"]
        unique_together = ["passport_id"]


@receiver(pre_save, sender=Users)
def validate_user(sender, instance, **kwargs):
    instance.clean()


class RegistredServices(Model):
    """Модель для забронированной/зарегистрированной услуги"""

    class StatusServices(TextChoices):
        CREATED = "CR", gettext("Создана")
        PROCESSED = "PR", gettext("В процессе")
        DONE = "DO", gettext("Выполнена")
        CANCELED = "CA", gettext("Отменена")

    client = ForeignKey(Clients, on_delete=CASCADE, related_name="client", verbose_name="Клиент", db_comment="Клиент")
    service = ForeignKey(
        ServiceInformation, on_delete=DO_NOTHING, related_name="service", verbose_name="Услуга", db_comment="Услуга"
    )
    date_services = DateTimeField(verbose_name="Дата записи", db_comment="Дата и время записи услуги")
    doctor = ForeignKey(Employees, on_delete=CASCADE, verbose_name="Доктор", db_comment="Доктор", **NULLABLE)
    status_service = CharField(
        max_length=15, default=StatusServices.CREATED, verbose_name="Статус услуги", db_comment="Статус услуги"
    )
    status_paid = BooleanField(verbose_name="Статус оплаты", db_comment="Статус оплаты", **NULLABLE)
    is_analyz = BooleanField(verbose_name="Флаг анализа", db_comment="Флаг анализа", **NULLABLE)
    is_vizit = BooleanField(verbose_name="Флаг визита", db_comment="Флаг визита", **NULLABLE)

    def __str__(self):
        return f"{self.client} {self.service} {self.date_services} {self.status_service}"

    class Meta:
        verbose_name = "Зарегистрированная услуга"
        verbose_name_plural = "Зарегистрированные услуги"
