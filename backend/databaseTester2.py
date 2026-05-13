# from start_database import start_database
# from objects.production import Production


# def testing():
#     db = start_database()

#     if db:
#         result = db.service.production.createProduction(
#             Production(
#                 title="Test Musical",
#                 startDate="2025-06-01",
#                 endDate="2025-07-30"
#             )
#         )
#         print("CREATE:", result)

#         result = db.service.production.viewAllProductions()
#         print("VIEW ALL:", result)

#         result = db.service.production.locateProductionTitle("Test Musical")
#         print("LOCATE TITLE:", result)

#         if isinstance(result, tuple):
#             productionId = result[0]

#             result = db.service.production.updateProduction(
#                 Production(
#                     productionId=productionId,
#                     title="Updated Test Musical",
#                     startDate="2025-06-05",
#                     endDate="2025-08-01"
#                 )
#             )
#             print("UPDATE:", result)

#         print("\nOPENING MONTHS:")
#         for row in db.service.production.viewOpeningMonths():
#             print(row)

#         print("\nPERFORMANCES BY PRODUCTION:")
#         for row in db.service.production.viewNumberofPerformancesByProduction():
#             print(row)

#         print("\nSEATS BY PRODUCTION:")
#         for row in db.service.production.viewNumberofSeatsByProduction():
#             print(row)

#         print("\nLESS THAN 50% SOLD:")
#         for row in db.service.production.viewProductionsLessThan50PercentSold():
#             print(row)

# testing()



# ------------------------------------------------------------------------------------------

# from start_database import start_database
# from objects.performance import Performance


# def testing():
#     db = start_database()

#     if db:
#         print("\n" + "=" * 50)
#         print("PERFORMANCE TESTING")
#         print("=" * 50)

#         # Use an existing production_id.
#         # Example: if you created Updated Test Musical earlier and its ID is 31,
#         # use productionId=31.
#         productionId = 31

#         print("\nCREATE PERFORMANCE:")
#         result = db.service.performance.createPerformance(
#             Performance(
#                 productionId=productionId,
#                 time="19:00:00",
#                 date="2025-06-10",
#                 totalSeats=30
#             )
#         )
#         print(result)

#         print("\nVIEW ALL PERFORMANCES:")
#         result = db.service.performance.viewAllPerformances()
#         for row in result:
#             print(row)

#         print("\nLOCATE PERFORMANCE BY ID:")
#         result = db.service.performance.locatePerformanceId(1)
#         print(result)

#         print("\nUPDATE PERFORMANCE:")
#         result = db.service.performance.updatePerformance(
#             Performance(
#                 performanceId=1,
#                 productionId=productionId,
#                 time="20:00:00",
#                 date="2025-06-11",
#                 totalSeats=30
#             )
#         )
#         print(result)

#         print("\nCURRENT PERFORMANCES:")
#         result = db.service.performance.viewCurrentPerformances()
#         for row in result:
#             print(row)

#         print("\nAVAILABLE SEATS EACH PERFORMANCE:")
#         result = db.service.performance.viewAvailableSeatsEachPerformance()
#         for row in result:
#             print(row)

#         print("\nPERFORMANCES BY PRODUCTION:")
#         result = db.service.performance.viewPerformancesByProduction()
#         for row in result:
#             print(row)

#         print("\nPERFORMANCE DETAILS:")
#         result = db.service.performance.viewPerformanceDetails(1)
#         print(result)

#         print("\nTEST INVALID TOTAL SEATS:")
#         result = db.service.performance.createPerformance(
#             Performance(
#                 productionId=productionId,
#                 time="18:00:00",
#                 date="2025-06-12",
#                 totalSeats=40
#             )
#         )
#         print(result)

#         print("\nTEST INVALID PRODUCTION ID:")
#         result = db.service.performance.createPerformance(
#             Performance(
#                 productionId=9999,
#                 time="18:00:00",
#                 date="2025-06-12",
#                 totalSeats=30
#             )
#         )
#         print(result)

#         print("\nTEST DATE OUTSIDE PRODUCTION DATE RANGE:")
#         result = db.service.performance.createPerformance(
#             Performance(
#                 productionId=productionId,
#                 time="18:00:00",
#                 date="2030-01-01",
#                 totalSeats=30
#             )
#         )
#         print(result)


# testing()

# -------------------------------------------------------------------------------------------------------------------------------

# from start_database import start_database
# from objects.seat import Seat


# def testing():
#     db = start_database()

#     if db:
#         print("\n" + "=" * 50)
#         print("SEAT TESTING")
#         print("=" * 50)

#         print("\nVIEW ALL SEATS:")
#         result = db.service.seat.viewAllSeats()
#         for seat in result:
#             print(seat)

#         print("\nLOCATE SEAT BY ID:")
#         result = db.service.seat.locateSeatId(1)
#         print(result)

#         print("\nLOCATE SEAT BY SEAT NUMBER:")
#         result = db.service.seat.locateSeatNumber("A1")
#         print(result)

#         print("\nUPDATE SEAT:")
#         result = db.service.seat.updateSeat(
#             Seat(
#                 seatId=1,
#                 seatView="OLALLALLALA",
#                 seatNumber="A1"
#             )
#         )
#         print(result)

#         print("\nTEST INVALID SEAT ID:")
#         result = db.service.seat.locateSeatId("abc")
#         print(result)

#         print("\nTEST NON-EXISTING SEAT:")
#         result = db.service.seat.locateSeatId(999)
#         print(result)


# testing()


# ----------------------------------------------------------------------------------------
# from start_database import start_database
# from objects.customer import Customer


# def testing():
#     db = start_database()

#     if db:
#         print("\n" + "=" * 50)
#         print("CUSTOMER TESTING")
#         print("=" * 50)

#         print("\nVIEW ALL CUSTOMERS:")
#         result = db.service.customer.viewAllCustomer()
#         for customer in result:
#             print(customer)

#         print("\nLOCATE CUSTOMER BY ID:")
#         result = db.service.customer.locateCustomerId(1)
#         print(result)

#         print("\nLOCATE CUSTOMER BY NAME:")
#         result = db.service.customer.locateCustomerName("Customer 1")
#         print(result)

#         print("\nLOCATE CUSTOMER BY EMAIL:")
#         result = db.service.customer.locateCustomerEmail("customer1@gmail.com")
#         print(result)

#         print("\nLOCATE CUSTOMER BY MOBILE NUMBER:")
#         result = db.service.customer.locateCustomerMobileNumber("09123456789")
#         print(result)

#         print("\nCREATE CUSTOMER:")
#         result = db.service.customer.createCustomer(
#             Customer(
#                 name="Test Customer",
#                 email="testcustomer@gmail.com",
#                 mobileNumber="09999999999"
#             )
#         )
#         print(result)

#         print("\nUPDATE CUSTOMER:")
#         result = db.service.customer.updateCustomer(
#             Customer(
#                 customerId=1,
#                 name="Updated Customer",
#                 email="updatedcustomer@gmail.com",
#                 mobileNumber="09888888888"
#             )
#         )
#         print(result)

#         print("\nTEST INVALID CUSTOMER ID:")
#         result = db.service.customer.locateCustomerId("abc")
#         print(result)

#         print("\nTEST NON-EXISTING CUSTOMER:")
#         result = db.service.customer.locateCustomerId(999)
#         print(result)

#     else:
#         print("Database connection failed.")


# testing()


# ----------------------------------------------------------------------------------------
# from start_database import start_database
# from objects.seat import Seat


# def testing():
#     db = start_database()

#     if db:
#         print("\n" + "=" * 50)
#         print("SEAT TESTING")
#         print("=" * 50)

#         print("\nVIEW ALL SEATS:")
#         result = db.service.seat.viewAllSeats()
#         for seat in result:
#             print(seat)

#         print("\nLOCATE SEAT BY ID:")
#         result = db.service.seat.locateSeatId(1)
#         print(result)

#         print("\nLOCATE SEAT BY SEAT NUMBER:")
#         result = db.service.seat.locateSeatNumber("A1")
#         print(result)

#         print("\nLOCATE SEAT BY SEAT VIEW:")
#         result = db.service.seat.locateSeatView("Orchestra")
#         print(result)

#         print("\nUPDATE SEAT:")
#         result = db.service.seat.updateSeat(
#             Seat(
#                 seatId=1,
#                 seatView="Orchestra",
#                 seatNumber="A1"
#             )
#         )
#         print(result)

#         print("\nTEST INVALID SEAT ID:")
#         result = db.service.seat.locateSeatId("abc")
#         print(result)

#         print("\nTEST NON-EXISTING SEAT:")
#         result = db.service.seat.locateSeatId(999)
#         print(result)

#     else:
#         print("Database connection failed.")


# testing()


# ---------------------------------------------------------------------------------------------
from start_database import start_database
from objects.performance import Performance


def testing():
    db = start_database()

    if db:
        print("\n" + "=" * 50)
        print("PERFORMANCE TESTING")
        print("=" * 50)

        print("\nVIEW ALL PERFORMANCES:")
        result = db.service.performance.viewAllPerformances()
        for performance in result:
            print(performance)

        print("\nLOCATE PERFORMANCE BY ID:")
        result = db.service.performance.locatePerformanceId(1)
        print(result)

        print("\nLOCATE PERFORMANCE (starttime and endtime) BY ID:")
        result = db.service.performance.locatePerformancebyPerformanceId(1)
        print(result)

        print("\nLOCATE PERFORMANCE BY PRODUCTION ID:")
        result = db.service.performance.locatePerformanceByProductionId(1)
        print(result)

        print("\nLOCATE PERFORMANCE BY DATE:")
        result = db.service.performance.locatePerformanceByDate("2024-01-15")
        print(result)

        print("\nLOCATE PERFORMANCE SCHEDULE:")
        result = db.service.performance.locatePerformanceSchedule(
            productionId=1,
            date="2024-01-15",
            startTime="19:00:00",
            endTime="21:00:00"
        )
        print(result)

        print("\nCREATE PERFORMANCE:")
        result = db.service.performance.createPerformance(
            Performance(
                productionId=1,
                startTime="10:00:00",
                endTime="12:00:00",
                date="2024-12-01",
                totalSeats=30
            )
        )
        print(result)

        print("\nUPDATE PERFORMANCE:")
        result = db.service.performance.updatePerformance(
            Performance(
                performanceId=1,
                productionId=1,
                startTime="18:00:00",
                endTime="20:00:00",
                date="2024-01-15",
                totalSeats=30
            )
        )
        print(result)

        print("\nTEST INVALID PERFORMANCE ID:")
        result = db.service.performance.locatePerformanceId("abc")
        print(result)

        print("\nTEST NON-EXISTING PERFORMANCE:")
        result = db.service.performance.locatePerformanceId(999)
        print(result)

        print("\nTEST INVALID DATE FORMAT:")
        result = db.service.performance.locatePerformanceByDate("01-15-2024")
        print(result)

        print("\nTEST INVALID TIME SCHEDULE:")
        result = db.service.performance.createPerformance(
            Performance(
                productionId=1,
                startTime="22:00:00",
                endTime="20:00:00",
                date="2024-12-02",
                totalSeats=30
            )
        )
        print(result)

        # Optional only.
        # Use this only if the performance has no connected tickets.
        # print("\nDELETE PERFORMANCE:")
        # result = db.service.performance.deletePerformance(1)
        # print(result)


testing()
# -----------------------------------------------------------------------------------------------------

# from start_database import start_database
# from objects.ticket import Ticket


# def testing():
#     db = start_database()

#     if db:
#         print("\n" + "=" * 50)
#         print("TICKET TESTING")
#         print("=" * 50)

#         print("\nVIEW ALL TICKETS:")
#         result = db.service.ticket.viewAllTickets()
#         for ticket in result:
#             print(ticket)

#         print("\nGENERATE TICKET NUMBER:")
#         result = db.service.ticket.generateTicketNumber(30)
#         print(result)

#         print("\nVIEW TICKET DETAILS:")
#         result = db.service.ticket.viewTicketDetails(1, 1)
#         for ticket in result:
#             print(ticket)

#         print("\nLOCATE TICKET BY ID:")
#         result = db.service.ticket.locateTicketId(1)
#         print(result)

#         print("\nLOCATE TICKET BY TICKET NUMBER:")
#         result = db.service.ticket.locateTicketByNumber("1cal011519")
#         for ticket in result:
#             print(ticket)

#         print("\nLOCATE TICKETS BY CUSTOMER:")
#         result = db.service.ticket.locateTicketsByCustomer(1)
#         for ticket in result:
#             print(ticket)

#         print("\nLOCATE TICKETS BY STATUS:")
#         result = db.service.ticket.locateTicketsByStatus("sold")
#         for ticket in result:
#             print(ticket)

#         print("\nLOCATE TICKETS BY PRODUCTION:")
#         result = db.service.ticket.locateTicketsByProduction(1)
#         for ticket in result:
#             print(ticket)

#         print("\nUPDATE TICKET STATUS:")
#         result = db.service.ticket.updateTicketStatus(1, "sold")
#         print(result)

#         print("\nPURCHASE TICKET:")
#         result = db.service.ticket.purchaseTicket(
#             performanceSeatId=1,
#             customerId=1,
#             status="sold",
#             saleDate="2024-01-10"
#         )
#         print(result)

#         print("\nTEST INVALID TICKET ID:")
#         result = db.service.ticket.locateTicketId("abc")
#         print(result)

#         print("\nTEST NON-EXISTING TICKET:")
#         result = db.service.ticket.locateTicketId(999)
#         print(result)

#     else:
#         print("Database connection failed.")


# testing()


# -----------------------------------------------------------------------------------------------------------------
# from start_database import start_database
# from objects.transaction import Transaction


# def testing():
#     db = start_database()

#     if db:
#         print("\n" + "=" * 50)
#         print("TRANSACTION TESTING")
#         print("=" * 50)

#         print("\nVIEW ALL TRANSACTIONS:")
#         result = db.service.transaction.viewAllTransactions()
#         for transaction in result:
#             print(transaction)

#         print("\nVIEW TRANSACTION REPORT:")
#         result = db.service.transaction.viewTransactionReport()
#         for transaction in result:
#             print("\n")
#             print(transaction)

#         print("\nVIEW HIGHEST EARNERS:")
#         result = db.service.transaction.viewHighestEarners()
#         for transaction in result:
#             print(transaction)

#         print("\nVIEW COMMISSION BY STAFF:")
#         result = db.service.transaction.viewCommissionByStaff()
#         for transaction in result:
#             print(transaction)

#         print("\nLOCATE TRANSACTION BY ID:")
#         result = db.service.transaction.locateTransactionId(1)
#         print(result)

#         print("\nLOCATE TRANSACTIONS BY STAFF:")
#         result = db.service.transaction.locateTransactionsByStaff(1)
#         for transaction in result:
#             print(transaction)

#         print("\nLOCATE TRANSACTIONS BY TICKET:")
#         result = db.service.transaction.locateTransactionsByTicket(1)
#         for transaction in result:
#             print(transaction)

#         print("\nLOCATE TRANSACTIONS BY TYPE:")
#         result = db.service.transaction.locateTransactionsByType("purchased")
#         for transaction in result:
#             print(transaction)

#         print("\nLOCATE TRANSACTIONS BY DATE:")
#         result = db.service.transaction.locateTransactionsByDate("2024-01-10")
#         for transaction in result:
#             print(transaction)

#         print("\nLOCATE TRANSACTIONS BY DATE RANGE:")
#         result = db.service.transaction.locateTransactionsByDateRange(
#             "2024-01-01",
#             "2024-01-31"
#         )
#         for transaction in result:
#             print(transaction)

#         print("\nCREATE TRANSACTION:")
#         result = db.service.transaction.createTransaction(
#             Transaction(
#                 ticketId=1,
#                 staffId=1,
#                 transactionDate="2024-01-10",
#                 type="purchased",
#                 amount=1500
#             )
#         )
#         print(result)

#         print("\nTEST INVALID TRANSACTION ID:")
#         result = db.service.transaction.locateTransactionId("abc")
#         print(result)

#         print("\nTEST NON-EXISTING TRANSACTION:")
#         result = db.service.transaction.locateTransactionId(999)
#         print(result)

#     else:
#         print("Database connection failed.")


# testing()