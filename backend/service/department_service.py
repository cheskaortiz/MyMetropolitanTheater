from repository.department_repo import DepartmentRepo
from repository.staff_repo import StaffRepo
from repository.log_in_repo import LogInRepo
from objects.log_in_obj import LogIn

class DepartmentService:
    def __init__(self, conn):
        self.dept_repo = DepartmentRepo(conn)
        self.staff_repo = StaffRepo(conn)
        self.log_in = LogInRepo(conn)

    # the needed attribute in creating new department is name (name of department) and manager_id (staff_id of staff to be manager)
    def create_department(self, dept):
        validation = self.__check_department(dept)

        if validation is True:
            self.dept_repo.create_department(dept)
            self.__create_log_in(dept)
            return "Successfully created department."
        
        return validation

    def update_department(self, dept):
        validation = self.__check_department(dept)

        if dept.id is None:
            return "Invalid department_id."

        if validation is True:
            self.dept_repo.update_department(dept)
            self.__create_log_in(dept)
            return "Successfully updated department."
        
        return validation
    
    # the needed attribute in udpating department is dept_id, name (department name), manager_id (staff_if of the presumed manager)
    def delete_department(self, dept_id):
        try:
            dept_id = int(dept_id)

            if self.dept_repo.locate_department_id(dept_id):
                self.dept_repo.delete_department(dept_id)
                return "Department deleted."
            else:
                return "Invalid department_id."
            
        except ValueError:
            return "Invalid department_id. Must be a number."
    
    # get department and its staff
    def get_department(self, dept_name):
        dept = self.dept_repo.get_department(dept_name)

        if dept is None:
            return "Department does not exist"
        
        staffs = []
        for staff in dept:
            if staff[1] is None:
                return "No employee available."
            
            staffs.append({
                "dept_name": staff[0],
                "staff_id": staff[1],
                "staff_name": staff[2],
                "staff_type": staff[3]
            })
        return staffs
         
    def __check_department(self, dept):
        try:
            dept.manager_id = int(dept.manager_id)
        except ValueError:
            return "Invalid manager_id. Must be a number."

        is_name_valid = dept.dept_name.replace(" ", "").isalpha()
        is_staff = self.staff_repo.locate_staff(dept.manager_id)
        is_already_manager = self.dept_repo.locate_manager(dept.manager_id)
        is_dept_name_exists = self.dept_repo.locate_department_name(dept.dept_name)

        if is_dept_name_exists:
            return "Department name already exists."

        if not is_staff:
            return "Staff does not exist."

        if is_already_manager:
            return "This staff is already assigned as a manager."

        if not is_name_valid:
            return "Department name must only contain letters and spaces."

        return True
    
    def __create_log_in(self, dept):
        staff = self.staff_repo.locate_staff(dept.manager_id)

        if self.log_in.locate_staff(dept.manager_id) is None:
            password = staff[1].replace(" ", ".") + "." + str(dept.manager_id) + "@mmt"
            self.log_in.create_log_in(LogIn(staff_id=id, password=password))

        
        
        


        