import pytest

from database.db import db
from app.services.marks_mgmt import MarksManagement
from app.services.student_service import StudentService


@pytest.fixture(autouse=True)
def reset_db():
    db.reset()
    yield
    db.reset()


def test_grade_requires_enrollment():
    with pytest.raises(ValueError, match="must be enrolled"):
        MarksManagement.record_grade("S101", "C101", "A")


def test_grade_recording():
    StudentService.enroll_student("S101", "C101")
    record = MarksManagement.record_grade("S101", "C101", "A")
    assert record["grade"] == "A"
    assert record["grade_point"] == 9.0


def test_gpa_calculation():
    StudentService.enroll_student("S101", "C101")
    StudentService.enroll_student("S101", "C102")
    MarksManagement.record_grade("S101", "C101", "A")
    MarksManagement.record_grade("S101", "C102", "B")
    assert MarksManagement.calculate_gpa("S101") == 8.0


def test_invalid_grade_is_rejected():
    StudentService.enroll_student("S101", "C101")
    with pytest.raises(ValueError, match="Invalid grade"):
        MarksManagement.record_grade("S101", "C101", "Z")
