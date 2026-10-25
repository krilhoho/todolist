from itertools import count

import pytest
from fastapi.testclient import TestClient

import app_final as application


@pytest.fixture
def client():
    application.tasks.clear()
    application.task_ids = count(1)

    with TestClient(application.app) as test_client:
        yield test_client

    application.tasks.clear()

def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_tasks_and_list(client):
    first = client.post("/tasks", json={"title": "Подготовить отчёт"})
    second = client.post("/tasks", json={"title": "Написать тесты"})

    assert first.status_code == 201
    assert second.status_code == 201

    first_task = first.json()
    second_task = second.json()

    assert first_task["title"] == "Подготовить отчёт"
    assert first_task["done"] is False
    assert first_task["id"] != second_task["id"]

    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == [first_task, second_task]


def test_get_task_by_id(client):
    created = client.post(
        "/tasks",
        json={"title": "Проверить поиск"},
    ).json()

    response = client.get(f"/tasks/{created['id']}")

    assert response.status_code == 200
    assert response.json() == created


def test_complete_task(client):
    created = client.post(
        "/tasks",
        json={"title": "Завершить задачу"},
    ).json()

    response = client.patch(f"/tasks/{created['id']}/complete")

    assert response.status_code == 200
    assert response.json()["id"] == created["id"]
    assert response.json()["title"] == created["title"]
    assert response.json()["done"] is True

    saved = client.get(f"/tasks/{created['id']}")

    assert saved.status_code == 200
    assert saved.json()["done"] is True

def test_empty_title_is_rejected(client):
    response = client.post("/tasks", json={"title": ""})

    assert response.status_code == 422

    tasks_response = client.get("/tasks")

    assert tasks_response.status_code == 200
    assert tasks_response.json() == []


def test_get_missing_task(client):
    response = client.get("/tasks/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Задача не найдена"}


def test_complete_missing_task(client):
    response = client.patch("/tasks/999/complete")

    assert response.status_code == 404
    assert response.json() == {"detail": "Задача не найдена"}


def test_invalid_task_id(client):
    response = client.get("/tasks/abc")

    assert response.status_code == 422