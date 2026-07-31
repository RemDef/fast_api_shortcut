import pytest


@pytest.mark.asyncio
async def test_users_list_forbidden_for_non_admin(client, auth_headers):
    response = await client.get("/v1/users/", headers=auth_headers)
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_users_list_unauthorized(client):
    response = await client.get("/v1/users/")
    assert response.status_code == 401
