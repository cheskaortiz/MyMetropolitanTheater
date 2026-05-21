from managers.production_manager  import ProductionManager
from managers.seat_manager        import SeatManager
from managers.employee_manager    import EmployeeManager
from managers.transaction_manager import TransactionManager

class MMTSystem:
    def __init__(self):
        self.production_manager  = ProductionManager()
        self.seat_manager        = SeatManager()
        self.employee_manager    = EmployeeManager()
        self.transaction_manager = TransactionManager(
            self.production_manager,
            self.seat_manager,
            self.employee_manager
        )

    def run(self):
        while True:
            print("\n====== My Metropolitan Theater ======")
            print("1. Productions & Performances")
            print("2. Seats")
            print("3. Employees")
            print("4. Transactions")
            print("5. Exit")
            choice = input("Choose: ")
            if   choice == "1": self.production_manager.menu()
            elif choice == "2": self.seat_manager.menu()
            elif choice == "3": self.employee_manager.menu()
            elif choice == "4": self.transaction_manager.menu()
            elif choice == "5": print("Goodbye!"); break
            else: print("Invalid choice.")