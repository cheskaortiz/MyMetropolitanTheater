from repository.staff_repo import StaffRepo
from repository.department_repo import DepartmentRepo
from repository.log_in_repo import LogInRepo
from repository.hourly_repo import HourlyRepo
from repository.commissioned_repo import CommissionedRepo
from repository.full_time_repo import FullTimeRepo
from objects.log_in_obj import LogIn
from objects.staff_obj import Staff
from objects.hourly_obj import Hourly
from objects.commissioned_obj import Commissioned
from objects.full_time_obj import FullTime

class StaffService:
    def __init__(self, conn):
        self.staff_repo = StaffRepo(conn)
        self.dept_repo = DepartmentRepo(conn)
        self.log_in = LogInRepo(conn)
        self.hourly_repo = HourlyRepo(conn)
        self.commission_repo = CommissionedRepo(conn)
        self.full_time_repo = FullTimeRepo(conn)
    
    # the needed attribute in creating new staff is dept_id, name, staff_type
    # famous_level is REQUIRED if staff_type is hourly
    # monthly_salary is REQUIRED if staff_type is full_time
    def create_staff(self, staff, famous_level=None, monthly_salary=None):
        validation = self.__check_staff(staff, famous_level, monthly_salary)

        if validation is True:
            id = self.staff_repo.create_staff(staff)
            self.__create_staff_type(Staff(id, name=staff.name, staff_type=staff.staff_type), famous_level, monthly_salary)
            self.__create_log_in(Staff(id, name=staff.name, staff_type=staff.staff_type))
            return "Successfully added staff."
        
        return validation

    # the needed attribute in udpating staff is staff_id, dept_id, name, staff_type
    # famous_level is REQUIRED if staff_type is hourly
    # monthly_salary is REQUIRED if staff_type is full_time
    def update_staff(self, staff, famous_level=None, monthly_salary=None):
        validation = self.__check_staff(staff, famous_level, monthly_salary)

        if staff.staff_id is None:
            return "Invalid staff_id."

        if validation is True:
            self.staff_repo.update_staff(staff)
            self.__remove_from_old_type(staff.staff_id)
            self.__create_staff_type(staff, famous_level, monthly_salary)
            self.__create_log_in(staff)
            return "Successfully updated staff."
        
        return validation

    # this returns a dictionary that contains the staff name, staff_type, department, salary
    def get_staffs(self):
        all_staffs = self.staff_repo.get_all_staff()

        staffs = []
        for staff in all_staffs:
            staffs.append({
                "name": staff[0],
                "type": staff[1],
                "department": staff[2],
                "salary": 0.0 if staff[3] is None else staff[3]
            })
        
        return staffs
    
    # this returns all staff in the sales department in descending order based on their commissions
    def get_sales_staff(self):
        sales_agents = self.staff_repo.get_sales_staff()

        sales = []
        for staff in sales_agents:
            sales.append({
                "name": staff[0],
                "type": staff[1],
                "department": staff[2],
                "salary": 0.0 if staff[3] is None else staff[3]
            })
        
        return sorted(sales, key=lambda x : x["salary"], reverse=True)
    
    # the needed parameter is the satff_id
    # this delete staff using their staff_id
    def delete_staff(self, staff_id):
        try:
            staff_id= int(staff_id)

            if self.staff_repo.locate_staff(staff_id):
                self.staff_repo.delete_staff(staff_id)
                return "Staff deleted."
            else:
                return "Invalid staff_id."
            
        except ValueError:
            return "Invalid _id. Must be a number."

    def __check_staff(self, staff, famous_level, monthly_salary):
        try:
            staff.dept_id = int(staff.dept_id)
        except ValueError:
            return "Invalid staff_id and/or dept_id. Must be a number."
        
        if monthly_salary is not None:
            try:
                monthly_salary = float(monthly_salary)
            except ValueError:
                return "Invalid monthly salary. Must be a number."

        if famous_level is not None:
            try:
                famous_level = int(famous_level)
            except ValueError:
                return "Invalid famous level. Only contains numbers 1 (lowest) to 5 (highest)."

        is_valid_type = self.__check_staff_type(staff.staff_type)
        is_type_and_department_match = self.__check_department_and_type(staff)
        is_name_valid = staff.name.replace(" ", "").isalpha()
        is_department_exist = self.dept_repo.locate_department_id(staff.dept_id)

        if not is_department_exist:
            return "Department does not exists."

        if not is_name_valid:
            return "Name must only contain letters and spaces."
        
        if not is_valid_type:
            return "Staff types are only 'Full Time', 'Hourly', or 'Commissioned'"
        
        if not is_type_and_department_match:
            return "Staff types and department does not match."
        
        if staff.staff_type == "Hourly" and famous_level is None:
            return "Include famous level of actor/actress to determine hourly rate."
        
        if staff.staff_type == "Full Time" and monthly_salary is None:
            return "Include monthly salary."

        if famous_level is not None and famous_level not in [1, 2, 3, 4, 5]:
            return "Famous level only ranges from 1 (lowest) to 5 (highest)"

        return True
    
    def __check_staff_type(self, type):
        if type == "Full Time" or type == "Hourly" or type == "Commissioned":
            return True
        return False

    def __check_department_and_type(self, staff):
        if staff.staff_type == "Commissioned" and staff.dept_id != 2:
            return False
        return True

    # log_in credentials are automatic
    def __create_log_in(self, staff):
    # Sales (Commissioned) staff get login credentials
        if staff.staff_type == "Commissioned" and self.log_in.locate_staff(staff.staff_id) is None:
            password = staff.name.replace(" ", ".") + "." + str(staff.staff_id) + "@mmt"
            self.log_in.create_log_in(LogIn(staff_id=staff.staff_id, password=password))

    # Managers also get login credentials
        if self.dept_repo.locate_manager(staff.staff_id) is not None and self.log_in.locate_staff(staff.staff_id) is None:
            password = staff.name.replace(" ", ".") + "." + str(staff.staff_id) + "@mmt"
            self.log_in.create_log_in(LogIn(staff_id=staff.staff_id, password=password))

    def __create_staff_type(self, staff, famous_level=None, monthly_salary=None):
        if staff.staff_type == "Hourly":
            self.hourly_repo.create_hourly(Hourly(staff.staff_id, self.__match_famous_level(famous_level), famous_level))
        elif staff.staff_type == "Commissioned":
            self.commission_repo.create_commission(Commissioned(staff.staff_id))
        else:
            self.full_time_repo.create_full_time(FullTime(staff.staff_id, monthly_salary))

    
    def __match_famous_level(self, famous_level):
        if famous_level == 1:
            return float(150.00)
        elif famous_level == 2:
            return float(300.00)
        elif famous_level == 3:
            return float(500.00)
        elif famous_level == 4:
            return float(700.00)
        elif famous_level == 5:
            return float(1000.00)
    
    def __remove_from_old_type(self, staff_id):
        if self.commission_repo.locate_staff(staff_id): 
            self.commission_repo.delete_commissioned(staff_id)
        
        if self.hourly_repo.locate_staff(staff_id): 
            self.hourly_repo.delete_hourly(staff_id)
        
        if self.full_time_repo.locate_staff(staff_id): 
            self.full_time_repo.delete_full_time(staff_id)
