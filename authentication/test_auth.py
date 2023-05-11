import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model, authenticate
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def authenticated_client():
    user = User.objects.create_user(
        username='ahmet',
        email='ahmet@gmail.com',
        password='ahmet1413'
    )
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.mark.django_db
def test_register():
    payload = {
        "email": "ahmet@gmail.com",
        "password": "ahmet1413",
        "username": "ahmet"
    }
    response = APIClient().post('/auth/register', payload)
    user = authenticate(username="ahmet@gmail.com", password="ahmet1413")
    assert response.status_code == status.HTTP_201_CREATED
    assert user is not None


@pytest.mark.django_db
def test_login(authenticated_client):
    payload = {
        "email": "ahmet@gmail.com",
        "password": "ahmet1413"
    }
    response = authenticated_client.post('/auth/login', payload)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_getuserdata_route(authenticated_client):
    response = authenticated_client.get('/auth/user')
    assert response.status_code == status.HTTP_200_OK