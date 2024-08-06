from datetime import timedelta

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q


NULLABLE = {"null": True, "blank": True}


class ServiceСategories(models.Model):
    """Модель категории оказываемой услуги."""

    title = models.CharField(
        max_length=255,
        verbose_name="Название категории услуг",
        db_comment="Название категории услуг",
    )
    description = models.TextField(
        verbose_name="Описание категории",
        db_comment="Описание категории услуг",
    )

    def __str__(self) -> str:
        return f"{self.title}"

    class Meta:
        verbose_name = "Категория услуги"
        verbose_name_plural = "Категории услуг"
        db_table = "_ca_categories"
        db_table_comment = "Справочная информация о категориях услуг"
        ordering = ["title"]
        unique_together = ["title"]


class ServiceInformation(models.Model):
    """Модель оказываемой услуги."""

    categories = models.ManyToManyField(
        ServiceСategories,
        related_name="categories",
        verbose_name="Категории услуги",
    )
    title = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Название услуги",
        db_comment="Название услуги",
    )
    general_info = models.TextField(
        verbose_name="Общая информация", db_comment="Общая информация об услуге", **NULLABLE
    )
    additional_info = models.TextField(
        verbose_name="Дополнительная информация",
        db_comment="Дополнительная информация об услуге",
        **NULLABLE,
    )
    duration = models.DurationField(
        default=timedelta(days=1),
        verbose_name="Продолжительность услуги",
        db_comment="Продолжительность оказания услуги",
    )
    preparation = models.TextField(
        verbose_name="Требования к подготовке",
        db_comment="Требования к подготовке оказания услуги",
        **NULLABLE,
    )
    price = models.PositiveIntegerField(
        verbose_name="Стоимость, руб.",
        db_comment="Стоимость, руб.",
    )
    discount = models.IntegerField(
        default=0,
        verbose_name="Скидка, проценты",
        db_comment="Скидка, проценты",
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    def __str__(self):
        return f"Название: {self.title}; Стоимость: {self.price}; Скидка: {self.discount}"

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
        db_table = "_ca_service_info"
        db_table_comment = "Справочная информация о предоставляемой услуге"
        ordering = ["title"]
        unique_together = ["title"]
