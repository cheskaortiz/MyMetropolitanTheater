class TransactionRepo:
    def __init__(self, connect):
        self.connect = connect
    
    # retrieves all transactions
    def getAllTransactions(self):
        with self.connect.cursor() as cur:
            cur.execute("SELECT * FROM Transactions")
            rows = cur.fetchall()
            return rows

    # call to create transaction
    def createTransaction(self, newTransaction):
        with self.connect.cursor() as cur:
            cur.execute(
                "INSERT INTO transactions (ticket_id, staff_id, transaction_date, type, amount) VALUES (%s, %s, %s, %s, %s)",
                (
                    newTransaction.ticketId,
                    newTransaction.staffId,
                    newTransaction.transactionDate,
                    newTransaction.type,
                    newTransaction.amount
                )
            )
        self.connect.commit()

    # # call to delete transaction
    # def deleteTransaction(self, transactionId):
    #     with self.connect.cursor() as cur:
    #         cur.execute("DELETE FROM Transactions WHERE transaction_id = %s", (transactionId,))
    #         self.connect.commit()

    def locateTransactionId(self, transactionId):
        with self.connect.cursor() as cur:
            cur.execute(
                """
                SELECT * FROM transactions
                WHERE transaction_id = %s
                """,
                (transactionId,)
            )
            row = cur.fetchone()
        
            if row:
                return row
            return None
    
    def locateTransactionsbyStaff(self, staffId):
        with self.connect.cursor() as cur:
            cur.execute(
                """
                SELECT
                    tr.transaction_id,
                    tr.transaction_date,
                    tr.type,
                    tr.amount,
                    s.name AS staff_name,
                    c.name AS customer_name,
                    t.ticket_number,
                    t.status,
                    prod.title,
                    per.date,
                    per.start_time,
                    per.end_time,
                    seat.seat_number,
                    seat.seat_view,
                    ps.price
                FROM transactions tr
                JOIN staff s 
                    ON tr.staff_id = s.staff_id
                JOIN ticket t 
                    ON tr.ticket_id = t.ticket_id
                JOIN customer c 
                    ON t.customer_id = c.customer_id
                JOIN performance_seat ps 
                    ON t.performance_seat_id = ps.performance_seat_id
                JOIN seat seat 
                    ON ps.seat_id = seat.seat_id
                JOIN performance per 
                    ON ps.performance_id = per.performance_id
                JOIN production prod 
                    ON per.production_id = prod.production_id
                WHERE tr.staff_id = %s
                ORDER BY tr.transaction_date, tr.transaction_id
                """,
                (staffId,)
            )
            return cur.fetchall()
        

    def locateTransactionsbyTicketId(self, ticketId):
        with self.connect.cursor() as cur:
            cur.execute(
                """
                SELECT
                    tr.transaction_id,
                    tr.transaction_date,
                    tr.type,
                    tr.amount,
                    s.name AS staff_name,
                    c.name AS customer_name,
                    t.ticket_number,
                    t.status,
                    prod.title,
                    per.date,
                    per.start_time,
                    per.end_time,
                    seat.seat_number,
                    seat.seat_view,
                    ps.price
                FROM transactions tr
                JOIN staff s 
                    ON tr.staff_id = s.staff_id
                JOIN ticket t 
                    ON tr.ticket_id = t.ticket_id
                JOIN customer c 
                    ON t.customer_id = c.customer_id
                JOIN performance_seat ps 
                    ON t.performance_seat_id = ps.performance_seat_id
                JOIN seat seat 
                    ON ps.seat_id = seat.seat_id
                JOIN performance per 
                    ON ps.performance_id = per.performance_id
                JOIN production prod 
                    ON per.production_id = prod.production_id
                WHERE tr.ticket_id = %s
                ORDER BY tr.transaction_date, tr.transaction_id
                """,
                (ticketId,)
            )
            return cur.fetchall()
            
    def locateTransactionsbyType(self, type):
        with self.connect.cursor() as cur:
            cur.execute(
                """
                SELECT
                    tr.transaction_id,
                    tr.transaction_date,
                    tr.type,
                    tr.amount,
                    s.name AS staff_name,
                    c.name AS customer_name,
                    t.ticket_number,
                    t.status,
                    prod.title,
                    per.date,
                    per.start_time,
                    per.end_time,
                    seat.seat_number,
                    seat.seat_view,
                    ps.price
                FROM transactions tr
                JOIN staff s 
                    ON tr.staff_id = s.staff_id
                JOIN ticket t 
                    ON tr.ticket_id = t.ticket_id
                JOIN customer c 
                    ON t.customer_id = c.customer_id
                JOIN performance_seat ps 
                    ON t.performance_seat_id = ps.performance_seat_id
                JOIN seat seat 
                    ON ps.seat_id = seat.seat_id
                JOIN performance per 
                    ON ps.performance_id = per.performance_id
                JOIN production prod 
                    ON per.production_id = prod.production_id
                WHERE LOWER(tr.type) = LOWER(%s)
                ORDER BY tr.transaction_date, tr.transaction_id
                """,
                (type,)
            )
            return cur.fetchall()
        
    def locateTransactionsbyDate(self, date):
        with self.connect.cursor() as cur:
            cur.execute(
                """
                SELECT
                    tr.transaction_id,
                    tr.transaction_date,
                    tr.type,
                    tr.amount,
                    s.name AS staff_name,
                    c.name AS customer_name,
                    t.ticket_number,
                    t.status,
                    prod.title,
                    per.date,
                    per.start_time,
                    per.end_time,
                    seat.seat_number,
                    seat.seat_view,
                    ps.price
                FROM transactions tr
                JOIN staff s 
                    ON tr.staff_id = s.staff_id
                JOIN ticket t 
                    ON tr.ticket_id = t.ticket_id
                JOIN customer c 
                    ON t.customer_id = c.customer_id
                JOIN performance_seat ps 
                    ON t.performance_seat_id = ps.performance_seat_id
                JOIN seat seat 
                    ON ps.seat_id = seat.seat_id
                JOIN performance per 
                    ON ps.performance_id = per.performance_id
                JOIN production prod 
                    ON per.production_id = prod.production_id
                WHERE tr.transaction_date = %s
                ORDER BY tr.transaction_date, tr.transaction_id
                """,
                (date,)
            )
            return cur.fetchall()
        
    def getTransactionReport(self):
        with self.connect.cursor() as cur:
            cur.execute(
                """
                SELECT
                    tr.transaction_id,
                    tr.transaction_date,
                    tr.type,
                    tr.amount,
                    s.name AS staff_name,
                    c.name AS customer_name,
                    t.ticket_number,
                    t.status,
                    prod.title,
                    per.date,
                    per.start_time,
                    per.end_time,
                    seat.seat_number,
                    seat.seat_view,
                    ps.price
                FROM transactions tr
                JOIN staff s 
                    ON tr.staff_id = s.staff_id
                JOIN ticket t 
                    ON tr.ticket_id = t.ticket_id
                JOIN customer c 
                    ON t.customer_id = c.customer_id
                JOIN performance_seat ps 
                    ON t.performance_seat_id = ps.performance_seat_id
                JOIN seat seat 
                    ON ps.seat_id = seat.seat_id
                JOIN performance per 
                    ON ps.performance_id = per.performance_id
                JOIN production prod 
                    ON per.production_id = prod.production_id
                ORDER BY tr.transaction_date, tr.transaction_id
                """
            )
            return cur.fetchall()


    def getEarningsByStaff(self):
        with self.connect.cursor() as cur:
            cur.execute(
                """
                SELECT
                    s.staff_id,
                    s.name AS staff_name,
                    SUM(tr.amount) AS total_sales
                FROM transactions tr
                JOIN staff s 
                    ON tr.staff_id = s.staff_id
                JOIN department d 
                    ON s.department_id = d.department_id
                WHERE LOWER(d.name) = 'sales'
                AND LOWER(tr.type) = 'purchased'
                GROUP BY s.staff_id, s.name
                ORDER BY total_sales DESC
                """
            )
            return cur.fetchall()
         
    def getCommissionByStaff(self):
        with self.connect.cursor() as cur:
            cur.execute(
                """
                SELECT
                    s.staff_id,
                    s.name AS staff_name,
                    SUM(tr.amount) AS total_sales,
                    SUM(tr.amount) * co.commission_rate AS commission
                FROM transactions tr
                JOIN staff s 
                    ON tr.staff_id = s.staff_id
                JOIN department d 
                    ON s.department_id = d.department_id
                JOIN commissioned co 
                    ON s.staff_id = co.staff_id
                WHERE LOWER(d.name) = 'sales'
                AND LOWER(tr.type) = 'purchased'
                GROUP BY s.staff_id, s.name, co.commission_rate
                ORDER BY commission DESC
                """
            )
            return cur.fetchall()

    def locateTransactionsByDateRange(self, startDate, endDate):
        with self.connect.cursor() as cur:
            cur.execute(
                """
                SELECT
                    tr.transaction_id,
                    tr.transaction_date,
                    tr.type,
                    tr.amount,
                    s.name AS staff_name,
                    c.name AS customer_name,
                    t.ticket_number,
                    t.status,
                    prod.title,
                    per.date,
                    per.start_time,
                    per.end_time,
                    seat.seat_number,
                    seat.seat_view,
                    ps.price
                FROM transactions tr
                JOIN staff s 
                    ON tr.staff_id = s.staff_id
                JOIN ticket t 
                    ON tr.ticket_id = t.ticket_id
                JOIN customer c 
                    ON t.customer_id = c.customer_id
                JOIN performance_seat ps 
                    ON t.performance_seat_id = ps.performance_seat_id
                JOIN seat seat 
                    ON ps.seat_id = seat.seat_id
                JOIN performance per 
                    ON ps.performance_id = per.performance_id
                JOIN production prod 
                    ON per.production_id = prod.production_id
                WHERE tr.transaction_date BETWEEN %s AND %s
                ORDER BY tr.transaction_date, tr.transaction_id
                """,
                (startDate, endDate)
            )
            return cur.fetchall()