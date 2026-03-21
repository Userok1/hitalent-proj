from src.schemas import Department


def test_create_departments(client, db_override):
    body = Department(
        name="IT",
        parent_id=None
    )
    response = client.post("http://localhost:8080/departments", json=body.model_dump())
    assert response.status_code == 201