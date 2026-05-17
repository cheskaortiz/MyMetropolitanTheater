from repository.transactionRepo import TransactionRepo
from repository.ticketRepo import TicketRepo
from repository.staff_repo import StaffRepo
from datetime import datetime


class TransactionService:
    def __init__(self, conn):
        self.transactionRepo = TransactionRepo(conn)
        self.ticketRepo = TicketRepo(conn)
        self.staff_repo = StaffRepo(conn)

    # Needed attributes: transaction object with ticketId, staffId, transactionDate, type, and amount.
    def createTransaction(self, transaction):
        validation = self.__checkTransaction(transaction)

        if validation is True:
            self.transactionRepo.createTransaction(transaction)
            return "Successfully created transaction."

        return validation

    # Needed attributes: none; displays all transactions using basic transaction details.
    def viewAllTransactions(self):
        transactions = self.transactionRepo.getAllTransactions()

        if not transactions:
            return "No transaction available."

        transaction_list = []

        for transaction in transactions:
            transaction_list.append(self.__formatBasicTransaction(transaction))

        return transaction_list

    # Needed attributes: none; displays full transaction report with ticket, staff, customer, production, performance, and seat details.
    def viewTransactionReport(self):
        transactions = self.transactionRepo.getTransactionReport()

        if not transactions:
            return "No transaction report available."

        transaction_reports = []

        for transaction in transactions:
            transaction_reports.append(self.__formatTransactionReport(transaction))

        return transaction_reports

    def viewHighestEarners(self):
        staffs = self.transactionRepo.getEarningsByStaff()

        if not staffs:
            return "No sales earnings available."

        highest_earners = []

        for staff in staffs:
            highest_earners.append(self.__formatHighestEarner(staff))

        return highest_earners

    def viewCommissionByStaff(self):
        staffs = self.transactionRepo.getCommissionByStaff()

        if not staffs:
            return "No commission records available."

        commissions = []

        for staff in staffs:
            commissions.append(self.__formatCommission(staff))

        return commissions

    # Needed attribute: transactionId.
    def locateTransactionId(self, transactionId):
        try:
            transactionId = int(transactionId)
        except ValueError:
            return "Invalid transactionId. Must be a number."

        transaction = self.transactionRepo.locateTransactionId(transactionId)

        if transaction:
            return self.__formatBasicTransaction(transaction)

        return "Transaction does not exist."
    
    # Needed attribute: staffid
    def locateTransactionsByStaff(self, staffId):
        try:
            staffId = int(staffId)
        except ValueError:
            return "Invalid staffId. Must be a number."

        staff = self.staff_repo.locate_staff(staffId)

        if not staff:
            return "Staff does not exist."

        transactions = self.transactionRepo.locateTransactionsbyStaff(staffId)

        if not transactions:
            return "No transactions found for this staff."

        transaction_list = []

        for transaction in transactions:
            transaction_list.append(self.__formatTransactionReport(transaction))

        return transaction_list

    # Needed attribute: ticketid
    def locateTransactionsByTicket(self, ticketId):
        try:
            ticketId = int(ticketId)
        except ValueError:
            return "Invalid ticketId. Must be a number."

        ticket = self.ticketRepo.locateTicketId(ticketId)

        if not ticket:
            return "Ticket does not exist."

        transactions = self.transactionRepo.locateTransactionsbyTicketId(ticketId)

        if not transactions:
            return "No transactions found for this ticket."

        transaction_list = []

        for transaction in transactions:
            transaction_list.append(self.__formatTransactionReport(transaction))

        return transaction_list

    # Needed attribute: type; must be purchased, reserved, or refunded. 
    def locateTransactionsByType(self, type):
        if type is None or str(type).strip() == "":
            return "Transaction type is required."

        type = str(type).lower().strip()

        if type not in ["purchased", "reserved", "refunded"]:
            return "Transaction type must be purchased, reserved, or refunded."

        transactions = self.transactionRepo.locateTransactionsbyType(type)

        if not transactions:
            return "No transactions found for this type."

        transaction_list = []

        for transaction in transactions:
            transaction_list.append(self.__formatTransactionReport(transaction))

        return transaction_list

    # Needed attribute: transactionDate in YYYY-MM-DD format.
    def locateTransactionsByDate(self, transactionDate):
        if transactionDate is None or str(transactionDate).strip() == "":
            return "Transaction date is required."

        try:
            datetime.strptime(str(transactionDate), "%Y-%m-%d")
        except ValueError:
            return "Invalid date format. Use YYYY-MM-DD."

        transactions = self.transactionRepo.locateTransactionsbyDate(transactionDate)

        if not transactions:
            return "No transactions found for this date."

        transaction_list = []

        for transaction in transactions:
            transaction_list.append(self.__formatTransactionReport(transaction))

        return transaction_list

# Needed attributes: startDate and endDate in YYYY-MM-DD format.
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

        transactions = self.transactionRepo.locateTransactionsByDateRange(startDate, endDate)

        if not transactions:
            return "No transactions found within this date range."

        transaction_reports = []

        for transaction in transactions:
            transaction_reports.append(self.__formatTransactionReport(transaction))

        return transaction_reports

    def __checkTransaction(self, transaction):
        if transaction is None:
            return "Transaction data is required."

        # Validate ticket ID
        if transaction.ticketId is None:
            return "Ticket ID is required."

        try:
            transaction.ticketId = int(transaction.ticketId)
        except ValueError:
            return "Invalid ticket ID. Must be a number."

        ticket = self.ticketRepo.locateTicketId(transaction.ticketId)

        if not ticket:
            return "Ticket does not exist."

        # Validate staff ID
        if transaction.staffId is None:
            return "Staff ID is required."

        try:
            transaction.staffId = int(transaction.staffId)
        except ValueError:
            return "Invalid staff ID. Must be a number."

        staff = self.staff_repo.locate_staff(transaction.staffId)

        if not staff:
            return "Staff does not exist."

        # Hourly staff should not process transactions.
        if str(staff[2]).lower() != "commissioned":
            return "Only commissioned staff or sales agents can process transactions."

        # Validate transaction date
        if transaction.transactionDate is None or str(transaction.transactionDate).strip() == "":
            return "Transaction date is required."

        try:
            datetime.strptime(str(transaction.transactionDate), "%Y-%m-%d")
        except ValueError:
            return "Invalid transaction date. Use YYYY-MM-DD."

        # Validate transaction type
        if transaction.type is None or str(transaction.type).strip() == "":
            return "Transaction type is required."

        transaction.type = str(transaction.type).lower().strip()

        if transaction.type not in ["purchased", "reserved", "refunded"]:
            return "Transaction type must be purchased, reserved, or refunded."

        # Validate amount
        if transaction.amount is None:
            return "Amount is required."

        try:
            transaction.amount = float(transaction.amount)
        except ValueError:
            return "Invalid amount. Must be a number."

        if transaction.amount <= 0:
            return "Amount must be greater than zero."

        return True
    
# ----------------------------Formats
    
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

    def __format_amount(self, value):
        if value is None:
            return "Php 0.00"
        
        return f"Php {float(value):,.2f}"

    # Used for SELECT * FROM transactions
    def __formatBasicTransaction(self, transaction):
        return {
            "transaction_id": transaction[0],
            "ticket_id": transaction[1],
            "staff_id": transaction[2],
            "transaction_date": self.__format_date(transaction[3]),
            "type": str(transaction[4]).title(),
            "amount": self.__format_amount(transaction[5])
        }

    # Used for getTransactionReport() and locateTransactionsByDateRange()
    def __formatTransactionReport(self, transaction):
        return {
            "transaction_id": transaction[0],
            "transaction_date": self.__format_date(transaction[1]),
            "type": str(transaction[2]).title(),
            "amount": self.__format_amount(transaction[3]),
            "staff_name": transaction[4],
            "customer_name": transaction[5],
            "ticket_number": transaction[6],
            "ticket_status": transaction[7],
            "production_title": transaction[8],
            "performance_date": self.__format_date(transaction[9]),
            "start_time": self.__format_time(transaction[10]),
            "end_time": self.__format_time(transaction[11]),
            "seat_number": transaction[12],
            "seat_view": transaction[13],
            "price": self.__format_amount(transaction[14])
        }

    def __formatHighestEarner(self, staff):
        return {
            "staff_id": staff[0],
            "staff_name": staff[1],
            "total_sales": self.__format_amount(staff[2])
        }

    def __formatCommission(self, staff):
        return {
            "staff_id": staff[0],
            "staff_name": staff[1],
            "total_sales": self.__format_amount(staff[2]),
            "commission": self.__format_amount(staff[3])
        }
    