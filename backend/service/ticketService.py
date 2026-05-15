from repository.ticketRepo import TicketRepo
from objects.ticket import Ticket

class TicketService:
    def __init__(self, conn):
        self.ticketRepo = TicketRepo(conn)

    # Used for creating a ticket record. for ticket purchasing/reservation.
    # requirement: ticket must have valid performance seat, customer, status, date, and ticket number
    def createTicket(self, ticket):
        validation = self.__checkTicket(ticket)

        if validation is True:
            self.ticketRepo.createTicket(ticket)
            return "Successfully created ticket"
        
        return validation

    # Uretrieves all all ticket records
    def viewAllTickets(self):
        return self.ticketRepo.getAllTickets()

    # the requirement that the system should generate a ticket code, ticket number
    # requirement: <production_num><last 3 letters of title><mmddhh of performance>
    # example: 1cal011519 = production 1, "The Notebook: The Musical", Jan 15 at 19:00
    def generateTicketNumber(self, performanceSeatId):
        row = self.ticketRepo.getTicketDataForTicketNumber(performanceSeatId)
        if not row:
            return None

        productionId = row[0]
        title = row[1]
        date = row[2]
        startTime = row[3]
        #endTIme not included unless necessary
        
        last3 = title[-3:].lower()
        mmddhh = date.strftime("%m%d") + startTime.strftime("%H")

        return f"{productionId}{last3}{mmddhh}"

    #  creates a ticket for a selected performance seat and customer.
    # requirement: Purchase Tickets by Performance — only sales agents can process
    # automatically generates ticket number before saving
    def purchaseTicket(self, performanceSeatId, customerId, status, saleDate): 
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
            return ticketNumber

        return validation

    # Used for changing the status of a ticket (sold, refunded, reserved)
    # requirement: Management tracks refunds and reservations
    # tickets are never deleted, only their status changes
    def updateTicketStatus(self, ticketId, newStatus):
        findTicket = self.ticketRepo.locateTicketId(ticketId)

        if not findTicket:
            return False

        self.ticketRepo.updateTicketStatus(ticketId, newStatus)
        return True

    # Used for viewing complete ticket information.
    # requirement that ticket details should show customer, production, performance date/time, seat number, seat view, price, and ticket status.
    def viewTicketDetails(self, performanceSeatId, customerId):
        return self.ticketRepo.getTicketDetails(performanceSeatId, customerId)

    # to search a ticket by ticket ID. used before updating or viewing one specific ticket.
    def locateTicketId(self, ticketId):
        try:
            ticketId = int(ticketId)
        except ValueError:
            return "Invalid ticketId. Must be a number."

        ticket = self.ticketRepo.locateTicketId(ticketId)

        if ticket:
            return ticket

        return "Ticket does not exist."

    # to search a ticket by its generated ticket number. helps verify if a ticket code exists.
    def locateTicketByNumber(self, ticketNumber):
        return self.ticketRepo.locateTicketNumber(ticketNumber)

    # to view all tickets of one customer.
    def locateTicketsByCustomer(self, customerId):
        return self.ticketRepo.locateTicketsByCustomerId(customerId)

    # to locate all the tickets by status (sold, reserve, refund)
    def locateTicketsByStatus(self, status):
        return self.ticketRepo.locateTicketsByStatus(status)

    # Used for viewing tickets under one production.
    def locateTicketsByProduction(self, productionId):
        return self.ticketRepo.locateTicketsByProductionId(productionId)
    
    # locates tickets by sale date — supports Transaction Report filtering by date
    def locateTicketsBySaleDate(self, saleDate):
        return self.ticketRepo.locateTicketsBySaleDate(saleDate)

    # for checking if completedetails before creating new ticker
    def __checkTicket(self, ticket):
        if not ticket.performanceSeatId:
            return "Performance seat ID is required."

        if not ticket.customerId:
            return "Customer ID is required."

        try:
            ticket.performanceSeatId = int(ticket.performanceSeatId)
        except ValueError:
            return "Performance seat ID must be a number."

        try:
            ticket.customerId = int(ticket.customerId)
        except ValueError:
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

        return True