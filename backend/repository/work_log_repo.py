class WorkLogRepo:
    def __init__(self, conn):
        self.conn = conn

    def create_work_log(self, new_work_log):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO Work_Log (staff_id, performance_id, hours_worked) VALUES (%s, %s, %s)",
                (new_work_log.staff_id, new_work_log.performance_id, new_work_log.hours_worked)
            )
        self.conn.commit()

    # returns work log per staff
    def get_staff_work_log(self, staff_id):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT 
                    p.title,
                    perf.date,
                    perf.start_time,
                    perf.end_time,
                    w.hours_worked
                FROM Work_Log w
                LEFT JOIN Performance perf ON w.performance_id = perf.performance_id
                LEFT JOIN Production p ON perf.production_id = p.production_id
                WHERE w.staff_id = %s;
                """,
                (staff_id,)
                )
            rows = cur.fetchall()
            return rows
    
    