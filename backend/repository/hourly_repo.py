class HourlyRepo:
    def __init__(self, conn):
        self.conn = conn

    def create_hourly(self, new_hourly):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO Hourly (staff_id, hourly_rate, famous_level) VALUES (%s, %s, %s)",
                (new_hourly.staff_id, new_hourly.hourly_rate, new_hourly.famous_level)
            )
        self.conn.commit()
    
    def delete_hourly(self, staff_id):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM Hourly
                WHERE staff_id = %s
                """,
                (staff_id,)
            )
    
            self.conn.commit()
    
    def locate_staff(self, staff_id):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT staff_id
                FROM Hourly
                WHERE staff_id = %s
                """,
                (staff_id,)
            )
            row = cur.fetchone()

            if row:
                return row
            return None

    
    