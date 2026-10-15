from database.db import db


class StudentService:
    """Business operations for students, courses and enrollments."""

    MAX_SEMESTER_CREDITS = 18

    @staticmethod
    def add_student(student_id, name, email, semester=1):
        if not student_id or not name or not email:
            raise ValueError("student_id, name and email are required.")
        if student_id in db.students:
            raise ValueError(f"Student '{student_id}' already exists.")
        student = {
            "student_id": student_id,
            "name": name,
            "email": email,
            "semester": int(semester),
        }
        db.students[student_id] = student
        return student

    @staticmethod
    def get_student(student_id):
        return db.students.get(student_id)

    @staticmethod
    def list_students():
        return list(db.students.values())

    @staticmethod
    def list_courses():
        return list(db.courses.values())

    @staticmethod
    def enroll_student(student_id, course_id):
        student = db.students.get(student_id)
        course = db.courses.get(course_id)

        if not student:
            raise ValueError(f"Student '{student_id}' not found.")
        if not course:
            raise ValueError(f"Course '{course_id}' not found.")

        if any(
            e["student_id"] == student_id
            and e["course_id"] == course_id
            and e["semester"] == student["semester"]
            for e in db.enrollments
        ):
            raise ValueError("Student is already enrolled in this course.")

        current_credits = sum(
            db.courses[e["course_id"]]["credits"]
            for e in db.enrollments
            if (
                e["student_id"] == student_id
                and e["semester"] == student["semester"]
            )
        )

        if (
            current_credits + course["credits"]
            > StudentService.MAX_SEMESTER_CREDITS
        ):
            raise ValueError(
                "Semester credit limit exceeded "
                f"(Max: {StudentService.MAX_SEMESTER_CREDITS})."
            )

        enrollment = {
            "enrollment_id": f"E-{len(db.enrollments) + 1:04d}",
            "student_id": student_id,
            "course_id": course_id,
            "semester": student["semester"],
            "status": "ENROLLED",
        }
        db.enrollments.append(enrollment)
        return enrollment

    @staticmethod
    def get_enrollments(student_id=None):
        if student_id:
            return [
                e for e in db.enrollments
                if e["student_id"] == student_id
            ]
        return list(db.enrollments)
