from datetime import date
from models import Production, Performance

class ProductionManager:
    def __init__(self):
        self.productions: list[Production] = []
        self.performances: list[Performance] = []

    def add_production(self):
        print("Add Production")
        num = len(self.productions) + 1
        title = input("Title: ")
        start_date = date.fromisoformat(input("Start Date (YYYY-MM-DD):     "))
        end_date = date.fromisoformat(input("End Date (YYYY-MM-DD):     "))

        self.productions.append(Production(num, title, start_date, end_date))
        print(f'"{title}" added successfully!')
    
    def add_performance(self):
        print("\n--- Add Performance ---")
        if not self.productions:
            print("No productions yet. Add a production first.")
            return

        self.display_productions()
        prod_num  = int(input("Enter Production # to link: "))
        perf_id   = len(self.performances) + 1
        perf_date = date.fromisoformat(input("Performance Date (YYYY-MM-DD): "))
        perf_time = input("Performance Time (e.g. 7:00 PM): ")

        self.performances.append(Performance(perf_id, prod_num, perf_date, perf_time))
        print("Performance added!")

    def display_productions(self):
        print("\n--- Productions ---")
        if not self.productions:
            print("No productions yet.")
            return
        for p in self.productions:
            print(f"  [{p.production_num}] {p.title}")
            print(f"       From : {p.start_date}  To: {p.end_date}")

    def display_performances(self):
        print("\n--- Performances ---")
        if not self.performances:
            print("No performances yet.")
            return
        for p in self.performances:
            prod  = next((x for x in self.productions if x.production_num == p.production_num), None)
            title = prod.title if prod else "Unknown"
            print(f"  [{p.performance_id}] {title}")
            print(f"       Date : {p.perf_date}  Time: {p.perf_time}")

    def menu(self):
        while True:
            print("\n=== Productions & Performances ===")
            print("1. Add production")
            print("2. Add performance")
            print("3. Display productions")
            print("4. Display performances")
            print("5. Back")
            choice = input("Choose: ")
            if   choice == "1": self.add_production()
            elif choice == "2": self.add_performance()
            elif choice == "3": self.display_productions()
            elif choice == "4": self.display_performances()
            elif choice == "5": break
            else: print("Invalid choice.")