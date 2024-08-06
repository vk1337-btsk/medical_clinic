import pytest
from core.permissions import IsAdminOrManager, IsAuthenticated
from django.urls import reverse
from tests.conftest import COUNT_CATEGORIES, COUNT_EMPLOYEES, COUNT_SERVICES


@pytest.mark.parametrize(
    "user,status_code",
    [
        ("anonymous_user", 200),
        ("user_manager", 200),
        ("user_admin", 200),
        ("user_employee1", 200),
        ("user_client1", 200),
        ("user_client_employee1", 200),
    ],
)
@pytest.mark.django_db
def test_url_catalog(api_client, request, categories_services_info, user, status_code):
    """
    Тест для получения данных с каталога для различных пользователей
    [GET] http://127.0.0.1:8000/api/catalog/
    """

    if user == "anonymous_user":
        client = request.getfixturevalue(user)
    else:
        user = request.getfixturevalue(user)
        api_client.force_authenticate(user=user)
        client = api_client

    response = client.get(reverse("catalog:catalog"), format="json")
    print(f"{user=} \n\n {response=}")
    assert response.status_code == status_code
    assert len(response.data["list_categories"]) == COUNT_CATEGORIES
    assert response.data["list_categories"][0]["title"] == categories_services_info[0][0].title


@pytest.mark.parametrize(
    "user,status_code",
    [
        ("anonymous_user", 200),
        ("user_manager", 200),
        ("user_admin", 200),
        ("user_employee1", 200),
        ("user_client1", 200),
        ("user_client_employee1", 200),
    ],
)
@pytest.mark.django_db
def test_url_category_list(api_client, request, categories_services_info, user, status_code):
    """
    Тест для получения списка категорий для различных пользователей
    [GET] http://127.0.0.1:8000/api/catalog/category/
    """

    if user == "anonymous_user":
        client = request.getfixturevalue(user)
    else:
        user = request.getfixturevalue(user)
        api_client.force_authenticate(user=user)
        client = api_client

    response = client.get(reverse("catalog:category-list"), format="json")

    assert response.status_code == status_code
    assert len(response.data) == COUNT_CATEGORIES
    assert response.data[0]["title"] == categories_services_info[0][0].title


@pytest.mark.parametrize(
    "user,status_code",
    [
        ("anonymous_user", 200),
        ("user_manager", 200),
        ("user_admin", 200),
        ("user_employee1", 200),
        ("user_client1", 200),
        ("user_client_employee1", 200),
    ],
)
@pytest.mark.django_db
def test_url_category_detail(api_client, request, category_service_info, user, status_code):
    """
    Тест для получения информации о категории для различных пользователей
    [GET] http://127.0.0.1:8000/api/catalog/category/{int:pk}/
    """

    if user == "anonymous_user":
        client = request.getfixturevalue(user)
    else:
        user = request.getfixturevalue(user)
        api_client.force_authenticate(user=user)
        client = api_client

    response = client.get(
        reverse("catalog:category-detail", kwargs={"pk": category_service_info[0][0].pk}), format="json"
    )

    assert response.status_code == status_code
    assert response.data["title"] == category_service_info[0][0].title


@pytest.mark.parametrize(
    "user,status_code",
    [
        ("anonymous_user", 401),
        ("user_manager", 201),
        ("user_admin", 201),
        ("user_employee1", 403),
        ("user_client1", 403),
        ("user_client_employee1", 403),
    ],
)
@pytest.mark.django_db
def test_url_category_create(api_client, request, user, status_code):
    """
    Тест для создания категории для различных пользователей
    [POST] http://127.0.0.1:8000/api/catalog/category/
    """

    data = {"title": "Название категории", "description": "Описание категории"}

    if user == "anonymous_user":
        client = request.getfixturevalue(user)
    else:
        user = request.getfixturevalue(user)
        api_client.force_authenticate(user=user)
        client = api_client

    response = client.post(reverse("catalog:category-list"), data=data, format="json")

    assert response.status_code == status_code

    if status_code == 201:
        assert response.data["title"] == data["title"]
    elif status_code == 401:
        assert response.data["detail"] == IsAuthenticated.message
    else:
        assert response.data["detail"] == IsAdminOrManager.message


@pytest.mark.parametrize(
    "user,status_code",
    [
        ("anonymous_user", 401),
        ("user_manager", 200),
        ("user_admin", 200),
        ("user_employee1", 403),
        ("user_client1", 403),
        ("user_client_employee1", 403),
    ],
)
@pytest.mark.django_db
def test_url_category_update(api_client, request, category_service_info, user, status_code):
    """
    Тест для изменения категории для различных пользователей
    [PUT, PATCH] http://127.0.0.1:8000/api/catalog/category/{int:pk}/
    """

    def perform_update_request(api_client, user, category_service_info, data, method="put"):
        """Выполняет запрос обновления категории."""

        if user == "anonymous_user":
            client = request.getfixturevalue(user)
        else:
            user = request.getfixturevalue(user)
            api_client.force_authenticate(user=user)
            client = api_client

        if method == "put":
            response = client.put(
                reverse("catalog:category-detail", kwargs={"pk": category_service_info[0][0].pk}),
                data=data,
                format="json",
            )
        elif method == "patch":
            response = client.patch(
                reverse("catalog:category-detail", kwargs={"pk": category_service_info[0][0].pk}),
                data=data,
                format="json",
            )

        return response

    put_data = {"title": "Название категории", "description": "Новое описание категории"}
    patch_data = {"title": "Название категории"}

    for method, data in [("put", put_data), ("patch", patch_data)]:
        response = perform_update_request(api_client, user, category_service_info, data, method)

        assert response.status_code == status_code

        if status_code == 200:
            assert response.data["title"] == data["title"]
        elif status_code == 401:
            assert response.data["detail"] == IsAuthenticated.message
        else:
            assert response.data["detail"] == IsAdminOrManager.message


@pytest.mark.parametrize(
    "user,status_code",
    [
        ("anonymous_user", 401),
        ("user_manager", 204),
        ("user_admin", 204),
        ("user_employee1", 403),
        ("user_client1", 403),
        ("user_client_employee1", 403),
    ],
)
@pytest.mark.django_db
def test_url_category_destroy(api_client, request, category_service_info, user, status_code):
    """
    Тест для удаления категории для различных пользователей
    [DELETE] http://127.0.0.1:8000/api/catalog/category/{int:pk}/
    """

    if user == "anonymous_user":
        client = request.getfixturevalue(user)
    else:
        user = request.getfixturevalue(user)
        api_client.force_authenticate(user=user)
        client = api_client

    response = client.delete(
        reverse("catalog:category-detail", kwargs={"pk": category_service_info[0][0].pk}), format="json"
    )

    if status_code == 204:
        assert response.data == None
    elif status_code == 401:
        assert response.data["detail"] == IsAuthenticated.message
    else:
        assert response.data["detail"] == IsAdminOrManager.message


@pytest.mark.parametrize(
    "user,status_code",
    [
        ("anonymous_user", 200),
        ("user_manager", 200),
        ("user_admin", 200),
        ("user_employee1", 200),
        ("user_client1", 200),
        ("user_client_employee1", 200),
    ],
)
@pytest.mark.django_db
def test_url_service_information_list(api_client, request, categories_services_info, user, status_code):
    """
    Тест для просмотра списка услуг для различных пользователей
    [GET] http://127.0.0.1:8000/api/catalog/service/
    """

    if user == "anonymous_user":
        client = request.getfixturevalue(user)
    else:
        user = request.getfixturevalue(user)
        api_client.force_authenticate(user=user)
        client = api_client

    response = client.get(reverse("catalog:service-list"), format="json")

    assert response.status_code == status_code
    assert len(response.data) == COUNT_CATEGORIES * COUNT_SERVICES


@pytest.mark.parametrize(
    "user,status_code",
    [
        ("anonymous_user", 200),
        ("user_manager", 200),
        ("user_admin", 200),
        ("user_employee1", 200),
        ("user_client1", 200),
        ("user_client_employee1", 200),
    ],
)
@pytest.mark.django_db
def test_url_service_information_detail(api_client, request, category_service_info, user, status_code):
    """
    Тест для просмотра услуги для различных пользователей
    [GET] http://127.0.0.1:8000/api/catalog/service/{int:pk}/
    """

    if user == "anonymous_user":
        client = request.getfixturevalue(user)
    else:
        user = request.getfixturevalue(user)
        api_client.force_authenticate(user=user)
        client = api_client

    response = client.get(
        reverse("catalog:service-detail", kwargs={"pk": category_service_info[1][0].pk}), format="json"
    )

    assert response.status_code == status_code
    assert response.data["title"] == category_service_info[1][0].title


@pytest.mark.parametrize(
    "user,status_code",
    [
        ("anonymous_user", 401),
        ("user_manager", 201),
        ("user_admin", 201),
        ("user_employee1", 403),
        ("user_client1", 403),
        ("user_client_employee1", 403),
    ],
)
@pytest.mark.django_db
def test_url_service_information_create(api_client, request, category_service_info, user, status_code):
    """
    Тест для создания услуги для различных пользователей
    [POST] http://127.0.0.1:8000/api/catalog/service/
    """

    data = {
        "title": "Название услуги",
        "general_info": "Общая информация об услуге",
        "additional_info": "Дополнительная информация об услуге",
        "preparation": "Продолжительность оказания услуги",
        "price": 1044,
        "categories": [category_service_info[0][0].pk],
    }

    if user == "anonymous_user":
        client = request.getfixturevalue(user)
    else:
        user = request.getfixturevalue(user)
        api_client.force_authenticate(user=user)
        client = api_client

    response = client.post(reverse("catalog:service-list"), data=data, format="json")

    assert response.status_code == status_code

    if status_code == 201:
        assert response.data["title"] == data["title"]
    elif status_code == 401:
        assert response.data["detail"] == IsAuthenticated.message
    else:
        assert response.data["detail"] == IsAdminOrManager.message


@pytest.mark.parametrize(
    "user,status_code",
    [
        ("anonymous_user", 401),
        ("user_manager", 200),
        ("user_admin", 200),
        ("user_employee1", 403),
        ("user_client1", 403),
        ("user_client_employee1", 403),
    ],
)
@pytest.mark.django_db
def test_url_service_information_update(api_client, request, category_service_info, user, status_code):
    """
    Тест для изменения услуги для различных пользователей
    [PUT, PATCH] http://127.0.0.1:8000/api/catalog/service/{int:pk}/
    """

    def perform_update_request(api_client, user, category_service_info, data, method="put"):
        """Выполняет запрос обновления услуги."""

        if user == "anonymous_user":
            client = request.getfixturevalue(user)
        else:
            user = request.getfixturevalue(user)
            api_client.force_authenticate(user=user)
            client = api_client

        if method == "put":
            response = client.put(
                reverse("catalog:service-detail", kwargs={"pk": category_service_info[1][0].pk}),
                data=data,
                format="json",
            )
        elif method == "patch":
            response = client.patch(
                reverse("catalog:service-detail", kwargs={"pk": category_service_info[1][0].pk}),
                data=data,
                format="json",
            )

        return response

    put_data = {
        "categories": [category.pk for category in category_service_info[0]],
        "title": "Новое название услуги",
        "general_info": "Новая общая информация",
        "additional_info": "Новая дополнительная информация",
        "duration": "1 00:00:00",
        "preparation": "Новые требования к подготовке оказания услуги",
        "price": 8007,
        "discount": 10,
    }
    patch_data = {"title": "Новое название услуги"}

    for method, data in [("put", put_data), ("patch", patch_data)]:
        response = perform_update_request(api_client, user, category_service_info, data, method)

        assert response.status_code == status_code

        if status_code == 200:
            assert response.data["title"] == data["title"]
        elif status_code == 401:
            assert response.data["detail"] == IsAuthenticated.message
        else:
            assert response.data["detail"] == IsAdminOrManager.message


@pytest.mark.parametrize(
    "user,status_code",
    [
        ("anonymous_user", 401),
        ("user_manager", 204),
        ("user_admin", 204),
        ("user_employee1", 403),
        ("user_client1", 403),
        ("user_client_employee1", 403),
    ],
)
@pytest.mark.django_db
def test_url_service_information_destroy(api_client, request, category_service_info, user, status_code):
    """
    Тест для удаления услуги для различных пользователей
    [DELETE] http://127.0.0.1:8000/api/catalog/service/{int:pk}/
    """

    if user == "anonymous_user":
        client = request.getfixturevalue(user)
    else:
        user = request.getfixturevalue(user)
        api_client.force_authenticate(user=user)
        client = api_client

    response = client.delete(
        reverse("catalog:service-detail", kwargs={"pk": category_service_info[1][0].pk}), format="json"
    )

    if status_code == 204:
        assert response.data == None
    elif status_code == 401:
        assert response.data["detail"] == IsAuthenticated.message
    else:
        assert response.data["detail"] == IsAdminOrManager.message


@pytest.mark.parametrize(
    "user,status_code",
    [
        ("anonymous_user", 200),
        ("user_manager", 200),
        ("user_admin", 200),
        ("user_employee1", 200),
        ("user_client1", 200),
        ("user_client_employee1", 200),
    ],
)
@pytest.mark.django_db
def test_url_doctors_list(api_client, request, employees, user, status_code):
    """
    Тест для получения списка докторов для различных пользователей
    [GET] http://127.0.0.1:8000/api/catalog/doctor/
    """

    if user == "anonymous_user":
        client = request.getfixturevalue(user)
    else:
        user = request.getfixturevalue(user)
        api_client.force_authenticate(user=user)
        client = api_client

    response = client.get(reverse("catalog:doctor-list"), format="json")

    if user == "anonymous_user" or not user.is_employee:
        assert response.status_code == status_code
        assert len(response.data) == COUNT_EMPLOYEES
    else:
        assert len(response.data) == COUNT_EMPLOYEES + 1


@pytest.mark.parametrize(
    "user,status_code",
    [
        ("anonymous_user", 200),
        ("user_manager", 200),
        ("user_admin", 200),
        ("user_employee1", 200),
        ("user_client1", 200),
        ("user_client_employee1", 200),
    ],
)
@pytest.mark.django_db
def test_url_doctors_detail(api_client, request, employees, user, status_code):
    """
    Тест для получения информации о докторе для различных пользователей
    [GET] http://127.0.0.1:8000/api/catalog/doctor/{int:pk}/
    """

    if user == "anonymous_user":
        client = request.getfixturevalue(user)
    else:
        user = request.getfixturevalue(user)
        api_client.force_authenticate(user=user)
        client = api_client

    response = client.get(reverse("catalog:doctor-detail", kwargs={"pk": employees[0].employee.pk}), format="json")

    assert response.status_code == status_code
    assert response.data["job_title"] == employees[0].employee.job_title
