class Ticket:
    def __init__ (self, performanceSeatId=None, customerId=None, status=None, ticketNumber=None, saleDate=None, ticketId=None):
        self.performanceSeatId = performanceSeatId
        self.ticketId = ticketId
        self.customerId = customerId
        self.status = status
        self.ticketNumber = ticketNumber
        self.saleDate = saleDate