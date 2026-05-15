from objects.seat import Seat

class SeatRepo:
    def __init__(self, connect):
        self.connect = connect

    # retrieves all seats
    # Retrieves all seats from the fixed seating list.
    # Requirement purpose: Used to display the available theater seats
    def getAllSeat(self):
        with self.connect.cursor() as cur:
            cur.execute("SELECT * FROM seat")
            rows = cur.fetchall()
            return rows

    # cant create because seat is already fixed -30 seat as per the requireents


    # call to update seat
    # Note: Seats are fixed, so only seat details such as seat number and seat view should be updated when needed.
    def updateSeat(self, updatedSeat):
        with self.connect.cursor() as cur:
            cur.execute(
                """
                UPDATE seat
                SET seat_view = %s, seat_number = %s
                WHERE seat_id = %s
                """,
                (
                    updatedSeat.seatView,
                    updatedSeat.seatNumber,
                    updatedSeat.seatId
                )
            )
            self.connect.commit()
        
    # Locates a seat using seat_id.
    # Requirement purpose: Used when validating seat records before updating or when linking a seat to Performance_Seat.
    def locateSeatId(self, seatId):
        with self.connect.cursor() as cur:
            cur.execute(
                """
                SELECT * from seat
                WHERE seat_id = %s
                """,
                (seatId,)
            )

            row = cur.fetchone()

            if row:
                return row
            return None
        
    # locates seat view (yung image ng seat)
    def locateSeatView(self, seatView):
        with self.connect.cursor() as cur:
            cur.execute(
                """
                SELECT * from seat
                WHERE seat_view = %s
                """,
                (seatView,)
            )

            row = cur.fetchone()

            if row:
                return row
            return None
        
    # Locates a seat using its seat number, such as A1, A2, B1, etc.
    # Requirement purpose: Used to search a specific physical seat and to prevent duplicate seat numbers.
    def locateSeatNumber(self, seatNumber):
        with self.connect.cursor() as cur:
            cur.execute(
                """
                SELECT * from seat
                WHERE seat_number = %s
                """,
                (seatNumber,)
            )

            row = cur.fetchone()

            if row:
                return row
            return None