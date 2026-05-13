from objects.production import Production

from repository.productionRepo import ProductionRepo
from repository.performanceRepo import PerformanceRepo
from datetime import datetime


class ProductionService:
    def __init__(self, conn):
        self.productionRepo = ProductionRepo(conn)
        self.performanceRepo = PerformanceRepo(conn)

    # needed attributes in creating production:
    # title, startDate, endDate
    def createProduction(self, production):
        validation = self.__checkProduction(production)

        if validation is True:
            self.productionRepo.createProduction(production)
            return "Successfully created production."

        return validation

    # needed attributes in updating production:
    # productionId, title, startDate, endDate
    def updateProduction(self, production):
        if production.productionId is None:
            return "Invalid productionId."

        try:
            production.productionId = int(production.productionId)
        except ValueError:
            return "Invalid productionId. Must be a number."

        if self.productionRepo.locateProdId(production.productionId) is None:
            return "Production does not exist."

        validation = self.__checkProduction(production, isUpdate=True)

        if validation is True:
            self.productionRepo.updateProduction(production)
            return "Successfully updated production."

        return validation

    # Delete is not always needed based on the requirements.
    # If you include delete, only allow it if the production has no performances yet.
    def deleteProduction(self, productionId):
        try:
            productionId = int(productionId)
        except ValueError:
            return "Invalid productionId. Must be a number."

        if self.productionRepo.locateProdId(productionId) is None:
            return "Production does not exist."

        if self.performanceRepo.locatePerformanceByProductionId(productionId):
            return "Cannot delete production because it already has performances."

        self.productionRepo.deleteProduction(productionId)
        return "Production deleted."

    # For viewing all productions
    def viewAllProductions(self):
        return self.productionRepo.getAllProductions()

    # For searching one production
    def locateProductionId(self, productionId):
        try:
            productionId = int(productionId)
        except ValueError:
            return "Invalid productionId. Must be a number."

        production = self.productionRepo.locateProdId(productionId)

        if production:
            return production

        return "Production does not exist."

    def locateProductionTitle(self, title):
        if title is None or title.strip() == "":
            return "Production title is required."

        production = self.productionRepo.locateProdTitle(title.strip())

        if production:
            return production

        return "Production does not exist."

    # Requirement: Ascending list of months where there will be an opening of a new show
    def viewOpeningMonths(self):
        return self.productionRepo.getOpeningMonths()

    # Requirement: Number of performances by production
    def viewNumberofPerformancesByProduction(self):
        return self.productionRepo.getNumberOfPerformancesByProduction()

    # Requirement: Number of seats by production
    def viewNumberofSeatsByProduction(self):
        return self.productionRepo.getNumberOfSeatsByProduction()

    # Requirement: List productions with less than 50% of their total seats sold
    def viewProductionsLessThan50PercentSold(self):
        return self.productionRepo.getProductionsLessThan50PercentSold()

    def __checkProduction(self, production, isUpdate=False):
        if production.title is None or production.title.strip() == "":
            return "Production title is required."

        if production.startDate is None or production.endDate is None:
            return "Start date and end date are required."

        try:
            startDate = datetime.strptime(str(production.startDate), "%Y-%m-%d").date()
            endDate = datetime.strptime(str(production.endDate), "%Y-%m-%d").date()
        except ValueError:
            return "Invalid date format. Use YYYY-MM-DD."

        if startDate > endDate:
            return "Start date cannot be later than end date."

        existingTitle = self.productionRepo.locateProdTitle(production.title.strip())

        if existingTitle:
            # existingTitle[0] is productionId based on your SELECT *
            if not isUpdate or existingTitle[0] != production.productionId:
                return "Production title already exists."

        return True