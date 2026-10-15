from dataclasses import dataclass


@dataclass
class Student:
    student_id: str
    name: str
    email: str
    semester: int
