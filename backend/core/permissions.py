from rest_framework.permissions import BasePermission, IsAuthenticated


class IsAuthenticated(IsAuthenticated):
    """Проверка пользователя на администратора."""

    message = "Учетные данные не были предоставлены."


class IsAdmin(BasePermission):
    """Проверка пользователя на администратора."""

    message = "Доступ разрешён только администратору."

    def has_permission(self, request, view):
        return getattr(request.user, "is_superuser", False)


class IsManager(BasePermission):
    """Проверка пользователя на группу Managers."""

    message = "Доступ разрешён только менеджеру."

    def has_permission(self, request, view):
        return request.user.groups.filter(name="Managers").exists()


class IsAdminOrManager(BasePermission):
    """Проверка пользователя на администратора или на группу Manager."""

    message = "Доступ разрешён только администратору и менеджеру."

    def has_permission(self, request, view):
        return IsAdmin.has_permission(self, request, view) or IsManager.has_permission(self, request, view)


class IsBanned(BasePermission):
    """Проверка пользователя наличие бана."""

    message = "Вы забанены и у вас нет доступа к этому ресурсу."

    def has_permission(self, request):
        return not request.user.is_banned


class IsOwnerOrAdmin(BasePermission):
    """Проверка пользователя владельца или на администратора."""

    message = "Доступ разрешён только владельцу или администратору."

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_superuser
            or (request.user.is_client and request.user == obj.client.user)
            or (request.user.is_employee and request.user == obj.doctor.user)
        )
