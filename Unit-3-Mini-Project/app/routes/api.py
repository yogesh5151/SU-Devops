from flask import Blueprint, jsonify, request

from app.services.marks_mgmt import MarksManagement
from app.services.student_service import StudentService
from database.db import db

api_bp = Blueprint("api", __name__)


@api_bp.route("/health", methods=["GET"])
def healthcheck():
    return jsonify({
        "status": "UP",
        "service": (
            "Enterprise Student Record and Academic "
            "Management Platform"
         ),
        "version": "1.0.0",
    }), 200


@api_bp.route("/students", methods=["GET"])
def list_students():
    students = StudentService.list_students()
    return jsonify({
        "count": len(students),
        "students": students
    }), 200


@api_bp.route("/students", methods=["POST"])
def register_student():
    data = request.get_json() or {}

    try:
        student = StudentService.add_student(
            data.get("student_id"),
            data.get("name"),
            data.get("email"),
            data.get("semester", 1),
        )

        return jsonify({
            "message": "Student registered successfully",
            "student": student
        }), 201

    except (ValueError, TypeError) as exc:
        return jsonify({"error": str(exc)}), 400


@api_bp.route("/students/<student_id>", methods=["GET"])
def get_student(student_id):
    student = StudentService.get_student(student_id)

    if not student:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(student), 200


@api_bp.route("/courses", methods=["GET"])
def list_courses():
    courses = StudentService.list_courses()

    return jsonify({
        "count": len(courses),
        "courses": courses
    }), 200


@api_bp.route("/faculty", methods=["GET"])
def list_faculty():
    faculty = list(db.faculty.values())

    return jsonify({
        "count": len(faculty),
        "faculty": faculty
    }), 200


@api_bp.route("/enrollments", methods=["POST"])
def enroll():
    data = request.get_json() or {}

    try:
        enrollment = StudentService.enroll_student(
            data.get("student_id"),
            data.get("course_id")
        )

        return jsonify({
            "message": "Enrollment successful",
            "enrollment": enrollment
        }), 201

    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400


@api_bp.route("/enrollments", methods=["GET"])
def list_enrollments():
    student_id = request.args.get("student_id")

    return jsonify(
        StudentService.get_enrollments(student_id)
    ), 200


@api_bp.route("/grades", methods=["POST"])
def record_grade():
    data = request.get_json() or {}

    try:
        record = MarksManagement.record_grade(
            data.get("student_id"),
            data.get("course_id"),
            data.get("grade")
        )

        return jsonify({
            "message": "Grade recorded successfully",
            "grade": record
        }), 201

    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400


@api_bp.route("/students/<student_id>/grades", methods=["GET"])
def get_grades(student_id):
    return jsonify(
        MarksManagement.get_grades(student_id)
    ), 200


@api_bp.route("/students/<student_id>/gpa", methods=["GET"])
def get_gpa(student_id):
    if not StudentService.get_student(student_id):
        return jsonify({"error": "Student not found"}), 404

    return jsonify({
        "student_id": student_id,
        "gpa": MarksManagement.calculate_gpa(student_id)
    }), 200
