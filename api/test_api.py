import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework import status
from .models import Task, TaskList
from uuid import uuid4

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
    user_id = user.id
    return client, user_id


@pytest.fixture
def admin_client():
    user = User.objects.create_superuser(
        username='admin',
        email='admin@gmail.com',
        password='ahmet1413'
    )
    client = APIClient()
    client.force_authenticate(user=user)
    user_id = user.id
    return client, user_id


@pytest.mark.django_db
def test_get_overview():
    client = APIClient()
    response = client.get('/')
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_authenticated_routes():
    client = APIClient()
    response = client.get('/list')
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_create_tasklist(authenticated_client):
    client, user_id = authenticated_client
    payload = {
        "name": "Tasklist 1",
        "completion_percentage": 90
    }
    response = client.post('/list', payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert TaskList.objects.count() == 1
    assert response.data['creator'] is not None


@pytest.mark.django_db
def test_get_all_tasklist(authenticated_client):
    client, user_id = authenticated_client
    TaskList.objects.create(
        name="Tasklist 1", completion_percentage=50, creator=user_id)
    TaskList.objects.create(name="Tasklist 2", completion_percentage=50)
    response = client.get('/list')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1


@pytest.mark.django_db
def test_get_all_tasklist_as_admin(admin_client):
    client, user_id = admin_client
    TaskList.objects.create(
        name="Tasklist 1", completion_percentage=50, creator=uuid4())
    TaskList.objects.create(name="Tasklist 1", completion_percentage=50)
    response = client.get('/list')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2


@pytest.mark.django_db
def test_get_tasklist(authenticated_client):
    client, user_id = authenticated_client
    created_tasklist = TaskList.objects.create(
        name="Tasklist 1", completion_percentage=50, creator=user_id)
    response = client.get(f'/list/{created_tasklist.id}')
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_tasklist_as_admin(admin_client):
    client, user_id = admin_client
    created_tasklist = TaskList.objects.create(
        name="Tasklist 1", completion_percentage=50)
    response = client.get(f'/list/{created_tasklist.id}')
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_put_tasklist(authenticated_client):
    client, user_id = authenticated_client
    created_tasklist = TaskList.objects.create(
        name="Tasklist 1", completion_percentage=50, creator=user_id)
    payload = {
        "name": "Quis minim in eu tempor sunt do aliqua occaecat duis dolor ea.",
        "completion_percentage": 90
    }
    response = client.put(f'/list/{created_tasklist.id}', payload)
    assert response.status_code == status.HTTP_200_OK
    get_created = TaskList.objects.get(id=created_tasklist.id, deleted_at=None)
    assert get_created.name == payload["name"]
    assert get_created.completion_percentage == payload["completion_percentage"]


@pytest.mark.django_db
def test_put_tasklist_as_admin(admin_client):
    client, user_id = admin_client
    created_tasklist = TaskList.objects.create(
        name="Tasklist 1", completion_percentage=50, creator=uuid4())
    payload = {
        "name": "Quis minim in eu tempor sunt do aliqua occaecat duis dolor ea.",
        "completion_percentage": 90
    }
    response = client.put(f'/list/{created_tasklist.id}', payload)
    assert response.status_code == status.HTTP_200_OK
    get_created = TaskList.objects.get(id=created_tasklist.id, deleted_at=None)
    assert get_created.name == payload["name"]
    assert get_created.completion_percentage == payload["completion_percentage"]


@pytest.mark.django_db
def test_delete_tasklist(authenticated_client):
    client, user_id = authenticated_client
    created_tasklist = TaskList.objects.create(
        name="Tasklist 1", completion_percentage=50, creator=user_id)
    created_task = Task.objects.create(
        list_id=created_tasklist.id, content="Mollit eu quis occaecat voluptate deserunt dolor dolore et.", creator=user_id)
    response = client.delete(f'/list/{created_tasklist.id}')
    assert response.status_code == status.HTTP_200_OK
    get_tasklist = TaskList.objects.filter(
        id=created_tasklist.id, deleted_at=None).first()
    assert get_tasklist is None
    get_task = Task.objects.filter(id=created_task.id, deleted_at=None).first()
    assert get_task is None


@pytest.mark.django_db
def test_delete_tasklist_as_admin(admin_client):
    client, user_id = admin_client
    created_tasklist = TaskList.objects.create(
        name="Tasklist 1", completion_percentage=50, creator=uuid4())
    created_task = Task.objects.create(
        list_id=created_tasklist.id, content="Mollit eu quis occaecat voluptate deserunt dolor dolore et.", creator=uuid4())
    response = client.delete(f'/list/{created_tasklist.id}')
    assert response.status_code == status.HTTP_200_OK
    get_tasklist = TaskList.objects.filter(
        id=created_tasklist.id, deleted_at=None).first()
    assert get_tasklist is None
    get_task = Task.objects.filter(id=created_task.id, deleted_at=None).first()
    assert get_task is None


@pytest.mark.django_db
def test_create_task(authenticated_client):
    client, user_id = authenticated_client
    created_tasklist = TaskList.objects.create(
        name="Tasklist 1", completion_percentage=50, creator=user_id)
    payload = {
        "list_id": created_tasklist.id,
        "content": "Culpa consequat ad voluptate pariatur nulla culpa et fugiat magna pariatur aliquip quis labore.",
        "completed": False
    }
    response = client.post('/task', payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert Task.objects.count() == 1
    assert response.data['creator'] is not None


@pytest.mark.django_db
def test_get_task(authenticated_client):
    client, user_id = authenticated_client
    created_tasklist = TaskList.objects.create(
        name="Tasklist 1", completion_percentage=50, creator=user_id)
    created_task = Task.objects.create(
        list_id=created_tasklist.id, content="Consectetur ad minim occaecat do est velit fugiat proident sint fugiat.", creator=user_id)
    response = client.get(f'/task/{created_task.id}')
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_task_as_admin(admin_client):
    client, user_id = admin_client
    created_tasklist = TaskList.objects.create(
        name="Tasklist 1", completion_percentage=50)
    created_task = Task.objects.create(
        list_id=created_tasklist.id, content="Consectetur ad minim occaecat do est velit fugiat proident sint fugiat.", creator=uuid4())
    response = client.get(f'/task/{created_task.id}')
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_put_task(authenticated_client):
    client, user_id = authenticated_client
    created_task = Task.objects.create(list_id=uuid4(
    ), content="Consectetur ad minim occaecat do est velit fugiat proident sint fugiat.", creator=user_id)
    payload = {
        "list_id": uuid4(),
        "content": "Quis occaecat incididunt ullamco dolor nostrud incididunt laboris.",
        "completed": True
    }
    response = client.put(f'/task/{created_task.id}', payload)
    assert response.status_code == status.HTTP_200_OK
    get_created = Task.objects.get(id=created_task.id)
    assert get_created.list_id == payload["list_id"]
    assert get_created.content == payload["content"]
    assert get_created.completed == payload["completed"]


@pytest.mark.django_db
def test_put_task_as_admin(admin_client):
    client, user_id = admin_client
    created_task = Task.objects.create(list_id=uuid4(
    ), content="Consectetur ad minim occaecat do est velit fugiat proident sint fugiat.", creator=uuid4())
    payload = {
        "list_id": uuid4(),
        "content": "Quis occaecat incididunt ullamco dolor nostrud incididunt laboris.",
        "completed": True
    }
    response = client.put(f'/task/{created_task.id}', payload)
    assert response.status_code == status.HTTP_200_OK
    get_created = Task.objects.get(id=created_task.id)
    assert get_created.list_id == payload["list_id"]
    assert get_created.content == payload["content"]
    assert get_created.completed == payload["completed"]


@pytest.mark.django_db
def test_delete_task(authenticated_client):
    client, user_id = authenticated_client
    created_task = Task.objects.create(list_id=uuid4(
    ), content="Consectetur ad minim occaecat do est velit fugiat proident sint fugiat.", creator=user_id)
    response = client.delete(f'/task/{created_task.id}')
    assert response.status_code == status.HTTP_200_OK
    get_task = Task.objects.filter(id=created_task.id, deleted_at=None).first()
    assert get_task is None


@pytest.mark.django_db
def test_delete_task_as_admin(admin_client):
    client, user_id = admin_client
    created_task = Task.objects.create(list_id=uuid4(
    ), content="Consectetur ad minim occaecat do est velit fugiat proident sint fugiat.", creator=uuid4())
    response = client.delete(f'/task/{created_task.id}')
    assert response.status_code == status.HTTP_200_OK
    get_task = Task.objects.filter(id=created_task.id, deleted_at=None).first()
    assert get_task is None
