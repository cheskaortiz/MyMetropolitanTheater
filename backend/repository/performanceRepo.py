class PerformanceRepo:
    def __init__(self, connect):
        self.connect = connect

    # retrieves all performances
    def getAllPerformance(self):
        with self.connect.cursor() as cur:
            cur.execute("SELECT * FROM performance")
            rows = cur.fetchall()
            return rows

    # call to create performance
    def createPerformance(self, newPerformance):
        with self.connect.cursor() as cur:
            cur.execute(
                """
                INSERT INTO performance 
                (production_id, start_time, end_time, date, total_seats) 
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    newPerformance.productionId,
                    newPerformance.startTime,
                    newPerformance.endTime,
                    newPerformance.date,
                    newPerformance.totalSeats
                )
            )
        self.connect.commit()

    # call to update performance
    def updatePerformance(self, updatedPerformance):
        with self.connect.cursor() as cur:
            cur.execute(
                """
                UPDATE performance
                SET production_id = %s,
                    start_time = %s,
                    end_time = %s,
                    date = %s,
                    total_seats = %s
                WHERE performance_id = %s
                """,
                (
                    updatedPerformance.productionId,
                    updatedPerformance.startTime,
                    updatedPerformance.endTime,
                    updatedPerformance.date,
                    updatedPerformance.totalSeats,
                    updatedPerformance.performanceId
                )
            )
        self.connect.commit()

    # call to delete performance
    def deletePerformance(self, performanceId):
        with self.connect.cursor() as cur:
            cur.execute(
                """
                DELETE FROM performance
                WHERE performance_id = %s
                """,
                (performanceId,)
            )
        self.connect.commit()

    def locatePerformanceId(self, performanceId):
        with self.connect.cursor() as cur:
            cur.execute(
                """
                SELECT
                    performance_id,
                    production_id,
                    start_time,
                    end_time,
                    date,
                    total_seats
                FROM performance
                WHERE performance_id = %s
                """,
                (performanceId,)
            )

            row = cur.fetchone()

            if row:
                return row
            return None
        
    # locates start time and ent time of performance by performance_id
    def locatePerformanceByPerformanceId(self, performanceId):
        with self.connect.cursor() as cur:
            cur.execute(
                """
                SELECT start_time, end_time
                FROM performance
                WHERE performance_id = %s
                """,
                (performanceId,)
            )

            row = cur.fetchone()

            if row:
                return row
            return None

    # locates all performances under one production
    def locatePerformanceByProductionId(self, productionId):
        with self.connect.cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM performance
                WHERE production_id = %s
                ORDER BY date, start_time
                """,
                (productionId,)
            )

            return cur.fetchall()

    # locates all performances on a specific date
    def locatePerformanceByDate(self, date):
        with self.connect.cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM performance
                WHERE date = %s
                ORDER BY start_time
                """,
                (date,)
            )

            return cur.fetchall()

    # checks if the same performance schedule already exists
    def locatePerformanceSchedule(self, productionId, date, startTime, endTime):
        with self.connect.cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM performance
                WHERE production_id = %s
                AND date = %s
                AND start_time = %s
                AND end_time = %s
                """,
                (productionId, date, startTime, endTime)
            )

            row = cur.fetchone()

            if row:
                return row
            return None

    # checks if tickets already exist for the performance
    def hasTicketsForPerformance(self, performanceId):
        with self.connect.cursor() as cur:
            cur.execute(
                """
                SELECT t.ticket_id
                FROM ticket t
                JOIN performance_seat ps
                    ON t.performance_seat_id = ps.performance_seat_id
                WHERE ps.performance_id = %s
                LIMIT 1
                """,
                (performanceId,)
            )

            row = cur.fetchone()

            if row:
                return True
            return False