from repository.performanceSeatRepo import PerformanceSeatRepo
from repository.seatRepo import SeatRepo
from repository.performanceRepo import PerformanceRepo
from repository.ticketRepo import TicketRepo
from decimal import Decimal, InvalidOperation


class PerformanceSeatService:
    def __init__(self, conn):
        self.performanceSeatRepo = PerformanceSeatRepo(conn)
        self.seatRepo = SeatRepo(conn)
        self.performanceRepo = PerformanceRepo(conn)
        self.ticketRepo = TicketRepo(conn)

    # creates a performance seat after validating seat, performance, price, and availability
    # requirement: seats must be assigned to a performance before tickets can be sold
    def createPerformanceSeat(self, performanceSeat):
        validation = self.__checkPerformanceSeat(performanceSeat)

        if validation is True:
            self.performanceSeatRepo.createPerformanceSeat(performanceSeat)
            return "Successfully created performance seat."

        return validation

    # updates seat price or availability after validating the performance seat exists
    # requirement: Modify the price and arrangement of seats for each performance (before/after snapshot)
    def updatePerformanceSeat(self, performanceSeat):
        if performanceSeat.performanceSeatId is None:
            return "Invalid performanceSeatId."

        try:
            performanceSeat.performanceSeatId = int(performanceSeat.performanceSeatId)
        except ValueError:
            return "Invalid performanceSeatId. Must be a number."

        if self.performanceSeatRepo.locatePerformanceSeatId(performanceSeat.performanceSeatId) is None:
            return "Performance seat does not exist."

        validation = self.__checkPerformanceSeat(performanceSeat, isUpdate=True)

        if validation is True:
            self.performanceSeatRepo.updatePerformanceSeat(performanceSeat)
            return "Successfully updated performance seat."

        return validation

    # retrieves all performance seat records
    def viewAllPerformanceSeats(self):
        return self.performanceSeatRepo.getAllPerformanceSeats()
    
    def deletePerformanceSeat(self, performanceSeatId):
        try:
            performanceSeatId = int(performanceSeatId)
        except (ValueError, TypeError):
            return "Invalid performance seat ID."

        performanceSeat = self.performanceSeatRepo.locatePerformanceSeatId(performanceSeatId)

        if not performanceSeat:
            return "Performance seat does not exist."

        existingTicket = self.ticketRepo.locateTicketByPerformanceSeatId(performanceSeatId)

        if existingTicket:
            return "Cannot delete performance seat because it already has an existing ticket."

        self.performanceSeatRepo.deletePerformanceSeat(performanceSeatId)

        return "Successfully deleted performance seat."

    # retrieves all seats for a performance including unavailable ones — full seat map
    # requirement: Theater Seat Map
    def viewAllSeatsByPerformance(self, performanceId):
        validation = self.checkPerformanceId(performanceId)

        if validation is not True:
            return validation

        return self.performanceSeatRepo.getAllSeatsByPerformance(int(performanceId))

    # retrieves only available seats for a performance
    # requirement: Purchase Tickets by Performance — only show seats customer can select
    def viewAvailableSeatsByPerformance(self, performanceId):
        validation = self.checkPerformanceId(performanceId)

        if validation is not True:
            return validation

        return self.performanceSeatRepo.getAvailableSeatsByPerformance(int(performanceId))

    # retrieves seat pricing for a performance
    # requirement: Seat Pricing — shows prices per seat per performance
    def viewSeatPricingByPerformance(self, performanceId):
        validation = self.checkPerformanceId(performanceId)

        if validation is not True:
            return validation

        return self.performanceSeatRepo.getSeatPricingByPerformance(int(performanceId))

    # locates a performance seat by ID — used before update
    def locatePerformanceSeatId(self, performanceSeatId):
        try:
            performanceSeatId = int(performanceSeatId)
        except ValueError:
            return "Invalid performanceSeatId. Must be a number."

        performanceSeat = self.performanceSeatRepo.locatePerformanceSeatId(performanceSeatId)

        if performanceSeat:
            return performanceSeat

        return "Performance seat does not exist."

    # locates a performance seat by seat and performance combination
    # used to prevent assigning the same seat twice to one performance
    def locatePerformanceSeatBySeatAndPerformance(self, seatId, performanceId):
        try:
            seatId = int(seatId)
            performanceId = int(performanceId)
        except ValueError:
            return "Seat ID and performance ID must be numbers."

        performanceSeat = self.performanceSeatRepo.locatePerformanceSeatBySeatAndPerformance(
            seatId,
            performanceId
        )

        if performanceSeat:
            return performanceSeat

        return "Performance seat does not exist."

    # validates all performance seat fields
    # checks: seat exists, performance exists, price > 0, valid availability, no duplicate seat-performance
    def __checkPerformanceSeat(self, performanceSeat, isUpdate=False):
        try:
            performanceSeat.seatId = int(performanceSeat.seatId)
        except ValueError:
            return "Invalid seatId. Must be a number."

        try:
            performanceSeat.performanceId = int(performanceSeat.performanceId)
        except ValueError:
            return "Invalid performanceId. Must be a number."

        if self.seatRepo.locateSeatId(performanceSeat.seatId) is None:
            return "Seat does not exist."

        if self.performanceRepo.locatePerformanceId(performanceSeat.performanceId) is None:
            return "Performance does not exist."

        try:
            performanceSeat.price = Decimal(str(performanceSeat.price))
        except InvalidOperation:
            return "Invalid price. Must be a number."

        if performanceSeat.price <= 0:
            return "Performance seat price must be greater than zero."

        isAvailable = self.convertToBoolean(performanceSeat.isAvailable)

        if isAvailable is None:
            return "Performance seat availability must be True or False."

        performanceSeat.isAvailable = isAvailable

        existingPerformanceSeat = self.performanceSeatRepo.locatePerformanceSeatBySeatAndPerformance(
            performanceSeat.seatId,
            performanceSeat.performanceId
        )

        if existingPerformanceSeat:
            existingPerformanceSeatId = existingPerformanceSeat[0]

            if not isUpdate or existingPerformanceSeatId != performanceSeat.performanceSeatId:
                return "This seat is already assigned to this performance."

        return True

    # validates that a performance ID exists in the database
    def checkPerformanceId(self, performanceId):
        try:
            performanceId = int(performanceId)
        except ValueError:
            return "Invalid performanceId. Must be a number."

        if self.performanceRepo.locatePerformanceId(performanceId) is None:
            return "Performance does not exist."

        return True

    # converts string input to boolean for is_available field
    def convertToBoolean(self, value):
        if isinstance(value, bool):
            return value

        if isinstance(value, str):
            value = value.strip().lower()

            if value in ["true", "t", "yes", "1"]:
                return True

            if value in ["false", "f", "no", "0"]:
                return False

        return None