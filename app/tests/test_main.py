from fastapi import status
import pytest
from httpx import AsyncClient

# # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # ENDPOINT ACCESS TOKEN # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # #


@pytest.mark.asyncio
async def test_access_token_successed(async_client: AsyncClient):
    response = await async_client.post(
        "/api/auth/login/access-token",
        data={"username": "admin", "password": "winsalg913tkwslkwq10q"},
    )
    response_json: dict = response.json()
    assert response_json.get("token_type") == "bearer"
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_access_token_incorrect_one(async_client: AsyncClient):
    response = await async_client.post(
        "/api/auth/login/access-token",
        data={"username": "123124", "password": "1224w12"},
    )
    response_json: dict = response.json()
    assert response_json == {"detail": "Incorrect username or password"}
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_access_token_incorrect_two(async_client: AsyncClient):
    response = await async_client.post(
        "/api/auth/login/access-token",
        data={"username": 1.52, "password": [1, 5]},
    )
    response_json: dict = response.json()
    assert response_json == {"detail": "Incorrect username or password"}
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_access_token_not_validated(async_client: AsyncClient):
    response = await async_client.post(
        "/api/auth/login/access-token",
        data={"us125erna125me": "123124", 1: "1224w12"},
    )
    response_json: dict = response.json()
    assert response_json == {
        "detail": [
            {
                "loc": ["body", "username"],
                "msg": "field required",
                "type": "value_error.missing",
            },
            {
                "loc": ["body", "password"],
                "msg": "field required",
                "type": "value_error.missing",
            },
        ]
    }
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


# # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # CREATE USER # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # #


@pytest.mark.asyncio
async def test_create_user_successed(
    async_client: AsyncClient,
    auth_headers_superuser: dict,
):
    data = {
        "username": "string",
        "email": "user@example.com",
        "first_name": "string",
        "last_name": "string",
        "password": "string",
    }

    response = await async_client.post(
        "/api/auth/users/create",
        json=data,
        headers=auth_headers_superuser,
    )
    response_json: dict = response.json()
    assert list(response_json.keys()) == [
        "username",
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_superuser",
        "created_at",
        "id",
    ]
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio
async def test_create_user_successed_two(
    async_client: AsyncClient,
    auth_headers_superuser: dict,
):
    data = {
        "username": "stringqw",
        "email": "usqewer@example.com",
        "password": "striwqeng",
    }

    response = await async_client.post(
        "/api/auth/users/create",
        json=data,
        headers=auth_headers_superuser,
    )
    response_json: dict = response.json()
    assert list(response_json.keys()) == [
        "username",
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_superuser",
        "created_at",
        "id",
    ]
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio
async def test_create_user_email_is_none(
    async_client: AsyncClient,
    auth_headers_superuser: dict,
):
    data = {
        "username": "stringqw",
        "password": "striwqeng",
    }

    response = await async_client.post(
        "/api/auth/users/create",
        json=data,
        headers=auth_headers_superuser,
    )
    response_json: dict = response.json()
    assert response_json == {
        "detail": [
            {
                "loc": ["body", "email"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_create_user_username_is_none(
    async_client: AsyncClient,
    auth_headers_superuser: dict,
):
    data = {
        "email": "usqewer@example.com",
        "password": "striwqeng",
    }

    response = await async_client.post(
        "/api/auth/users/create",
        json=data,
        headers=auth_headers_superuser,
    )
    response_json: dict = response.json()
    assert response_json == {
        "detail": [
            {
                "loc": ["body", "username"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_create_user_password_is_none(
    async_client: AsyncClient,
    auth_headers_superuser: dict,
):
    data = {
        "username": "stringqw",
        "email": "usqewer@example.com",
    }

    response = await async_client.post(
        "/api/auth/users/create",
        json=data,
        headers=auth_headers_superuser,
    )
    response_json: dict = response.json()
    assert response_json == {
        "detail": [
            {
                "loc": ["body", "password"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_create_user_none_auth(
    async_client: AsyncClient,
):
    data = {
        "username": "stringqw",
        "password": "saktwjt132",
        "email": "usqewer@example.com",
    }

    response = await async_client.post("/api/auth/users/create", json=data)
    response_json: dict = response.json()

    assert response_json == {"detail": "Not authenticated"}
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_create_user_auth_not_superuser(
    async_client: AsyncClient,
):
    data = {
        "username": "stringqw",
        "password": "saktwjt132",
        "email": "usqewer@example.com",
    }

    response = await async_client.post("/api/auth/users/create", json=data)
    response_json: dict = response.json()

    assert response_json == {"detail": "Not authenticated"}
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # #  READ USERS # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # #


@pytest.mark.asyncio
async def test_read_users_success(
    async_client: AsyncClient,
    auth_headers_superuser: dict,
):
    response = await async_client.get(
        "/api/auth/users/?skip=0&limit=25",
        headers=auth_headers_superuser,
    )
    response_json: list = response.json()
    assert type(response_json) == list
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_read_users_not_correct_url(
    async_client: AsyncClient,
    auth_headers_superuser: dict,
):
    not_correct_url = "/api/auth/users?skip=0&limit=25"
    response = await async_client.get(
        not_correct_url,
        headers=auth_headers_superuser,
    )
    assert response.headers.get("location")
    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT


@pytest.mark.asyncio
async def test_read_users_none_correct_skip(
    async_client: AsyncClient,
    auth_headers_superuser: dict,
):
    skip: int = 12
    limit: int = 12

    url = f"/api/auth/users/?skip={skip}&limit={limit}&523151=251"

    response = await async_client.get(
        url,
        headers=auth_headers_superuser,
    )
    response_json: list = response.json()
    assert response_json == {
        "detail": "No users with such parameters were found",
    }
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_read_users_float_data(
    async_client: AsyncClient,
    auth_headers_superuser: dict,
):
    skip: int = 0.1
    limit: int = 0.5
    url = f"/api/auth/users/?skip={skip}&limit={limit}&523151=251"

    response = await async_client.get(
        url,
        headers=auth_headers_superuser,
    )
    response_json: list = response.json()
    assert response_json == {
        "detail": [
            {
                "loc": ["query", "skip"],
                "msg": "value is not a valid integer",
                "type": "type_error.integer",
            },
            {
                "loc": ["query", "limit"],
                "msg": "value is not a valid integer",
                "type": "type_error.integer",
            },
        ]
    }
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_read_users_string_data(
    async_client: AsyncClient,
    auth_headers_superuser: dict,
):
    skip: str = "01"
    limit: str = "w"
    url = f"/api/auth/users/?skip={skip}&limit={limit}&523151=251"

    response = await async_client.get(
        url,
        headers=auth_headers_superuser,
    )
    response_json: list = response.json()
    assert response_json == {
        "detail": [
            {
                "loc": ["query", "limit"],
                "msg": "value is not a valid integer",
                "type": "type_error.integer",
            }
        ]
    }
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_read_users_none_auth_data_corrected(
    async_client: AsyncClient,
):
    skip: int = 0
    limit: int = 5
    url = f"/api/auth/users/?skip={skip}&limit={limit}"

    response = await async_client.get(url)
    response_json: list = response.json()

    assert response_json == {"detail": "Not authenticated"}
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_read_users_none_auth_data_uncorrected(
    async_client: AsyncClient,
):
    skip: str = "201"
    limit: float = 5.1
    url = f"/api/auth/users/?skip={skip}&limit={limit}"

    response = await async_client.get(url)
    response_json: list = response.json()

    assert response_json == {"detail": "Not authenticated"}
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # READ ME # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # #

# To be continued...
