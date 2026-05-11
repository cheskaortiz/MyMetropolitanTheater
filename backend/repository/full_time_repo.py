class FullTimeRepo:
    def __init__(self, conn):
        self.conn = conn

    def create_full_time(self, new_full_time):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO Full_Time (staff_id, monthly_salary) VALUES (%s, %s)",
                (new_full_time.staff_id, new_full_time.monthly_salary)
            )
        self.conn.commit()

    def delete_full_time(self, staff_id):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM Full_Time
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
                FROM Full_Time
                WHERE staff_id = %s
                """,
                (staff_id,)
            )
            row = cur.fetchone()

            if row:
                return row
            return None

    