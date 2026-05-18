from datetime import datetime, date

from repository.ticketRepo import TicketRepo
from objects.ticket import Ticket


class TicketService:
    def __init__(self, conn):
        self.ticketRepo = TicketRepo(conn)

    #  call to creat ticket
    #  needed attribute are performance seat id, customer id, status, ticket num, 
    def createTicket(self, ticket):
        if ticket is None:
            return "Ticket data is required."

        # Generate ticket number if missing
        if not ticket.ticketNumber:
            ticket.ticketNumber = self.generateTicketNumber(ticket.performanceSeatId)

            if not ticket.ticketNumber:
                return "Cannot generate ticket number. Invalid performance seat."

        validation = self.__checkTicket(ticket)

        if validation is True:
            self.ticketRepo.createTicket(ticket)

            return {
                "message": "Successfully created ticket.",
                "ticket_number": ticket.ticketNumber
            }

        return validation

    #  call to generate ticketNumber
    def generateTicketNumber(self, performanceSeatId):
        try:
            performanceSeatId = int(performanceSeatId)
        except (ValueError, TypeError):
            return None

        row = self.ticketRepo.getTicketDataForTicketNumber(performanceSeatId)

        if not row:
            return None

        productionId = row[0]
        title = row[1]
        performanceDate = row[2]
        startTime = row[3]

        last3 = title[-3:].lower()
        mmddhh = performanceDate.strftime("%m%d") + startTime.strftime("%H")

        return f"{productionId}{last3}{mmddhh}"

    def purchaseTicket(self, performanceSeatId, customerId, status, saleDate, ticketNumber):
        ticketNumber = self.generateTicketNumber(performanceSeatId)

        if not ticketNumber:
            return "Cannot generate ticket number. Invalid performance seat."

        newTicket = Ticket(
            performanceSeatId=performanceSeatId,
            customerId=customerId,
            status=status,
            ticketNumber=ticketNumber,
            saleDate=saleDate
        )

        validation = self.__checkTicket(newTicket)

        if validation is True:
            self.ticketRepo.createTicket(newTicket)

            return {
                "message": "Successfully purchased/reserved ticket.",
                "ticket_number": ticketNumber
            }

        return validation

    def viewAllTickets(self):
        tickets = self.ticketRepo.getAllTickets()
        return self.__format_basic_ticket_list(tickets)

    # Needed attributes: performance seat id and customer id
    def viewTicketDetails(self, performanceSeatId, customerId):
        try:
            performanceSeatId = int(performanceSeatId)
            customerId = int(customerId)
        except (ValueError, TypeError):
            return "Performance seat ID and customer ID must be numbers."

        details = self.ticketRepo.getTicketDetails(performanceSeatId, customerId)
        return self.__format_ticket_details_list(details)

    def locateTicketId(self, ticketId):
        try:
            ticketId = int(ticketId)
        except (ValueError, TypeError):
            return "Invalid ticket ID. Must be a number."

        ticket = self.ticketRepo.locateTicketId(ticketId)

        if ticket:
            return self.__format_basic_ticket(ticket)

        return "Ticket does not exist."

    def locateTicketByNumber(self, ticketNumber):
        if not ticketNumber:
            return "Ticket number is required."

        ticket = self.ticketRepo.locateTicketNumber(ticketNumber)

        if ticket:
            return self.__format_basic_ticket(ticket)

        return "Ticket does not exist."

    def locateTicketByPerformanceSeatId(self, performanceSeatId):
        try:
            performanceSeatId = int(performanceSeatId)
        except (ValueError, TypeError):
            return "Invalid performance seat ID. Must be a number."

        ticket = self.ticketRepo.locateTicketByPerformanceSeatId(performanceSeatId)

        if ticket:
            return self.__format_basic_ticket(ticket)

        return "Ticket does not exist."

    def locateTicketsByCustomer(self, customerId):
        try:
            customerId = int(customerId)
        except (ValueError, TypeError):
            return "Invalid customer ID. Must be a number."

        tickets = self.ticketRepo.locateTicketsByCustomerId(customerId)
        return self.__format_basic_ticket_list(tickets)

    def locateTicketsByStatus(self, status):
        if not status:
            return "Status is required."

        status = status.lower().strip()

        if status not in ["sold", "refunded", "reserved"]:
            return "Status must be sold, refunded, or reserved."

        tickets = self.ticketRepo.locateTicketsByStatus(status)
        return self.__format_basic_ticket_list(tickets)

    def locateTicketsByProduction(self, productionId):
        try:
            productionId = int(productionId)
        except (ValueError, TypeError):
            return "Invalid production ID. Must be a number."

        tickets = self.ticketRepo.locateTicketsByProductionId(productionId)
        return self.__format_basic_ticket_list(tickets)

    def locateTicketsBySaleDate(self, saleDate):
        if not saleDate:
            return "Sale date is required."

        tickets = self.ticketRepo.locateTicketsBySaleDate(saleDate)
        return self.__format_basic_ticket_list(tickets)

    def updateTicketStatus(self, ticketId, newStatus):
        try:
            ticketId = int(ticketId)
        except (ValueError, TypeError):
            return "Invalid ticket ID. Must be a number."

        if not newStatus:
            return "Status is required."

        newStatus = newStatus.lower().strip()

        if newStatus not in ["sold", "refunded", "reserved"]:
            return "Status must be sold, refunded, or reserved."

        findTicket = self.ticketRepo.locateTicketId(ticketId)

        if not findTicket:
            return "Ticket does not exist."

        self.ticketRepo.updateTicketStatus(ticketId, newStatus)

        return "Successfully updated ticket status."

    def __checkTicket(self, ticket):
        if not ticket.performanceSeatId:
            return "Performance seat ID is required."

        if not ticket.customerId:
            return "Customer ID is required."

        try:
            ticket.performanceSeatId = int(ticket.performanceSeatId)
        except (ValueError, TypeError):
            return "Performance seat ID must be a number."

        try:
            ticket.customerId = int(ticket.customerId)
        except (ValueError, TypeError):
            return "Customer ID must be a number."

        if not ticket.saleDate:
            return "Sale date is required."

        if not ticket.ticketNumber:
            return "Ticket number is required."

        if not ticket.status:
            return "Status is required."

        ticket.status = ticket.status.lower().strip()

        if ticket.status not in ["sold", "refunded", "reserved"]:
            return "Status must be sold, refunded, or reserved."

        existingTicket = self.ticketRepo.locateTicketByPerformanceSeatId(ticket.performanceSeatId)

        if existingTicket:
            return "This performance seat already has an existing ticket."

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

    def __format_time(self, value):
        if value is None:
            return None

        if hasattr(value, "strftime"):
            return value.strftime("%I:%M %p").lstrip("0")

        return str(value)

    def __format_basic_ticket(self, ticket):
        """
        Used for repo methods that return SELECT * FROM ticket.

        Expected row format:
        ticket_id, performance_seat_id, customer_id, status, ticket_number, sale_date
        """

        if not ticket:
            return None

        return {
            "ticket_id": ticket[0],
            "performance_seat_id": ticket[1],
            "customer_id": ticket[2],
            "status": ticket[3],
            "ticket_number": ticket[4],
            "sale_date": self.__format_date(ticket[5])
        }

    def __format_basic_ticket_list(self, tickets):
        if not tickets:
            return []

        ticket_list = []

        for ticket in tickets:
            ticket_list.append(self.__format_basic_ticket(ticket))

        return ticket_list

    def __format_ticket_details(self, ticket):
        """
        Used only for getTicketDetails(), because that repo method returns joined data.

        Expected row format:
        ticket_id, ticket_number, status, sale_date, customer_name,
        production_title, performance_date, start_time, end_time,
        seat_number, seat_view, price
        """

        if not ticket:
            return None

        return {
            "ticket_id": ticket[0],
            "ticket_number": ticket[1],
            "status": ticket[2],
            "sale_date": self.__format_date(ticket[3]),
            "customer_name": ticket[4],
            "production_title": ticket[5],
            "performance_date": self.__format_date(ticket[6]),
            "start_time": self.__format_time(ticket[7]),
            "end_time": self.__format_time(ticket[8]),
            "seat_number": ticket[9],
            "seat_view": ticket[10],
            "price": ticket[11]
        }

    def __format_ticket_details_list(self, tickets):
        if not tickets:
            return []

        ticket_details = []

        for ticket in tickets:
            ticket_details.append(self.__format_ticket_details(ticket))

        return ticket_details