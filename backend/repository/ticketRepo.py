class TicketRepo:
    def __init__ (self, connect):
        self.connect = connect

    # retrieves all tickets
    # requirement: Transaction Report — shows all ticket purchases, refunds, reservations
    def getAllTickets(self):
        with self.connect.cursor() as cur:
            cur.execute("SELECT * FROM Ticket")
            rows = cur.fetchall()
            return rows
        
    # creates a new ticket record for a purchased or reserved seat
    # requirement: Purchase Tickets by Performance — only sales agents can make transactions
    def createTicket(self, newTicket):
        with self.connect.cursor() as cur:
            cur.execute(
                "INSERT INTO ticket (performance_seat_id, customer_id, status, ticket_number, sale_date) VALUES (%s, %s, %s, %s, %s)",
                (
                    newTicket.performanceSeatId,
                    newTicket.customerId,
                    newTicket.status,
                    newTicket.ticketNumber,
                    newTicket.saleDate
                )
            )
        self.connect.commit()
    
    # call to update ticket
    # def updateTicket(self, updatedTicket):
    #     with self.connect.cursor() as cur:
    #         cur.execute(
    #             """
    #             UPDATE ticket
    #             SET performance_seat_id = %s, customer_id = %s, status = %s, ticket_number = %s, sale_date = %s
    #             WHERE ticket_id = %s
    #             """,
    #             (
    #                 updatedTicket.performanceSeatId,
    #                 updatedTicket.customerId,
    #                 updatedTicket.status,
    #                 updatedTicket.ticketNumber,
    #                 updatedTicket.saleDate,
    #                 updatedTicket.ticketId
    #             )
    #         )
    #         self.connect.commit()

                    # #call to delete ticket
                    # def deleteTicket(self, ticketId):
                    #     with self.connect.cursor() as cur:
                    #         cur.execute("DELETE FROM ticket WHERE ticket_id = %s", (ticketId,))
                    #         self.connect.commit()

                    # # check if ticket exists
                    # def findTicket(self, ticketId):
                    #     with self.connect.cursor() as cur:
                    #         cur.execute("SELECT * FROM ticket WHERE ticket_id = %s", (ticketId,))
                    #         row = cur.fetchone()
                    #         return Ticket(*row) if row else None
        
    # retrieves full ticket details including customer, production, performance, seat, and price
    # requirement: Produce ticket for the customer generating the coded ticket number
    # output: ticket_id, ticket_number, status, sale_date, customer name, production title,
    #         performance date/time, seat number, seat view, price

    def getTicketDetails(self, performanceSeatId, customerId):
        with self.connect.cursor() as cur:
            cur.execute(
                """
                SELECT 
                    t.ticket_id,
                    t.ticket_number,
                    t.status,
                    t.sale_date,
                    c.name,
                    prod.title,
                    per.date,
                    per.start_time,
                    per.end_time,
                    s.seat_number,
                    s.seat_view,
                    ps.price
                FROM ticket t
                JOIN customer c
                    ON t.customer_id = c.customer_id
                JOIN performance_seat ps
                    ON t.performance_seat_id = ps.performance_seat_id
                JOIN seat s
                    ON ps.seat_id = s.seat_id
                JOIN performance per
                    ON ps.performance_id = per.performance_id
                JOIN production prod
                    ON per.production_id = prod.production_id
                WHERE t.performance_seat_id = %s
                AND t.customer_id = %s
                """,
                (performanceSeatId, customerId)
            )

            return cur.fetchall()
    
    # updates only the ticket status — sold, reserved, or refunded
    # requirement: Management tracks refunds and reservations
    # tickets should not be deleted, only their status changes
    def updateTicketStatus(self, ticketId, status):
        with self.connect.cursor() as cur:
            cur.execute(
                "UPDATE ticket SET status = %s WHERE ticket_id = %s",
                (status, ticketId)
            )
        self.connect.commit()

    # locates a ticket by its system-generated ID — used before status updates
    def locateTicketId(self, ticketId):
        with self.connect.cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM ticket
                WHERE ticket_id = %s
                """,
                (ticketId,)
            )

            row = cur.fetchone()

            if row:
                return row
            return None
        
    # locates a ticket by its generated ticket number
    # requirement: coded ticket number output must be verifiable
    def locateTicketNumber(self, ticketNumber):
        with self.connect.cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM ticket
                WHERE ticket_number = %s
                """,
                (ticketNumber,)
            )

            row = cur.fetchone()

            if row:
                return row
            return None
        
    # locates a ticket by performance seat ID — checks if a seat already has a ticket
    # requirement: no duplicate seats can be assigned to a single performance
    def locateTicketByPerformanceSeatId(self, performanceSeatId):
        with self.connect.cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM ticket
                WHERE performance_seat_id = %s
                """,
                (performanceSeatId,)
            )

            row = cur.fetchone()

            if row:
                return row
            return None
        
    # locates all tickets belonging to one customer
    # requirement: Purchase Tickets by Performance — view customer ticket history
    def locateTicketsByCustomerId(self, customerId):
        with self.connect.cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM ticket
                WHERE customer_id = %s
                """,
                (customerId,)
            )

            row = cur.fetchall()

            if row:
                return row
            return None
    
    # locates all tickets by status (sold, reserved, refunded)
    # requirement: Transaction Report — tracks all transaction types
    def locateTicketsByStatus(self, status):
        with self.connect.cursor() as cur:
            cur.execute(
                "SELECT * FROM ticket WHERE status = %s",
                (status,)
            )
            return cur.fetchall()
    
    # locates all tickets under one production
    # requirement: List the productions that have less than 50% of their total seats sold
    def locateTicketsByProductionId(self, productionId):
        with self.connect.cursor() as cur:
            cur.execute(
                """
                SELECT t.*
                FROM ticket t
                JOIN performance_seat ps
                    ON t.performance_seat_id = ps.performance_seat_id
                JOIN performance per
                    ON ps.performance_id = per.performance_id
                WHERE per.production_id = %s
                """,
                (productionId,)
            )
            return cur.fetchall()
    
    # locates all tickets by sale date
    # requirement: Transaction Report — filter transactions by date
    def locateTicketsBySaleDate(self, saleDate):
        with self.connect.cursor() as cur:
            cur.execute(
                "SELECT * FROM ticket WHERE sale_date = %s",
                (saleDate,)
            )
            return cur.fetchall()
        

    # Produce ticket for the customer generating the coded ticket number with output mask of
    # EXAMPLE:
    # Ticket # 5lily071807
    # Tidle: "The Last Lily"
    # When: Say 18, 2007 
    # <production num> + 
    # <last 3 letters of performance title>+
    # <mmddhh of performance> 
    # followed by production number, performance title, and other pertinent details    
    def getTicketDataForTicketNumber(self, performanceSeatId):
        with self.connect.cursor() as cur:
            cur.execute(
                """
                SELECT
                    prod.production_id,
                    prod.title,
                    per.date,
                    per.start_time,
                    per.end_time
                FROM performance_seat ps
                JOIN performance per
                    ON ps.performance_id = per.performance_id
                JOIN production prod
                    ON per.production_id = prod.production_id
                WHERE ps.performance_seat_id = %s
                """,
                (performanceSeatId,)
            )
            return cur.fetchone()

