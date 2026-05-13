from repository.performanceRepo import PerformanceRepo
from repository.productionRepo import ProductionRepo
from datetime import datetime


class PerformanceService:
    def __init__(self, conn):
        self.performanceRepo = PerformanceRepo(conn)
        self.productionRepo = ProductionRepo(conn)

    # creates a new performance schedule for a production
    def createPerformance(self, performance):
        validation = self.__checkPerformance(performance)

        if validation is True:
            self.performanceRepo.createPerformance(performance)
            return "Successfully created performance."

        return validation

    # updates an existing performance schedule
    def updatePerformance(self, performance):
        if performance.performanceId is None:
            return "Invalid performanceId."

        try:
            performance.performanceId = int(performance.performanceId)
        except ValueError:
            return "Invalid performanceId. Must be a number."

        if self.performanceRepo.locatePerformanceId(performance.performanceId) is None:
            return "Performance does not exist."

        validation = self.__checkPerformance(performance, isUpdate=True)

        if validation is True:
            self.performanceRepo.updatePerformance(performance)
            return "Successfully updated performance."

        return validation

    # deletes a performance if there are no tickets connected to it
    def deletePerformance(self, performanceId):
        try:
            performanceId = int(performanceId)
        except ValueError:
            return "Invalid performanceId. Must be a number."

        if self.performanceRepo.locatePerformanceId(performanceId) is None:
            return "Performance does not exist."

        if self.performanceRepo.hasTicketsForPerformance(performanceId):
            return "Cannot delete performance because it already has tickets."

        self.performanceRepo.deletePerformance(performanceId)
        return "Performance deleted."

    # retrieves all performances
    def viewAllPerformances(self):
        return self.performanceRepo.getAllPerformance()
    
    def locatePerformanceId(self, performanceId):
        try:
            performanceId = int(performanceId)
        except ValueError:
            return "Invalid performanceId. Must be a number."

        performance = self.performanceRepo.locatePerformanceId(performanceId)

        if performance:
            return performance

        return "Performance does not exist."

    # locates start time and entime of performance using performance_id
    def locatePerformancebyPerformanceId(self, performanceId):
        try:
            performanceId = int(performanceId)
        except ValueError:
            return "Invalid performanceId. Must be a number."

        performance = self.performanceRepo.locatePerformanceByPerformanceId(performanceId)

        if performance:
            return performance

        return "Performance does not exist."

    # locates all performances under one production
    def locatePerformanceByProductionId(self, productionId):
        try:
            productionId = int(productionId)
        except ValueError:
            return "Invalid productionId. Must be a number."

        performances = self.performanceRepo.locatePerformanceByProductionId(productionId)

        if performances:
            return performances

        return "No performances found for this production."

    # locates all performances scheduled on a specific date
    def locatePerformanceByDate(self, date):
        if date is None or str(date).strip() == "":
            return "Performance date is required."

        try:
            datetime.strptime(str(date), "%Y-%m-%d")
        except ValueError:
            return "Invalid date format. Use YYYY-MM-DD."

        performances = self.performanceRepo.locatePerformanceByDate(date)

        if performances:
            return performances

        return "No performances found on this date."

    # locates a performance by production, date, start time, and end time
    def locatePerformanceSchedule(self, productionId, date, startTime, endTime):
        try:
            productionId = int(productionId)
        except ValueError:
            return "Invalid productionId. Must be a number."

        try:
            date = self.convertDate(date)
            startTime = self.convertTime(startTime)
            endTime = self.convertTime(endTime)
        except ValueError:
            return "Invalid date or time format."

        performance = self.performanceRepo.locatePerformanceSchedule(
            productionId,
            date,
            startTime,
            endTime
        )

        if performance:
            return performance

        return "Performance schedule does not exist."

    # validates performance details before create or update
    def __checkPerformance(self, performance, isUpdate=False):
        if performance.productionId is None:
            return "Production ID is required."

        if performance.startTime is None:
            return "Start time is required."

        if performance.endTime is None:
            return "End time is required."

        if performance.date is None:
            return "Performance date is required."

        if performance.totalSeats is None:
            return "Total seats is required."

        try:
            performance.productionId = int(performance.productionId)
        except ValueError:
            return "Invalid productionId. Must be a number."

        try:
            performance.totalSeats = int(performance.totalSeats)
        except ValueError:
            return "Invalid totalSeats. Must be a number."

        if performance.totalSeats <= 0:
            return "Total seats must be greater than 0."

        if self.productionRepo.locateProdId(performance.productionId) is None:
            return "Production does not exist."

        try:
            performance.date = self.convertDate(performance.date)
        except ValueError:
            return "Invalid date format. Use YYYY-MM-DD."

        try:
            performance.startTime = self.convertTime(performance.startTime)
            performance.endTime = self.convertTime(performance.endTime)
        except ValueError:
            return "Invalid time format. Use HH:MM:SS."

        if performance.startTime >= performance.endTime:
            return "Start time must be earlier than end time."

        existingSchedule = self.performanceRepo.locatePerformanceSchedule(
            performance.productionId,
            performance.date,
            performance.startTime,
            performance.endTime
        )

        if existingSchedule:
            existingPerformanceId = existingSchedule[0]

            if not isUpdate or existingPerformanceId != performance.performanceId:
                return "Performance schedule already exists."

        return True

    # converts date into YYYY-MM-DD format
    def convertDate(self, date):
        return datetime.strptime(str(date), "%Y-%m-%d").date()

    # converts time into HH:MM:SS format
    def convertTime(self, time):
        return datetime.strptime(str(time), "%H:%M:%S").time()