# CREATE TABLE Ticket (
#     performance_seat_id INTEGEr NOT NULL,
# 	ticket_id INTEGER PRIMARY KEY,
#     customer_id INTEGER NOT NULL,
#     status VARCHAR(50),
#     ticket_number VARCHAR(100),
#     sale_date DATE,
#     FOREIGN KEY (performance_seat_id) REFERENCES Performance_Seat(performance_seat_id),
#     FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
# );

class Ticket:
    def __init__ (self, performanceSeatId=None, customerId=None, status=None, ticketNumber=None, saleDate=None, ticketId=None):
        self.performanceSeatId = performanceSeatId
        self.ticketId = ticketId
        self.customerId = customerId
        self.status = status
        self.ticketNumber = ticketNumber
        self.saleDate = saleDate