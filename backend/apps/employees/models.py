from apps.users.models import Users
from django.db.models import (
    CASCADE,
    CharField,
    DurationField,
    Model,
    OneToOneField,
    PositiveIntegerField,
)
from django.db.models.signals import pre_save
from django.dispatch import receiver


NULLABLE = {"null": True, "blank": True}


class Employees(Model):

    user = OneToOneField(Users, on_delete=CASCADE, related_name="employee", db_comment="Работник", **NULLABLE)
    id_employee = PositiveIntegerField(verbose_name="ID работника", db_comment="ID работника")
    job_title = CharField(max_length=255, verbose_name="Должность работника", db_comment="Должность работника")
    specializations = CharField(max_length=255, verbose_name="Специализация", db_comment="Специализация")
    experience = DurationField(verbose_name="Опыт работы", db_comment="Опыт работы")
    education = CharField(max_length=255, verbose_name="Образование", db_comment="Образование")

    def __str__(self):
        return f"{self.user} {self.id_employee}"

    class Meta:
        verbose_name = "Работник"
        verbose_name_plural = "Работники"
        db_table = "_us_employees"
        db_table_comment = "Работники"
        ordering = ["id_employee"]
        unique_together = ["id_employee"]


@receiver(pre_save, sender=Users)
def validate_user(sender, instance, **kwargs):
    instance.clean()
