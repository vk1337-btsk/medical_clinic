from apps.users.apps import UsersConfig
from django.urls import include, path


app_name = UsersConfig.name


urlpatterns = [
    path("", include("djoser.urls")),  # URL для действий пользователя
    path("users/", include("djoser.urls.jwt")),  # Настроенные URL для токенов
]
