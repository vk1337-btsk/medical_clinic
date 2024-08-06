import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv


# Getting the base project directory
BASE_DIR = Path(__file__).resolve().parent.parent


# Getting data from .env
if os.getenv("ENVIRONMENT") == "docker":
    env_file = "../.env.docker"
else:
    env_file = "../.env.local"
dotenv_path = BASE_DIR / env_file

if dotenv_path.exists():
    load_dotenv(dotenv_path)


# Settings Django project
SECRET_KEY = os.environ.get("SECRET_KEY", "django-bad-secret-key")
DEBUG = os.environ.get("DEBUG", "False") == "True"


# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # System apps
    "django_celery_beat",  # Celery 
    "rest_framework",  # Django Rest Framework
    "rest_framework_simplejwt",  # Django Rest Framework JWT для авторизации
    "corsheaders",  # Corsheaders
    "djoser",  # Djoser для аутентификации
    "drf_yasg",  # Swagger и ReDoc
    # My apps
    "apps.catalog",
    "apps.users",
    "apps.clients",
    "apps.employees",
]


# Settings middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # System middleware
    "corsheaders.middleware.CorsMiddleware",
]


# Settings CORS and security
CORS_ALLOW_ALL_ORIGINS = True
ALLOWED_HOSTS = ["*"]
ROOT_URLCONF = "config.urls"


# Settings templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Settings Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        # "ENGINE": f"django.db.backends.{os.environ.get('POSTGRES_ENGINE', 'postgresql')}",
        "NAME": os.environ.get("POSTGRES_DB", "medical_clinic"),
        "USER": os.environ.get("POSTGRES_USER", "postgres"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "SecretPassword"),
        "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
        "PORT": os.environ.get("POSTGRES_PORT", 5432),
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
LANGUAGE_CODE = "ru"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# Settings static files (CSS, JavaScript, Images) and media files
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Settings Users
AUTH_USER_MODEL = "users.Users"


# Settings REST API
REST_FRAMEWORK = {
    # Класс по умолчанию для авторизации
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    # Класс по умолчанию для прав
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}


# Settings Authentification
DJOSER = {
    # Основные настройки
    "LOGIN_FIELD": "email",  # Название поля в модели пользователя для авторизации
    "USER_ID_FIELD": "id",  # Название уникального поля в модели пользователя, используемое в качестве идентификатора
    "TOKEN_MODEL": "rest_framework.authtoken.models.Token",  # Указывает модель токена, используемого djoser
    "HIDE_USERS": True,  # В случае запроса обычным пользователем списка пользователей, вернётся только пользователь
    # Регистрация и активация пользователя
    "USER_CREATE_PASSWORD_RETYPE": True,  # Отправлять ли поле 're_password" (подтверждение пароля) при регистрации
    "SEND_ACTIVATION_EMAIL": True,  # Отправлять ли ссылку подтверждения при создании аккаунта и изменении почты
    "SEND_CONFIRMATION_EMAIL": True,  # Отправлять ли пользователю письмо с подтверждением регистрации
    "ACTIVATION_URL": "#/activate/{uid}/{token}",  # Эндпоинт для активации аккаунта пользователя
    # Сброс пароля
    "PASSWORD_CHANGED_EMAIL_CONFIRMATION": True,  # Отправлять ли ссылку с подтверждением для смены пароля
    "SET_PASSWORD_RETYPE": True,  # Отправлять ли поле 're_new_password " (повтор password) при смене пароля
    "PASSWORD_RESET_CONFIRM_RETYPE": True,  # Отправлять ли поле 're_new_password " (повтор password) при подтверждении смены пароля
    "PASSWORD_RESET_CONFIRM_URL": "#/password-reset/{uid}/{token}",  # Эндпоинт для сброса пароля
    "PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND": False,  # При сбросе пароля, если введён несуществующий в базе пароль будет сообщение: Пользователь с указанным адресом электронной почты не существует
    "LOGOUT_ON_PASSWORD_CHANGE": True,  # При смене пароля происходит выход из аккаунта
    # Смена email
    "USERNAME_CHANGED_EMAIL_CONFIRMATION": False,  # Отправлять ли ссылку с подтверждением для смены имени
    "SET_USERNAME_RETYPE": True,  # Отправлять ли поле 're_new_email" (повтор email) при смене username
    "USERNAME_RESET_CONFIRM_RETYPE": True,  # Отправлять ли поле 're_new_email" (повтор email) при подтверждении смены email
    "USERNAME_RESET_CONFIRM_URL": "#/username-reset/{uid}/{token}",  # Эндпоинт для сброса email
    "USERNAME_RESET_SHOW_EMAIL_NOT_FOUND": False,  # При смене email, если введён несуществующий email будет сообщение: Пользователь с указанным адресом электронной почты не существует
    # Настройки сериализаторов классов
    "SERIALIZERS": {
        # "user_create_password_retype": "djoser.serializers.UserCreatePasswordRetypeSerializer",
        "user_create_password_retype": "apps.users.serializers.users.UserRegistrationSerializer",  # Сериализатор для регистрации
        # "user_create": "apps.users.serializers.users.UserRegistrationSerializer",
        "user_create": "apps.users.serializers.users.UserRegistrationSerializer",  # Сериализатор для регистрации
        # "user": "djoser.serializers.UserSerializer",
        "user": "apps.users.serializers.users.UserDetailSerializer",  # Сериализатор для просмотра пользователя
        # "current_user": "djoser.serializers.UserSerializer",
        "current_user": "apps.users.serializers.users.CurrentUserDetailSerializer",  # Сериализатор для действий текущего пользователя
        "activation": "djoser.serializers.ActivationSerializer",
        "password_reset": "djoser.serializers.SendEmailResetSerializer",
        "password_reset_confirm": "djoser.serializers.PasswordResetConfirmSerializer",
        "password_reset_confirm_retype": "djoser.serializers.PasswordResetConfirmRetypeSerializer",
        "set_password": "djoser.serializers.SetPasswordSerializer",
        "set_password_retype": "djoser.serializers.SetPasswordRetypeSerializer",
        "set_username": "djoser.serializers.SetUsernameSerializer",
        "set_username_retype": "djoser.serializers.SetUsernameRetypeSerializer",
        "username_reset": "djoser.serializers.SendEmailResetSerializer",
        "username_reset_confirm": "djoser.serializers.UsernameResetConfirmSerializer",
        "username_reset_confirm_retype": "djoser.serializers.UsernameResetConfirmRetypeSerializer",
        "user_delete": "djoser.serializers.UserDeleteSerializer",
        "token": "djoser.serializers.TokenSerializer",
        "token_create": "djoser.serializers.TokenCreateSerializer",
    },
    # Настройки классов для работы с email
    "EMAIL": {
        "activation": "djoser.email.ActivationEmail",
        "confirmation": "djoser.email.ConfirmationEmail",
        "password_reset": "djoser.email.PasswordResetEmail",
        "password_changed_confirmation": "djoser.email.PasswordChangedConfirmationEmail",
        "username_changed_confirmation": "djoser.email.UsernameChangedConfirmationEmail",
        "username_reset": "djoser.email.UsernameResetEmail",
    },
    # Настройки прав для классов
    "PERMISSIONS": {
        "activation": ["rest_framework.permissions.AllowAny"],
        "password_reset": ["rest_framework.permissions.AllowAny"],
        "password_reset_confirm": ["rest_framework.permissions.AllowAny"],
        "set_password": ["djoser.permissions.CurrentUserOrAdmin"],
        "username_reset": ["rest_framework.permissions.AllowAny"],
        "username_reset_confirm": ["rest_framework.permissions.AllowAny"],
        "set_username": ["djoser.permissions.CurrentUserOrAdmin"],
        "user_create": ["rest_framework.permissions.AllowAny"],
        "user_delete": ["djoser.permissions.CurrentUserOrAdmin"],
        "user": ["djoser.permissions.CurrentUserOrAdmin"],
        "user_list": ["djoser.permissions.CurrentUserOrAdmin"],
        "token_create": ["rest_framework.permissions.AllowAny"],
        "token_destroy": ["rest_framework.permissions.IsAuthenticated"],
    },
    # Настройки сообщений
    "CONSTANTS": {
        "messages": "djoser.constants.Messages",
    },
    # Настройки социальной аутентификации
    "SOCIAL_AUTH_TOKEN_STRATEGY": "djoser.social.token.jwt.TokenStrategy",
    "SOCIAL_AUTH_ALLOWED_REDIRECT_URIS": [],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=30),  # Срок жизни acess-токена (было 5 минут)
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),  # Срок жизни refresh-токена (был 1 день)
    "ROTATE_REFRESH_TOKENS": False,  # При запросе нового acess-токен также будет возвращаться новый refresh-токен
    "BLACKLIST_AFTER_ROTATION": False,  # Черный список для refresh-токенов
    "UPDATE_LAST_LOGIN": False,  # Нужно ли обновлять поле last_login в при входе в систему (есть вопросы к безопасности)
    "ALGORITHM": "HS256",  # Алгоритм шифрования
    "SIGNING_KEY": SECRET_KEY,  # Ключ для подписи содержимого токенов (SECRET_KEY использовать не рекомендуется)
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_TYPES": ("Bearer",),  # Ключевый слова, которые будут искать в заголовке авторизации
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}


# Settings host-email
EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.yandex.ru")
EMAIL_PORT = os.environ.get("EMAIL_PORT", "smtp.yandex.ru")
EMAIL_USE_SSL = True
EMAIL_USE_TLS = False

EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "my_email@yandex.ru")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "SecretPassword")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
