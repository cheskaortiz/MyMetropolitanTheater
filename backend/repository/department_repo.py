class DepartmentRepo:
    def __init__(self, conn):
        self.conn = conn

    def create_department(self, new_dept):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO Department (name, manager_id) VALUES (%s, %s)",
                (new_dept.dept_name, new_dept.manager_id)
            )
        self.conn.commit()
    
    def update_department(self, updated_dept):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                UPDATE Department
                SET name = %s,
                    manager_id = %s
                WHERE department_id = %s
                """,
                (updated_dept.dept_name, updated_dept.manager_id, updated_dept.id)
            )
            self.conn.commit()
    
    def delete_department(self, dept_id):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM Department
                WHERE department_id = %s
                """,
                (dept_id,)
            )
            self.conn.commit()

    def get_department(self, dept_name):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT 
                    d.name,
                    s.staff_id,
                    s.name AS staff_name,
                    s.type AS type
                FROM Department d
                LEFT JOIN Staff s 
                    ON s.department_id = d.department_id
                WHERE d.name = %s
                """,
                (dept_name,)
            )
            return cur.fetchall()

    def locate_department_name(self, dept_name):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT * FROM Department
                WHERE name = %s
                """,
                (dept_name,)
            )
            row = cur.fetchone()

            if row:
                return row
            return None
    
    def locate_department_id(self, dept_id):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT * FROM Department
                WHERE department_id = %s
                """,
                (dept_id,)
            )
            row = cur.fetchone()

            if row:
                return row
            return None
    
    def locate_manager(self, manager_id):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT * FROM Department
                WHERE manager_id = %s
                """,
                (manager_id,)
            )
            row = cur.fetchone()

            if row:
                return row
            return None
    
    