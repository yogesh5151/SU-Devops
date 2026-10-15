from dataclasses import dataclass


@dataclass
class Faculty:
    faculty_id: str
    name: str
    email: str
    department: str
