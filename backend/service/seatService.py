from repository.seatRepo import SeatRepo


class SeatService:
    def __init__(self, conn):
        self.seatRepo = SeatRepo(conn)

    


    def viewAllSeats(self):
        seats = self.seatRepo.getAllSeat()

        if seats is None:
            return "No seats available."

        return self.__format_seat_list(seats)

    # Optional alias for requirement: Theater Seat Map
    def viewSeatMap(self):
        seats = self.seatRepo.getAllSeat()

        if seats is None:
            return "No seats available."

        return self.__format_seat_list(seats)


    def locateSeatId(self, seatId):
        if seatId is None or str(seatId).strip() == "":
            return "Seat ID is required."

        try:
            seatId = int(seatId)
        except (ValueError, TypeError):
            return "Invalid seat ID. Must be a number."

        seat = self.seatRepo.locateSeatId(seatId)

        if seat:
            return self.__format_seat(seat)

        return "Seat does not exist."

    def locateSeatNumber(self, seatNumber):
        if seatNumber is None or str(seatNumber).strip() == "":
            return "Seat number is required."

        seatNumber = str(seatNumber).strip()

        seat = self.seatRepo.locateSeatNumber(seatNumber)

        if seat:
            return self.__format_seat(seat)

        return "Seat does not exist."

    def locateSeatView(self, seatView):
        if seatView is None or str(seatView).strip() == "":
            return "Seat view is required."

        seatView = str(seatView).strip()

        seat = self.seatRepo.locateSeatView(seatView)

        if seat:
            return self.__format_seat(seat)

        return "Seat does not exist."


    def updateSeat(self, seat):
        validation = self.__checkSeat(seat, isUpdate=True)

        if validation is True:
            self.seatRepo.updateSeat(seat)

            return {
                "message": "Successfully updated seat.",
                "seat": self.__format_seat(
                    self.seatRepo.locateSeatId(seat.seatId)
                )
            }

        return validation

    def __checkSeat(self, seat, isUpdate=False):
        if seat is None:
            return "Seat data is required."

        if seat.seatId is None or str(seat.seatId).strip() == "":
            return "Seat ID is required."

        try:
            seat.seatId = int(seat.seatId)
        except (ValueError, TypeError):
            return "Invalid seat ID. Must be a number."

        existingSeat = self.seatRepo.locateSeatId(seat.seatId)

        if existingSeat is None:
            return "Seat does not exist."

        if seat.seatNumber is None or str(seat.seatNumber).strip() == "":
            return "Seat number is required."

        if seat.seatView is None or str(seat.seatView).strip() == "":
            return "Seat view is required."

        seat.seatNumber = str(seat.seatNumber).strip()
        seat.seatView = str(seat.seatView).strip()

        existingSeatNumber = self.seatRepo.locateSeatNumber(seat.seatNumber)

        if existingSeatNumber:
            existingSeatId = existingSeatNumber[0]

            if not isUpdate or existingSeatId != seat.seatId:
                return "Seat number already exists."

        return True
    
# ----------------------------Formats

    def __format_seat(self, seat):
        """
        Used for repo methods that return SELECT * FROM seat.

        Expected row format:
        seat_id, seat_view, seat_number
        """

        if not seat:
            return None

        return {
            "seat_id": seat[0],
            "seat_view": seat[1],
            "seat_number": seat[2]
        }

    def __format_seat_list(self, seats):
        if not seats:
            return []

        seat_list = []

        for seat in seats:
            seat_list.append(self.__format_seat(seat))

        return seat_list