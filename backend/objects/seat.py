# CREATE TABLE Seat (
#     seat_id INTEGER PRIMARY KEY,
#     seat_view VARCHAR(100),
#     seat_number VARCHAR(20)
# );

class Seat:
    def __init__ (self, seatId=None, seatView=None, seatNumber=None):
        self.seatId = seatId
        self.seatView = seatView
        self.seatNumber = seatNumber
    