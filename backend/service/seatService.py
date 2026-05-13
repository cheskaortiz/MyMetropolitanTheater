from repository.seatRepo import SeatRepo


class SeatService:
    def __init__(self, conn):
        self.seatRepo = SeatRepo(conn)

    #  call to update seat
    def updateSeat(self, seat):
        if seat.seatId is None:
            return "Invalid seatId."

        try:
            seat.seatId = int(seat.seatId)
        except ValueError:
            return "Invalid seatId. Must be a number."

        if self.seatRepo.locateSeatId(seat.seatId) is None:
            return "Seat does not exist."

        validation = self.__checkSeat(seat, isUpdate=True)

        if validation is True:
            self.seatRepo.updateSeat(seat)
            return "Successfully updated seat."

        return validation
    
    # retrieves all seat
    def viewAllSeats(self):
        return self.seatRepo.getAllSeat()

    # 
    def locateSeatId(self, seatId):
        try:
            seatId = int(seatId)
        except ValueError:
            return "Invalid seatId. Must be a number."

        seat = self.seatRepo.locateSeatId(seatId)

        if seat:
            return seat

        return "Seat does not exist."

    def locateSeatNumber(self, seatNumber):
        if seatNumber is None or str(seatNumber).strip() == "":
            return "Seat number is required."

        seatNumber = str(seatNumber).strip()

        seat = self.seatRepo.locateSeatNumber(seatNumber)

        if seat:
            return seat

        return "Seat does not exist."

    def locateSeatView(self, seatView):
        if seatView is None or str(seatView).strip() == "":
            return "Seat view is required."

        seatView = str(seatView).strip()

        seat = self.seatRepo.locateSeatView(seatView)

        if seat:
            return seat

        return "Seat does not exist."

    def __checkSeat(self, seat, isUpdate=False):
        if seat.seatId is None:
            return "Invalid seatId."

        try:
            seat.seatId = int(seat.seatId)
        except ValueError:
            return "Invalid seatId. Must be a number."

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