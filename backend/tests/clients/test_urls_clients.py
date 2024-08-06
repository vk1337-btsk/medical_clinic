import random
from datetime import datetime

import pytest
from apps.clients.models import RegistredServices
from core.permissions import IsAdmin, IsAuthenticated, IsOwnerOrAdmin
from django.urls import reverse
from tests.conftest import COUNT_CLIENTS


@pytest.mark.parametrize(
    "user,status_code,expected_count",
    [
        ("anonymous_user", 401, 0),
        ("user_manager", 200, 1),
        ("user_admin", 200, 5 + COUNT_CLIENTS),
        ("user_employee1", 200, 2),
        ("user_employee2", 200, 2),
        ("user_client1", 200, 2),
        ("user_client2", 200, 2),
        ("user_client_employee1", 200, 1),
    ],
)
@pytest.mark.django_db
def test_url_history_service_list(api_client, request, user, status_code, expected_count, register_services):
    """
    Тест для получения информации об истории услуг пользователя
    [GET] http://127.0.0.1:8000/api/me/history/
    """

    if user == "anonymous_user":
        client = request.getfixturevalue(user)
    else:
        user = request.getfixturevalue(user)
        api_client.force_authenticate(user=user)
        client = api_client

    response = client.get(reverse("clients:service-list"), format="json")

    assert response.status_code == status_code

    if status_code == 401:
        assert response.data["detail"] == IsAuthenticated.message

    elif status_code == 200:

        expected_services = [
            {
                "pk": service.pk,
                "client": service.client.pk,
                "doctor": service.doctor.pk,
                "service": service.service.pk,
                "date_services": service.date_services,
                "status_service": service.status_service,
                "status_paid": service.status_paid,
                "is_analyz": service.is_analyz,
                "is_vizit": service.is_vizit,
            }
            for service in register_services
            if user.is_superuser
            or (user.is_client and user.client.pk == service.client.pk)
            or (user.is_employee and user.employee.pk == service.doctor.pk)
            or (
                user.is_client
                and user.is_employee
                and (user.employee.pk == service.doctor.pk or user.client.pk == service.client.pk)
            )
        ]

        expected_services = sorted(expected_services, key=lambda x: x["date_services"], reverse=True)

        response_services = sorted(
            [
                {
                    "pk": service["pk"],
                    "client": service["client"],
                    "doctor": service["doctor"],
                    "service": service["service"],
                    "date_services": datetime.fromisoformat(service["date_services"]),
                    "status_service": service["status_service"],
                    "status_paid": service["status_paid"],
                    "is_analyz": service["is_analyz"],
                    "is_vizit": service["is_vizit"],
                }
                for service in response.data
            ],
            key=lambda x: x["date_services"],
            reverse=True,
        )

        assert len(response_services) == expected_count
        assert response_services == [el for el in expected_services[:expected_count]]


@pytest.mark.parametrize(
    "user,status_code_ok,status_code_not_ok",
    [
        ("anonymous_user", 401, 401),
        ("user_employee1", 200, 403),
        ("user_client2", 200, 403),
        ("user_client1", 200, 403),
        ("user_manager", 200, 403),
        ("user_admin", 200, 200),
    ],
)
@pytest.mark.django_db
def test_url_history_service_detail(api_client, request, user, status_code_ok, status_code_not_ok, register_services):
    """
    Тест для получения информации о зарегистрированной услуге
    [GET] http://127.0.0.1:8000/api/me/history/service/{int:pk}/
    """

    if user == "anonymous_user":
        client = request.getfixturevalue(user)
        pk_service = random.randint(1, len(register_services))
        response = client.get(reverse("clients:service-detail", kwargs={"pk": pk_service}), format="json")

        assert response.status_code == status_code_ok
        assert response.data["detail"] == IsAuthenticated.message

    else:
        user = request.getfixturevalue(user)
        api_client.force_authenticate(user=user)
        client = api_client

        register_service_user = [
            service
            for service in register_services
            if (user.is_client and service.client.user.pk == user.pk)
            or (user.is_employee and service.doctor.user.pk == user.pk)
            or (
                (user.is_client and service.client.user.pk == user.pk)
                and (user.is_employee and service.doctor.user.pk == user.pk)
            )
        ]

        register_service_not_user = [
            service
            for service in register_services
            if (user.is_client and service.client.user.pk != user.pk)
            or (user.is_employee and service.doctor.user.pk != user.pk)
            or (
                (user.is_client and service.client.user.pk != user.pk)
                and (user.is_employee and service.doctor.user.pk != user.pk)
            )
        ]

        for service in register_service_user:
            response = client.get(reverse("clients:service-detail", kwargs={"pk": service.pk}), format="json")

            assert response.status_code == status_code_ok
            if user.is_client:
                assert response.data["client"] == user.client.pk
            if user.is_employee:
                assert response.data["doctor"] == user.employee.pk

        for service in register_service_not_user:
            response = client.get(reverse("clients:service-detail", kwargs={"pk": service.pk}), format="json")

            assert response.status_code == status_code_not_ok

            if status_code_not_ok == 200:
                if user.is_client or user.is_employee:
                    assert response.data != None
            else:
                assert response.data["detail"] == IsOwnerOrAdmin.message


@pytest.mark.parametrize(
    "user, status_code",
    [
        ("anonymous_user", 401),
        ("user_client1", 200),
        ("user_employee1", 200),
        ("user_client2", 403),
        ("user_employee2", 403),
        ("user_manager", 403),
        ("user_admin", 200),
    ],
)
@pytest.mark.django_db
def test_url_history_service_update(
    api_client, request, user, status_code, register_service, user_client2, user_client_employee2
):
    """
    Тест для редактирования записи о зарегистрированной услуге
    [PUT, PATCH] http://127.0.0.1:8000/api/me/service/{int:pk}/
    """

    def perform_update_request(api_client, user, register_service, data, method="put"):
        """Выполняет запрос обновления категории."""

        if user == "anonymous_user":
            client = request.getfixturevalue(user)
        else:
            user = request.getfixturevalue(user)
            api_client.force_authenticate(user=user)
            client = api_client

        if method == "put":
            response = client.put(
                reverse("clients:service-detail", kwargs={"pk": register_service.pk}),
                data=data,
                format="json",
            )
        elif method == "patch":
            response = client.patch(
                reverse("clients:service-detail", kwargs={"pk": register_service.pk}),
                data=data,
                format="json",
            )

        return response

    put_data = {
        "pk": register_service.pk,
        "client": register_service.client.pk,
        "doctor": register_service.doctor.pk,
        "service": register_service.service.pk,
        "date_services": register_service.date_services,
        "status_service": RegistredServices.StatusServices.DONE,
        "status_paid": register_service.status_paid,
        "is_analyz": register_service.is_analyz,
        "is_vizit": register_service.is_vizit,
    }

    patch_data = {
        "status_service": RegistredServices.StatusServices.DONE,
    }

    for method, data in [("put", put_data), ("patch", patch_data)]:
        response = perform_update_request(api_client, user, register_service, data, method)

        assert response.status_code == status_code
        if status_code == 200:
            assert response.data["status_service"] == RegistredServices.StatusServices.DONE
        elif status_code == 401:
            assert response.data["detail"] == IsAuthenticated.message
        else:
            assert response.data["detail"] == IsOwnerOrAdmin.message


@pytest.mark.parametrize(
    "user,status_code",
    [
        ("anonymous_user", 401),
        ("user_manager", 403),
        ("user_admin", 204),
        ("user_employee1", 403),
        ("user_client1", 403),
        ("user_client_employee1", 403),
    ],
)
@pytest.mark.django_db
def test_url_history_service_destroy(api_client, request, user, status_code, register_service):
    """
    Тест для удаления записи о зарегистрированной услуге
    [DELETE] http://127.0.0.1:8000/api/me/service/{int:pk}/
    """

    if user == "anonymous_user":
        client = request.getfixturevalue(user)
    else:
        user = request.getfixturevalue(user)
        api_client.force_authenticate(user=user)
        client = api_client

    response = client.delete(reverse("clients:service-detail", kwargs={"pk": register_service.pk}), format="json")

    assert response.status_code == status_code

    if status_code == 204:
        assert response.data == None
    elif status_code == 401:
        assert response.data["detail"] == IsAuthenticated.message
    elif status_code == 403:
        assert response.data["detail"] == IsAdmin.message
