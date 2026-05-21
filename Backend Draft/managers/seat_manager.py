from models import Seat

class SeatManager:
    def __init__(self):
        self.seats: list[Seat] = []
    
    def add_seat(self):
        print("\n--- Add Seat ---")
        seat_id = len(self.seats) + 1
        location = input("Seat Location (e.g. A1, B2): ")
        price = float(input("Seat Price: "))

        self.seats.append(Seat(seat_id, location, price))
        print(f"Seat {location} added successfully!")

    def display_seats(self):
        print("\n--- Seats ---")
        if not self.seats:
            print("No seats yet.")
            return
        for s in self.seats:
            print(f"[{s.seat_id}{s.seat_location}] - PHP {s.price:.2f}")

    def menu(self):
        while True:
            print("\n=== Seat Management ===")
            print("1. Add seat")
            print("2. Display seats")
            print("3. Back")
            choice = input("Choose: ")

            if choice == '1':
                self.add_seat()
            elif choice == '2':
                self.display_seats()
            elif choice == '3':
                break
            else:
                print()

