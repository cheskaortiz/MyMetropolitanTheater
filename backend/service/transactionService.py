from repository.transactionRepo import TransactionRepo
from repository.ticketRepo import TicketRepo
from repository.staff_repo import StaffRepo
from datetime import datetime


class TransactionService:
    def __init__(self, conn):
        self.transactionRepo = TransactionRepo(conn)
        self.ticketRepo = TicketRepo(conn)
        self.staff_repo = StaffRepo(conn)

    # creates a transaction after full validation
    # requirement: only commissioned staff/sales agents can process transactions
    # requirement: ticket must exist before a transaction can be created
    def createTransaction(self, transaction):
        validation = self.__checkTransaction(transaction)

        if validation is True:
            self.transactionRepo.createTransaction(transaction)
            return "Successfully created transaction."

        return validation

    # retrieves all transactions for reporting
    # requirement: Transaction Report
    def viewAllTransactions(self):
        return self.transactionRepo.getAllTransactions()

    # retrieves full transaction report with all joined details
    # requirement: Transaction Report — customer, production, performance, seat, price, staff
    def viewTransactionReport(self):
        return self.transactionRepo.getTransactionReport()

    # retrieves highest earners in the sales department
    # requirement: List of highest earners in the Sales Department
    def viewHighestEarners(self):
        return self.transactionRepo.getEarningsByStaff()

    # calculates and retrieves commission earned per sales agent
    # requirement: sales agents paid 25% of total tickets sold
    # requirement: List of highest earners in the Sales Department
    def viewCommissionByStaff(self):
        return self.transactionRepo.getCommissionByStaff()

    # locates a transaction by ID
    # used before any lookup/update
    def locateTransactionId(self, transactionId):
        try:
            transactionId = int(transactionId)
        except ValueError:
            return "Invalid transactionId. Must be a number."

        transaction = self.transactionRepo.locateTransactionId(transactionId)

        if transaction:
            return transaction

        return "Transaction does not exist."

    # locates all transactions processed by a specific sales agent
    # requirement: Names, salaries, and departments of specific workers
    def locateTransactionsByStaff(self, staffId):
        try:
            staffId = int(staffId)
        except ValueError:
            return "Invalid staffId. Must be a number."

        staff = self.staff_repo.locate_staff(staffId)

        if not staff:
            return "Staff does not exist."

        return self.transactionRepo.locateTransactionsbyStaff(staffId)

    # locates all transactions linked to a specific ticket
    # requirement: Transaction Report — full ticket transaction history
    def locateTransactionsByTicket(self, ticketId):
        try:
            ticketId = int(ticketId)
        except ValueError:
            return "Invalid ticketId. Must be a number."

        ticket = self.ticketRepo.locateTicketId(ticketId)

        if not ticket:
            return "Ticket does not exist."

        return self.transactionRepo.locateTransactionsbyTicketId(ticketId)

    # locates transactions by type: purchased, reserved, refunded
    # requirement: Transaction Report — filter by type
    def locateTransactionsByType(self, type):
        if type is None or str(type).strip() == "":
            return "Transaction type is required."

        type = str(type).lower().strip()

        if type not in ["purchased", "reserved", "refunded"]:
            return "Transaction type must be purchased, reserved, or refunded."

        return self.transactionRepo.locateTransactionsbyType(type)

    # locates transactions by date
    # requirement: Transaction Report — filter by date
    def locateTransactionsByDate(self, transactionDate):
        if transactionDate is None or str(transactionDate).strip() == "":
            return "Transaction date is required."

        try:
            datetime.strptime(str(transactionDate), "%Y-%m-%d")
        except ValueError:
            return "Invalid date format. Use YYYY-MM-DD."

        return self.transactionRepo.locateTransactionsbyDate(transactionDate)

    # locates transactions within a date range
    # requirement: Transaction Report — filter by date range
    def locateTransactionsByDateRange(self, startDate, endDate):
        if startDate is None or endDate is None:
            return "Start date and end date are required."

        try:
            start = datetime.strptime(str(startDate), "%Y-%m-%d").date()
            end = datetime.strptime(str(endDate), "%Y-%m-%d").date()
        except ValueError:
            return "Invalid date format. Use YYYY-MM-DD."

        if start > end:
            return "Start date cannot be later than end date."

        return self.transactionRepo.locateTransactionsByDateRange(startDate, endDate)

    # validates transaction fields before creating
    # checks: ticketId exists, staffId exists and is Commissioned type,
    # type is purchased/reserved/refunded, amount is valid number
    # requirement: only sales agents can make transactions
    def __checkTransaction(self, transaction):
        if not transaction.ticketId:
            return "Ticket ID is required."

        if not transaction.staffId:
            return "Staff ID is required."

        if not transaction.transactionDate:
            return "Transaction date is required."

        if not transaction.type:
            return "Transaction type is required."

        if transaction.amount is None or str(transaction.amount).strip() == "":
            return "Amount is required."

        try:
            transaction.ticketId = int(transaction.ticketId)
        except ValueError:
            return "Ticket ID must be a number."

        try:
            transaction.staffId = int(transaction.staffId)
        except ValueError:
            return "Staff ID must be a number."

        try:
            transaction.amount = float(transaction.amount)
        except ValueError:
            return "Amount must be a number."

        try:
            datetime.strptime(str(transaction.transactionDate), "%Y-%m-%d")
        except ValueError:
            return "Invalid transaction date format. Use YYYY-MM-DD."

        transaction.type = transaction.type.lower().strip()

        if transaction.type not in ["purchased", "reserved", "refunded"]:
            return "Transaction type must be purchased, reserved, or refunded."

        ticket = self.ticketRepo.locateTicketId(transaction.ticketId)

        if not ticket:
            return "Ticket does not exist."

        staff = self.staff_repo.locate_staff(transaction.staffId)

        if not staff:
            return "Staff does not exist."

        staffType = staff[1]

        if staffType != "Commissioned":
            return "Only commissioned staff or sales agents can process transactions."

        if transaction.type in ["purchased", "reserved"] and transaction.amount <= 0:
            return "Purchased or reserved transaction amount must be greater than 0."

        if transaction.type == "refunded" and transaction.amount >= 0:
            return "Refunded transaction amount should be negative."

        return True