from repository.performanceRepo import PerformanceRepo
from repository.productionRepo import ProductionRepo
from datetime import datetime


class PerformanceService:
    def __init__(self, conn):
        self.performanceRepo = PerformanceRepo(conn)
        self.productionRepo = ProductionRepo(conn)

    # Needed attributes: productionId, startTime, endTime, date, totalSeats
    def createPerformance(self, performance):
        validation = self.__checkPerformance(performance)

        if validation is True:
            self.performanceRepo.createPerformance(performance)
            return "Successfully created performance."

        return validation

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


    def viewAllPerformances(self):
        performances = self.performanceRepo.getAllPerformance()

        if not performances:
            return "No performances available."

        performance_list = []

        for performance in performances:
            performance_list.append(self.__performance_dictionary(performance))

        return performance_list
    
    def locatePerformanceId(self, performanceId):
        try:
            performanceId = int(performanceId)
        except ValueError:
            return "Invalid performanceId. Must be a number."

        performance = self.performanceRepo.locatePerformanceId(performanceId)

        if performance:
            return self.__performance_dictionary(performance)

        return "Performance does not exist."

    # used in workdlogs, This returns only start_time and end_time because the repo query only selects those two columns.
    def locatePerformanceByPerformanceId(self, performanceId):
        try:
            performanceId = int(performanceId)
        except ValueError:
            return "Invalid performanceId. Must be a number."

        performance = self.performanceRepo.locatePerformanceByPerformanceId(performanceId)

        if performance:
            return self.__performance_time_dictionary(performance)

        return "Performance does not exist."


    def locatePerformanceByProductionId(self, productionId):
        try:
            productionId = int(productionId)
        except ValueError:
            return "Invalid productionId. Must be a number."

        performances = self.performanceRepo.locatePerformanceByProductionId(productionId)

        if not performances:
            return "No performances found for this production."

        performance_list = []

        for performance in performances:
            performance_list.append(self.__performance_dictionary(performance))

        return performance_list
    
    def locatePerformanceByDate(self, date):
        if date is None or str(date).strip() == "":
            return "Performance date is required."

        try:
            date = self.convertDate(date)
        except ValueError:
            return "Invalid date format. Use YYYY-MM-DD."

        performances = self.performanceRepo.locatePerformanceByDate(date)

        if not performances:
            return "No performances found on this date."

        performance_list = []

        for performance in performances:
            performance_list.append(self.__performance_dictionary(performance))

        return performance_list


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
            return self.__performance_dictionary(performance)

        return "Performance schedule does not exist."

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
    
# -----------------------------------Formats
    
    def __format_date(self, value):
        if value is None:
            return None

        if hasattr(value, "strftime"):
            return value.strftime("%m/%d/%Y")

        return str(value)

    def __format_time(self, value):
        if value is None:
            return None

        if hasattr(value, "strftime"):
            return value.strftime("%I:%M %p").lstrip("0")

        return str(value)

    def __performance_dictionary(self, performance):
        return {
            "performance_id": performance[0],
            "production_id": performance[1],
            "start_time": self.__format_time(performance[2]),
            "end_time": self.__format_time(performance[3]),
            "date": self.__format_date(performance[4]),
            "total_seats": performance[5]
        }

    def __performance_time_dictionary(self, performance):
        return {
            "start_time": self.__format_time(performance[0]),
            "end_time": self.__format_time(performance[1])
        }


    def convertDate(self, date):
        return datetime.strptime(str(date), "%Y-%m-%d").date()

    def convertTime(self, time):
        return datetime.strptime(str(time), "%H:%M:%S").time()