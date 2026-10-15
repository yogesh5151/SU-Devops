import pytest

from database.db import db
from app.services.student_service import StudentService


@pytest.fixture(autouse=True)
def reset_db():
    db.reset()
    yield
    db.reset()


def test_student_lookup():
    student = StudentService.get_student("S101")
    assert student["name"] == "Aarav Patil"


def test_add_student():
    student = StudentService.add_student("S103", "Om Student", "om@university.edu", 2)
    assert student["student_id"] == "S103"
    assert StudentService.get_student("S103") is not None


def test_duplicate_student_is_rejected():
    with pytest.raises(ValueError, match="already exists"):
        StudentService.add_student("S101", "Duplicate", "duplicate@university.edu", 2)


def test_enrollment_conflict_is_rejected():
    StudentService.enroll_student("S101", "C101")
    with pytest.raises(ValueError, match="already enrolled"):
        StudentService.enroll_student("S101", "C101")


def test_semester_credit_limit_is_18():
    StudentService.enroll_student("S101", "C101")  # 4
    StudentService.enroll_student("S101", "C102")  # 8
    StudentService.enroll_student("S101", "C103")  # 12
    StudentService.enroll_student("S101", "C104")  # 15
    StudentService.enroll_student("S101", "C105")  # 18
    db.courses["C106"] = {"course_id": "C106", "name": "Academic Project", "credits": 1, "faculty_id": "F101"}
    with pytest.raises(ValueError, match="credit limit exceeded"):
        StudentService.enroll_student("S101", "C106")
