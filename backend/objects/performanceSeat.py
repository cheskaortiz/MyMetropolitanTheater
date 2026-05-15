class PerformanceSeat:
    def __init__ (self, seatId=None, price=None, isAvailable=None, performanceId=None, performanceSeatId=None):
        self.performanceSeatId = performanceSeatId
        self.seatId = seatId
        self.price = price
        self.isAvailable = isAvailable
        self.performanceId = performanceId