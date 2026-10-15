import pytest

from app import create_app
from database.db import db


@pytest.fixture
def client():
    db.reset()
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as test_client:
        yield test_client

    db.reset()


def test_health_endpoint(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "UP"


def test_student_and_course_endpoints(client):
    students = client.get("/api/students")
    courses = client.get("/api/courses")
    assert students.status_code == 200
    assert courses.status_code == 200
    assert students.get_json()["count"] >= 2
    assert courses.get_json()["count"] >= 5


def test_enrollment_and_gpa_flow(client):
    enrollment = client.post(
        "/api/enrollments",
        json={"student_id": "S101", "course_id": "C101"},
    )
    assert enrollment.status_code == 201

    grade = client.post(
        "/api/grades",
        json={"student_id": "S101", "course_id": "C101", "grade": "A"},
    )
    assert grade.status_code == 201

    gpa = client.get("/api/students/S101/gpa")
    assert gpa.status_code == 200
    assert gpa.get_json()["gpa"] == 9.0


def test_faculty_endpoint(client):
    response = client.get("/api/faculty")

    assert response.status_code == 200

    data = response.get_json()

    assert "count" in data
    assert "faculty" in data
    assert data["count"] == len(data["faculty"])
