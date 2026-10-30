from fastapi.testclient import TestClient

from app.main import _tasks, app

client = TestClient(app)


def setup_function() -> None:
    _tasks.clear()


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_and_get_task() -> None:
    created = client.post("/tasks", json={"title": "write course"})
    assert created.status_code == 201
    task_id = created.json()["id"]
    assert client.get(f"/tasks/{task_id}").json()["title"] == "write course"


def test_missing_task_returns_404() -> None:
    assert client.get("/tasks/999").status_code == 404


def test_empty_title_is_rejected() -> None:
    assert client.post("/tasks", json={"title": ""}).status_code == 422
