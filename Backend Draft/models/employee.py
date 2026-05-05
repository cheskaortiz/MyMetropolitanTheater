from dataclasses import dataclass

@dataclass
class Employee:
    employee_id: int
    name:        str
    emp_type:    str
    department:  str
    salary:      float