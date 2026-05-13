from service.department_service import DepartmentService
from service.staff_service import StaffService
from service.productionService import ProductionService
from service.performanceService import PerformanceService
from service.seatService import SeatService
from service.performanceSeatService import PerformanceSeatService
from service.customerService import CustomerService
from service.ticketService import TicketService
from service.transactionService import TransactionService

class Service:
    def __init__(self, conn):
        self.department = DepartmentService(conn)
        self.staff = StaffService(conn)
        self.production = ProductionService(conn)
        self.performance = PerformanceService(conn)
        self.seat = SeatService(conn)
        self.performanceSeat = PerformanceSeatService(conn)
        self.customer = CustomerService(conn)
        self.ticket = TicketService(conn)
        self.transaction = TransactionService(conn)
