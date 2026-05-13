# CREATE TABLE Transactions (
#     transaction_id INTEGER PRIMARY KEY,
#     ticket_id INTEGER NOT NULL,
#     staff_id INTEGER,
#     transaction_date DATE,
#     type VARCHAR(50),
#     amount DOUBLE PRECISION,
#     FOREIGN KEY (ticket_id) REFERENCES Ticket(ticket_id),
#     FOREIGN KEY (staff_id)  REFERENCES Staff(staff_id)
# );


class Transaction:
    def __init__(self, transactionId=None, ticketId=None, staffId=None, transactionDate=None, type=None, amount=None):
        self.transactionId = transactionId
        self.ticketId = ticketId
        self.staffId = staffId
        self.transactionDate = transactionDate
        self.type = type
        self.amount = amount

