import threading


class Database:
    """Thread-safe in-memory data store for the academic platform."""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._init_db()
            return cls._instance

    def _init_db(self):
        self.students = {}
        self.faculty = {}
        self.courses = {}
        self.enrollments = []
        self.grades = []
        self._seed_initial_data()

    def _seed_initial_data(self):
        self.students["S101"] = {
            "student_id": "S101",
            "name": "Aarav Patil",
            "email": "aarav@university.edu",
            "semester": 2,
        }
        self.students["S102"] = {
            "student_id": "S102",
            "name": "Isha Sharma",
            "email": "isha@university.edu",
            "semester": 2,
        }

        self.faculty["F101"] = {
            "faculty_id": "F101",
            "name": "Dr. Neha Kulkarni",
            "email": "neha.kulkarni@university.edu",
            "department": "Computer Science",
        }

        self.courses["C101"] = {
            "course_id": "C101",
            "name": "Data Structures",
            "credits": 4,
            "faculty_id": "F101",
        }
        self.courses["C102"] = {
            "course_id": "C102",
            "name": "Database Management Systems",
            "credits": 4,
            "faculty_id": "F101",
        }
        self.courses["C103"] = {
            "course_id": "C103",
            "name": "Operating Systems",
            "credits": 4,
            "faculty_id": "F101",
        }
        self.courses["C104"] = {
            "course_id": "C104",
            "name": "Computer Networks",
            "credits": 3,
            "faculty_id": "F101",
        }
        self.courses["C105"] = {
            "course_id": "C105",
            "name": "Software Engineering",
            "credits": 3,
            "faculty_id": "F101",
        }

    def reset(self):
        with self._lock:
            self.students.clear()
            self.faculty.clear()
            self.courses.clear()
            self.enrollments.clear()
            self.grades.clear()
            self._seed_initial_data()


db = Database()
