class PerformanceSeatRepo:
    def __init__ (self, connect):
        self.connect = connect

    # retrieves all performance seats
    # requirement: supports Theater Seat Map and Seat Pricing views
    def getAllPerformanceSeats(self):
        with self.connect.cursor() as cur:
            cur.execute("SELECT * FROM performance_seat")
            rows = cur.fetchall()
            return rows
    
    # call to create performance seat
    # requirement: all seat numbers must be assigned before they can be allocated to a performance
    def createPerformanceSeat(self, newPerformanceSeat):
        with self.connect.cursor() as cur:
            cur.execute(
                "INSERT INTO performance_seat (seat_id, price, is_available, performance_id) VALUES (%s, %s, %s, %s)",
                (
                    newPerformanceSeat.seatId,
                    newPerformanceSeat.price,
                    newPerformanceSeat.isAvailable,
                    newPerformanceSeat.performanceId
                )
            )
        self.connect.commit()
    
    ## updates seat price or availability for a specific performance
    # requirement: Modify the price and arrangement of seats for each performance
    # requirement: visual image of seat plan must be provided (before and after snapshot)

    def updatePerformanceSeat(self, updatedPerformanceSeat):
        with self.connect.cursor() as cur:
            cur.execute(
                """
                UPDATE performance_seat
                SET seat_id = %s, price = %s, is_available = %s, performance_id = %s
                WHERE performance_seat_id = %s
                """,
                (
                    updatedPerformanceSeat.seatId,
                    updatedPerformanceSeat.price,
                    updatedPerformanceSeat.isAvailable,
                    updatedPerformanceSeat.performanceId,
                    updatedPerformanceSeat.performanceSeatId
                )
            )
            self.connect.commit()
    
    # call to delete performance seat
    def deletePerformanceSeat(self, performanceSeatId):
        with self.connect.cursor() as cur:
            cur.execute("DELETE FROM performance_seat WHERE performance_seat_id = %s", (performanceSeatId,))
            self.connect.commit()

    # checks if performance seat exists
    # def findPerformanceSeat(self, performanceSeatId):
    #     with self.connect.cursor() as cur:
    #         cur.execute("SELECT * FROM performance_seat WHERE performance_seat_id = %s", (performanceSeatId,))
    #         row = cur.fetchone()
    #         return PerformanceSeat(*row) if row else None
        
    # retrieves all seats both avail or not for a specific performance
    # requirement: Theater Seat Map — shows full seat layout per performance
    def getAllSeatsByPerformance(self, performanceId):
        with self.connect.cursor() as cur:
            cur.execute(
                """
                SELECT
                    ps.performance_seat_id,
                    ps.performance_id,
                    ps.seat_id,
                    s.seat_number,
                    s.seat_view,
                    ps.price,
                    ps.is_available
                FROM performance_seat ps
                JOIN seat s
                    ON ps.seat_id = s.seat_id
                JOIN performance per
                    ON ps.performance_id = per.performance_id
                WHERE ps.performance_id = %s
                ORDER BY s.seat_number
                """,
                (performanceId,)
            )

            return cur.fetchall()
        
    # retrieves only available seats for a specific performance
    # requirement: Purchase Tickets by Performance — customer can only pick available seats
    def getAvailableSeatsByPerformance(self, performanceId):
        with self.connect.cursor() as cur:
            cur.execute(
                """
                SELECT
                    ps.performance_seat_id,
                    ps.performance_id,
                    ps.seat_id,
                    s.seat_number,
                    s.seat_view,
                    ps.price,
                    ps.is_available
                FROM performance_seat ps
                JOIN seat s
                    ON ps.seat_id = s.seat_id
                WHERE ps.performance_id = %s
                AND ps.is_available = TRUE
                ORDER BY s.seat_number
                """,
                (performanceId,)
            )

            return cur.fetchall()
        
    # retrieves seat pricing details for a specific performance
    # requirement: Seat Pricing — price depends on seat location, date, and time of performance
    def getSeatPricingByPerformance(self, performanceId):
        with self.connect.cursor() as cur:
            cur.execute(
                """
                SELECT 
                    ps.performance_seat_id,
                    ps.performance_id,
                    s.seat_number,
                    s.seat_view,
                    ps.price,
                    ps.is_available
                FROM performance_seat ps
                JOIN seat s
                    ON ps.seat_id = s.seat_id
                WHERE ps.performance_id = %s
                ORDER BY s.seat_number
                """,
                (performanceId,)
            )

            return cur.fetchall()

    # locates a specific performance seat by its ID — used before update operations
    def locatePerformanceSeatId(self, performanceSeatId):
        with self.connect.cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM performance_seat
                WHERE performance_seat_id = %s
                """,
                (performanceSeatId,)
            )

            row = cur.fetchone()

            if row:
                return row
            return None
        
    # locates a performance seat by seat ID and performance ID
    # requirement: database must monitor that no duplicate seats can be assigned to a single performance
    def locatePerformanceSeatBySeatAndPerformance(self, seatId, performanceId):
        with self.connect.cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM performance_seat
                WHERE seat_id = %s
                AND performance_id = %s
                """,
                (seatId, performanceId)
            )

            row = cur.fetchone()

            if row:
                return row
            return None
            
    