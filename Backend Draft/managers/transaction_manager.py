from models                      import Transaction
from managers.production_manager import ProductionManager
from managers.seat_manager       import SeatManager
from managers.employee_manager   import EmployeeManager

class TransactionManager:
    def __init__(self, production_manager: ProductionManager,
                       seat_manager:       SeatManager,
                       employee_manager:   EmployeeManager):
        self.transactions       = []
        self.production_manager = production_manager
        self.seat_manager       = seat_manager
        self.employee_manager   = employee_manager

    def _generate_ticket_num(self, production_num, performance_id, title):
        last3 = title[-3:].lower()
        return f"{production_num}{last3}{performance_id:04d}"

    def add_transaction(self):
        print("\n--- New Transaction ---")
        print("Type: 1-Purchase  2-Refund  3-Reservation")
        t        = input("Choose type: ")
        txn_type = {"1":"purchase","2":"refund","3":"reservation"}.get(t, "purchase")

        self.seat_manager.display_seats()
        seat_id = int(input("Seat ID: "))

        self.production_manager.display_performances()
        perf_id = int(input("Performance ID: "))

        self.employee_manager.display_employees()
        emp_id  = int(input("Employee ID (sales agent): "))

        prod = next((x for x in self.production_manager.productions
                     if x.production_num ==
                     next((p.production_num for p in self.production_manager.performances
                           if p.performance_id == perf_id), None)), None)

        ticket_num = self._generate_ticket_num(
            prod.production_num if prod else 0,
            perf_id,
            prod.title if prod else "unk"
        )

        txn_id = len(self.transactions) + 1
        self.transactions.append(
            Transaction(txn_id, ticket_num, txn_type, seat_id, perf_id, emp_id)
        )
        print(f"Transaction done! Ticket #: {ticket_num}")

    def display_transactions(self):
        print("\n--- Transactions ---")
        if not self.transactions:
            print("No transactions yet.")
            return
        for t in self.transactions:
            print(f"  [{t.transaction_id}] Ticket: {t.ticket_number}  Type: {t.txn_type}")
            print(f"       Seat: {t.seat_id}  Perf: {t.performance_id}  Agent: {t.employee_id}")

    def menu(self):
        while True:
            print("\n=== Transaction Manager ===")
            print("1. New transaction")
            print("2. Display transactions")
            print("3. Back")
            choice = input("Choose: ")
            if   choice == "1": self.add_transaction()
            elif choice == "2": self.display_transactions()
            elif choice == "3": break
            else: print("Invalid choice.")