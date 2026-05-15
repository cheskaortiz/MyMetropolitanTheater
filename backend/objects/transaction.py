class Transaction:
    def __init__(self, transactionId=None, ticketId=None, staffId=None, transactionDate=None, type=None, amount=None):
        self.transactionId = transactionId
        self.ticketId = ticketId
        self.staffId = staffId
        self.transactionDate = transactionDate
        self.type = type
        self.amount = amount

