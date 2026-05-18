from repository.productionRepo import ProductionRepo
from repository.performanceRepo import PerformanceRepo
from datetime import datetime


class ProductionService:
    def __init__(self, conn):
        self.productionRepo = ProductionRepo(conn)
        self.performanceRepo = PerformanceRepo(conn)

    # needed attributes:
    # title, startDate, endDate
    def createProduction(self, production):
        validation = self.__checkProduction(production)

        if validation is True:
            self.productionRepo.createProduction(production)
            return "Successfully created production."

        return validation

    # needed attributes:
    # productionId, title, startDate, endDate
    def updateProduction(self, production):
        if production is None:
            return "Production data is required."

        if production.productionId is None or str(production.productionId).strip() == "":
            return "Production ID is required."

        try:
            production.productionId = int(production.productionId)
        except (ValueError, TypeError):
            return "Invalid production ID. Must be a number."

        if self.productionRepo.locateProdId(production.productionId) is None:
            return "Production does not exist."

        validation = self.__checkProduction(production, isUpdate=True)

        if validation is True:
            self.productionRepo.updateProduction(production)

            updated_production = self.productionRepo.locateProdTitle(production.title)

            return {
                "message": "Successfully updated production.",
                "production": self.__format_production_full(updated_production)
            }

        return validation

    # Delete is not always needed based on the requirements.
    # Only allow delete if production has no performances yet.
    def deleteProduction(self, productionId):
        if productionId is None or str(productionId).strip() == "":
            return "Production ID is required."

        try:
            productionId = int(productionId)
        except (ValueError, TypeError):
            return "Invalid production ID. Must be a number."

        if self.productionRepo.locateProdId(productionId) is None:
            return "Production does not exist."

        if self.performanceRepo.locatePerformanceByProductionId(productionId):
            return "Cannot delete production because it already has performances."

        self.productionRepo.deleteProduction(productionId)

        return "Production deleted."

    def viewAllProductions(self):
        productions = self.productionRepo.getAllProductions()

        if productions is None:
            return "No productions available."

        return self.__format_production_list(productions)

    def locateProductionId(self, productionId):
        if productionId is None or str(productionId).strip() == "":
            return "Production ID is required."

        try:
            productionId = int(productionId)
        except (ValueError, TypeError):
            return "Invalid production ID. Must be a number."

        production = self.productionRepo.locateProdId(productionId)

        if production:
            return self.__format_production_basic(production)

        return "Production does not exist."

    def locateProductionTitle(self, title):
        if title is None or str(title).strip() == "":
            return "Production title is required."

        title = str(title).strip()

        production = self.productionRepo.locateProdTitle(title)

        if production:
            return self.__format_production_full(production)

        return "Production does not exist."

    # Requirement:
    # Ascending list of months where there will be an opening of a new show
    def viewOpeningMonths(self):
        rows = self.productionRepo.getOpeningMonths()

        if rows is None:
            return "No opening months available."

        opening_months = []

        for row in rows:
            opening_months.append(self.__format_opening_month(row))

        return opening_months

    # Requirement:
    # Number of performances by production
    def viewNumberofPerformancesByProduction(self):
        rows = self.productionRepo.getNumberOfPerformancesByProduction()

        if rows is None:
            return "No performance count available."

        performance_counts = []

        for row in rows:
            performance_counts.append(self.__format_performance_count(row))

        return performance_counts

    # Requirement:
    # Number of seats by production
    def viewNumberofSeatsByProduction(self):
        rows = self.productionRepo.getNumberOfSeatsByProduction()

        if rows is None:
            return "No seat count available."

        seat_counts = []

        for row in rows:
            seat_counts.append(self.__format_seat_count(row))

        return seat_counts

    # Requirement:
    # List productions with less than 50% of their total seats sold
    def viewProductionsLessThan50PercentSold(self):
        rows = self.productionRepo.getProductionsLessThan50PercentSold()

        if rows is None:
            return "No productions available."

        productions = []

        for row in rows:
            productions.append(self.__format_less_than_50_percent_sold(row))

        return productions

    def __checkProduction(self, production, isUpdate=False):
        if production is None:
            return "Production data is required."

        if production.title is None or str(production.title).strip() == "":
            return "Production title is required."

        if production.startDate is None or str(production.startDate).strip() == "":
            return "Start date is required."

        if production.endDate is None or str(production.endDate).strip() == "":
            return "End date is required."

        production.title = str(production.title).strip()

        try:
            startDate = datetime.strptime(str(production.startDate), "%Y-%m-%d").date()
            endDate = datetime.strptime(str(production.endDate), "%Y-%m-%d").date()
        except ValueError:
            return "Invalid date format. Use YYYY-MM-DD."

        if startDate > endDate:
            return "Start date cannot be later than end date."

        existingTitle = self.productionRepo.locateProdTitle(production.title)

        if existingTitle:
            existingProductionId = existingTitle[0]

            if not isUpdate or existingProductionId != production.productionId:
                return "Production title already exists."

        return True
    
# ----------------------------Formats

    def __format_date(self, value):
        if value is None:
            return None

        if hasattr(value, "strftime"):
            return value.strftime("%m/%d/%Y")

        try:
            return datetime.strptime(str(value), "%Y-%m-%d").strftime("%m/%d/%Y")
        except ValueError:
            return str(value)

    def __format_production_full(self, production):
        """
        Used for repo methods that return:
        SELECT * FROM production

        Expected row format:
        production_id, title, start_date, end_date
        """

        if not production:
            return None

        return {
            "production_id": production[0],
            "title": production[1],
            "start_date": self.__format_date(production[2]),
            "end_date": self.__format_date(production[3])
        }

    def __format_production_basic(self, production):
        """
        Used for locateProdId() because repo returns:
        SELECT production_id, title
        """

        if not production:
            return None

        return {
            "production_id": production[0],
            "title": production[1]
        }

    def __format_production_list(self, productions):
        if not productions:
            return []

        production_list = []

        for production in productions:
            production_list.append(self.__format_production_full(production))

        return production_list

    def __format_opening_month(self, row):
        """
        Used for getOpeningMonths()

        Expected row format:
        month_number, month_name
        """

        if not row:
            return None

        return {
            "month_number": int(row[0]) if row[0] is not None else None,
            "month_name": str(row[1]).strip() if row[1] is not None else None
        }

    def __format_performance_count(self, row):
        """
        Used for getNumberOfPerformancesByProduction()

        Expected row format:
        production_id, title, number_of_performances
        """

        if not row:
            return None

        return {
            "production_id": row[0],
            "title": row[1],
            "number_of_performances": row[2]
        }

    def __format_seat_count(self, row):
        """
        Used for getNumberOfSeatsByProduction()

        Expected row format:
        production_id, title, total_seats
        """

        if not row:
            return None

        return {
            "production_id": row[0],
            "title": row[1],
            "total_seats": row[2]
        }

    def __format_less_than_50_percent_sold(self, row):
        """
        Used for getProductionsLessThan50PercentSold()

        Expected row format:
        production_id, title, seats_sold, total_seats, percent_sold
        """

        if not row:
            return None

        return {
            "production_id": row[0],
            "title": row[1],
            "seats_sold": row[2],
            "total_seats": row[3],
            "percent_sold": float(row[4]) if row[4] is not None else 0.0
        }