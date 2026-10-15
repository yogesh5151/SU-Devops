from database.db import db


GRADE_POINTS = {
    "A+": 10.0,
    "A": 9.0,
    "B+": 8.0,
    "B": 7.0,
    "C": 6.0,
    "D": 5.0,
    "F": 0.0,
}


class MarksManagement:
    """Academic grade storage and GPA calculation."""

    @staticmethod
    def record_grade(student_id, course_id, grade):
        if student_id not in db.students:
            raise ValueError(f"Student '{student_id}' not found.")
        if course_id not in db.courses:
            raise ValueError(f"Course '{course_id}' not found.")
        if grade not in GRADE_POINTS:
            raise ValueError(f"Invalid grade '{grade}'.")
        if not any(
            e["student_id"] == student_id and e["course_id"] == course_id
            for e in db.enrollments
        ):
            raise ValueError(
                "Student must be enrolled before a grade can be recorded."
            )

        existing = next(
            (
                g for g in db.grades
                if g["student_id"] == student_id
                and g["course_id"] == course_id
            ),
            None,
        )
        if existing:
            existing["grade"] = grade
            existing["grade_point"] = GRADE_POINTS[grade]
            return existing

        record = {
            "student_id": student_id,
            "course_id": course_id,
            "grade": grade,
            "grade_point": GRADE_POINTS[grade],
        }
        db.grades.append(record)
        return record

    @staticmethod
    def get_grades(student_id):
        return [g for g in db.grades if g["student_id"] == student_id]

    @staticmethod
    def calculate_gpa(student_id):
        grades = MarksManagement.get_grades(student_id)
        if not grades:
            return 0.0

        total_quality_points = 0.0
        total_credits = 0
        for grade in grades:
            credits = db.courses[grade["course_id"]]["credits"]
            total_quality_points += grade["grade_point"] * credits
            total_credits += credits

        return round(total_quality_points / total_credits, 2)
