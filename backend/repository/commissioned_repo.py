class CommissionedRepo:
    def __init__(self, conn):
        self.conn = conn

    def create_commission(self, new_commissioned):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO Commissioned (staff_id, commission_rate) VALUES (%s, %s)",
                (new_commissioned.staff_id, new_commissioned.commission_rate)
            )
        self.conn.commit()
    
    def delete_commissioned(self, staff_id):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM Commissioned
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
                FROM Commissioned
                WHERE staff_id = %s
                """,
                (staff_id,)
            )
            row = cur.fetchone()

            if row:
                return row
            return None

    
    