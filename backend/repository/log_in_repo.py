class LogInRepo:
    def __init__(self, conn):
        self.conn = conn

    def create_log_in(self, new_log_in):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO Log_In (staff_id, password) VALUES (%s, %s)",
                (new_log_in.staff_id, new_log_in.password)
            )
        self.conn.commit()

    # returns log_in per staff
    def get_log_in(self, staff_id):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT * FROM Log_In
                WHERE staff_id = %s
                """,
                (staff_id,)
                )
            row = cur.fetchone()
            return row
    
    def delete_log_in(self, staff_id):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM Log_In
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
                FROM Log_In
                WHERE staff_id = %s
                """,
                (staff_id,)
            )
            row = cur.fetchone()

            if row:
                return row
            return None
    