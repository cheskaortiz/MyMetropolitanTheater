
# CREATE TABLE Performance_Seat (
#     performance_seat_id INTEGER PRIMARY KEY,
#     seat_id INTEGER NOT NULL,
#     price DOUBLE PRECISION,
#     is_available BOOLEAN,
# 	performance_id INTEGER NOT NULL,
#     FOREIGN KEY (seat_id) REFERENCES Seat(seat_id),
#     FOREIGN KEY (performance_id) REFERENCES Performance(performance_id)
# );

class PerformanceSeat:
    def __init__ (self, seatId=None, price=None, isAvailable=None, performanceId=None, performanceSeatId=None):
        self.performanceSeatId = performanceSeatId
        self.seatId = seatId
        self.price = price
        self.isAvailable = isAvailable
        self.performanceId = performanceId