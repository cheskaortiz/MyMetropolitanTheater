from repository.log_in_repo import LogInRepo
from repository.department_repo import DepartmentRepo
from repository.commissioned_repo import CommissionedRepo

class LogInService:
    def __init__(self, conn):
        self.log_in_repo = LogInRepo(conn)
        self.commissioned_repo = CommissionedRepo(conn)
        self.department_repo = DepartmentRepo(conn)

    # returns staff_id
    def log_in(self, log_in):
        details = self.log_in_repo.get_log_in(log_in.staff_id)
        if details is None:
            return "Invalid log in credentials. User not found"
        
        if details[2] != log_in.password:
            return "Wrong password."

        # if the returned value is a list then successful log in
        return log_in.staff_id
    
    # method to check if current person logged in is manager
    def is_manager(self, staff_id):
        if self.department_repo.locate_manager(staff_id) is not None:
            return True
        return False
    
    # method to check if current person logged is sales
    def is_sales(self, staff_id):
        if self.commissioned_repo.locate_staff(staff_id) is not None:
            return True
        return False
    

