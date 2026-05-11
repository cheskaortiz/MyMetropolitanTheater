from service.department_service import DepartmentService
from service.staff_service import StaffService

class Service:
    def __init__(self, conn):
        self.department = DepartmentService(conn)
        self.staff = StaffService(conn)