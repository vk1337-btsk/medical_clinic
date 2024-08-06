from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db.models import BooleanField, CharField, DateField, EmailField, ImageField


NULLABLE = {"null": True, "blank": True}


class CustomUserManager(BaseUserManager):
    """Custom user model manager where email is the unique identifiers"""

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class Users(AbstractUser, PermissionsMixin):

    objects = CustomUserManager()
    username = None

    email = EmailField(max_length=255, unique=True, verbose_name="Электронная почта", db_comment="Электронная почта")
    first_name = CharField(max_length=255, verbose_name="Имя пользователя", db_comment="Имя пользователя")
    last_name = CharField(max_length=255, verbose_name="Фамилия пользователя", db_comment="Фамилия пользователя")
    middle_name = CharField(max_length=255, verbose_name="Отчество пользователя", db_comment="Отчество пользователя")
    date_birthday = DateField(**NULLABLE, verbose_name="День рождения", db_comment="День рождения")
    phone = CharField(max_length=15, verbose_name="Телефон", db_comment="Телефон", **NULLABLE)
    avatar = ImageField(
        default="media/users/avatar/avatar_default.png",
        upload_to="users/avatar/",
        verbose_name="Аватар пользователя",
        db_comment="Аватар пользователя",
        **NULLABLE
    )
    is_client = BooleanField(default=False, verbose_name="Флаг клиента", db_comment="Флаг клиента")
    is_employee = BooleanField(default=False, verbose_name="Флаг работника", db_comment="Флаг работника")

    is_banned = BooleanField(default=False, verbose_name="Флаг бана", db_comment="Флаг бана")
    is_active = BooleanField(default=True, verbose_name="Флаг активности", db_comment="Флаг активности")
    is_staff = BooleanField(default=False, verbose_name="Флаг персонала", db_comment="Флаг персонала")
    is_superuser = BooleanField(default=False, verbose_name="Флаг админа", db_comment="Флаг админа")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        db_table = "_us_users"
        db_table_comment = "Пользователи"
        ordering = ["pk"]

    def __str__(self):
        return self.email

    def clean(self):
        super().clean()
        if not self.is_superuser and (not self.is_client and not self.is_employee):
            raise ValidationError("Пользователь должен быть либо клиентом, либо работником, либо и тем, и другим.")
