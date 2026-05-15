from service.department_service import DepartmentService
from service.staff_service import StaffService
from service.log_in_service import LogInService
from service.work_log_service import WorkLogService

class Service:
    def __init__(self, conn):
        self.department = DepartmentService(conn)
        self.staff = StaffService(conn)
        self.log_in = LogInService(conn)
        self.work_log = WorkLogService(conn)