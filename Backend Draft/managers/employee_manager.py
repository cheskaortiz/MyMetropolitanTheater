from models import Employee

class EmployeeManager:
    def __init__(self):
        self.employees: list[Employee] = []

    def add_employee(self):
        print("\n--- Add Employee ---")
        emp_id     = len(self.employees) + 1
        name       = input("Name: ")
        print("Type: 1-Full-time  2-Sales Agent  3-Entertainer")
        t          = input("Choose type: ")
        emp_type   = {"1":"full-time","2":"sales agent","3":"entertainer"}.get(t, "full-time")
        department = input("Department: ")
        salary     = float(input("Salary: "))

        self.employees.append(Employee(emp_id, name, emp_type, department, salary))
        print(f'"{name}" added!')

    def display_employees(self):
        print("\n--- Employees ---")
        if not self.employees:
            print("No employees yet.")
            return
        for e in self.employees:
            print(f"  [{e.employee_id}] {e.name}  ({e.emp_type})  —  {e.department}  —  PHP {e.salary:.2f}")

    def menu(self):
        while True:
            print("\n=== Employee Manager ===")
            print("1. Add employee")
            print("2. Display employees")
            print("3. Back")
            choice = input("Choose: ")
            if   choice == "1": self.add_employee()
            elif choice == "2": self.display_employees()
            elif choice == "3": break
            else: print("Invalid choice.")