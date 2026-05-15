class ProductionRepo:
    def __init__(self, connect):
        self.connect = connect

    # retrieves all productions
    def getAllProductions(self):
        with self.connect.cursor() as cur:
            cur.execute("SELECT * FROM production")
            rows = cur.fetchall()
            return rows

    # call to create production
    def createProduction(self, newProduction):
        with self.connect.cursor() as cur:
            cur.execute(
                "INSERT INTO production (title, start_date, end_date) VALUES (%s, %s, %s)",
                (
                    newProduction.title,
                    newProduction.startDate,
                    newProduction.endDate
                )
            )
        self.connect.commit()

    # call to update production
    def updateProduction(self, updatedProduction):
        with self.connect.cursor() as cur:
            cur.execute(
                """
                UPDATE production
                SET title = %s, start_date = %s, end_date = %s
                WHERE production_id = %s
                """,
                (
                    updatedProduction.title,
                    updatedProduction.startDate,
                    updatedProduction.endDate,
                    updatedProduction.productionId
                )
            )
        self.connect.commit()

    # checks if productionID already exists
    def locateProdId(self, productionId):
        with self.connect.cursor() as cur:
            cur.execute(
                """
                SELECT * FROM production
                WHERE production_id = %s
                """,
                (productionId,)
            )

            row = cur.fetchone()

            if row:
                return row
            return None
        
    def locateProdTitle(self, productionTitle):
        with self.connect.cursor() as cur:
            cur.execute(
                """
                SELECT * FROM production
                WHERE title = %s
                """,
                (productionTitle,)
            )
            row = cur.fetchone()

            if row:
                return row
            return None
        
    def deleteProduction(self, productionId):
        with self.connect.cursor() as cur:
            cur.execute(
                """
                DELETE FROM production
                WHERE production_id = %s
                """,
                (productionId,)
            )
        self.connect.commit()

    # ascending list of mopnths where there will be opening of new show
    def getOpeningMonths(self):
        with self.connect.cursor() as cur:
            cur.execute(
                """
                SELECT DISTINCT 
                    EXTRACT(MONTH FROM start_date) AS month_number,
                    TO_CHAR(start_date, 'Month') AS month_name
                FROM production
                ORDER BY month_number
                """
            )
            return cur.fetchall()
        
    # number of performances by production
    def getNumberOfPerformancesByProduction(self):
        with self.connect.cursor() as cur:
            cur.execute(
                """
                SELECT 
                    p.production_id,
                    p.title,
                    COUNT(per.performance_id) AS number_of_performances
                FROM production p
                LEFT JOIN performance per 
                    ON p.production_id = per.production_id
                GROUP BY p.production_id, p.title
                ORDER BY p.production_id
                """
            )
            return cur.fetchall()
        
    # number of seats by production
    def getNumberOfSeatsByProduction(self):
        with self.connect.cursor() as cur:
            cur.execute(
                """
                SELECT 
                    p.production_id,
                    p.title,
                    COALESCE(SUM(per.total_seats), 0) AS total_seats
                FROM production p
                LEFT JOIN performance per 
                    ON p.production_id = per.production_id
                GROUP BY p.production_id, p.title
                ORDER BY p.production_id
                """
            )
            return cur.fetchall()
    
    # list of productions that have lless than 50% of to total seats sold
    def getProductionsLessThan50PercentSold(self):
        with self.connect.cursor() as cur:
            cur.execute(
                """
                SELECT
                    p.production_id,
                    p.title,
                    COUNT(t.ticket_id) FILTER (WHERE t.status = 'sold') AS seats_sold,
                    COALESCE(SUM(per.total_seats), 0) AS total_seats,
                    ROUND(
                        (
                            COUNT(t.ticket_id) FILTER (WHERE t.status = 'sold')::DECIMAL
                            / NULLIF(COALESCE(SUM(per.total_seats), 0), 0)
                        ) * 100, 
                        2
                    ) AS percent_sold
                FROM production p
                LEFT JOIN performance per 
                    ON p.production_id = per.production_id
                LEFT JOIN performance_seat ps 
                    ON per.performance_id = ps.performance_id
                LEFT JOIN ticket t 
                    ON ps.performance_seat_id = t.performance_seat_id
                GROUP BY p.production_id, p.title
                HAVING 
                    (
                        COUNT(t.ticket_id) FILTER (WHERE t.status = 'sold')::DECIMAL
                        / NULLIF(COALESCE(SUM(per.total_seats), 0), 0)
                    ) < 0.50
                ORDER BY percent_sold ASC
                """
            )
            return cur.fetchall()