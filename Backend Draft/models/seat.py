from dataclasses import dataclass

@dataclass
class Seat:
    seat_id:       int
    seat_location: str
    price:         float