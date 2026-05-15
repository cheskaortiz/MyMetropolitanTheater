class StaffRepo:
    def __init__(self, conn):
        self.conn = conn

    def create_staff(self, new_staff):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO Staff (department_id, name, type) VALUES (%s, %s, %s) RETURNING staff_id",
                (new_staff.dept_id, new_staff.name, new_staff.staff_type)
            )
            new_id = cur.fetchone()[0]
            self.conn.commit()
            return new_id
    
    def update_staff(self, updated_staff):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                UPDATE Staff
                SET department_id = %s,
                    name = %s,
                    type = %s
                WHERE staff_id = %s
                """,
                (updated_staff.dept_id, updated_staff.name, updated_staff.staff_type, updated_staff.staff_id)
            )
            self.conn.commit()
    
    def delete_staff(self, staff_id):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM Staff
                WHERE staff_id = %s
                """,
                (staff_id,)
            )
    
            self.conn.commit()

    # returns all staff with their respective departments and salaries
    def get_all_staff(self):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT 
                    s.name, 
                    s.type, 
                    d.name AS department_name,

                    CASE
                        WHEN s.type = 'Hourly' THEN COALESCE(w.total_hours, 0) * h.hourly_rate
                        WHEN s.type = 'Full Time' THEN ft.monthly_salary
                        WHEN s.type = 'Commissioned' THEN COALESCE(t.total_sales, 0) * c.commission_rate
                    END AS salary

                FROM Staff s

                LEFT JOIN Department d 
                    ON s.department_id = d.department_id

                LEFT JOIN (
                    SELECT staff_id, SUM(hours_worked) AS total_hours
                    FROM Work_Log
                    GROUP BY staff_id
                ) w ON s.staff_id = w.staff_id

                LEFT JOIN (
                    SELECT staff_id, SUM(amount) AS total_sales
                    FROM Transactions
                    WHERE type = 'purchased'
                    GROUP BY staff_id
                ) t ON s.staff_id = t.staff_id

                LEFT JOIN Full_Time ft 
                    ON s.staff_id = ft.staff_id

                LEFT JOIN Hourly h 
                    ON s.staff_id = h.staff_id

                LEFT JOIN Commissioned c 
                    ON s.staff_id = c.staff_id;
                """
                )
            rows = cur.fetchall()
            return rows
    
    def get_sales_staff(self):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT 
                    s.name, 
                    s.type, 
                    d.name AS department_name,

                    CASE 
                        WHEN s.type = 'Commissioned' 
                            THEN COALESCE(t.total_sales, 0) * c.commission_rate
                    END AS salary

                FROM Staff s

                LEFT JOIN Department d 
                    ON s.department_id = d.department_id

                LEFT JOIN (
                    SELECT staff_id, SUM(amount) AS total_sales
                    FROM Transactions
                    WHERE type = 'purchased'
                    GROUP BY staff_id
                ) t 
                    ON s.staff_id = t.staff_id

                LEFT JOIN Commissioned c 
                    ON s.staff_id = c.staff_id;
                """
                )
            rows = cur.fetchall()
            return rows
        
    def locate_staff(self, staff_id):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT staff_id, name, staff_type
                FROM Staff
                WHERE staff_id = %s
                """,
                (staff_id,)
            )
            row = cur.fetchone()

            if row:
                return row
            return None
    
    