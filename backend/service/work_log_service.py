from datetime import datetime, date
from repository.work_log_repo import WorkLogRepo
from repository.staff_repo import StaffRepo

class WorkLogService:
    def __init__(self, conn):
        self.work_log_repo = WorkLogRepo(conn)
        self.staff_repo = StaffRepo(conn)
        # self.performance_repo = 

    # get work log of specific staff
    def get_work_logs(self, staff_id):
        logs = self.work_log_repo.get_staff_work_log(staff_id)

        if logs is None:
            return "No work logs available."
        
        work_logs = []

        for log in logs:
            log_date = log[1]   
            log_start_time = log[2]  
            log_end_time = log[3]  

            work_logs.append({
                "title": log[0],
                "date": log_date.strftime("%m/%d/%Y"),
                "start_time": log_start_time.strftime("%I:%M %p").lstrip("0"),
                "start_time": log_end_time.strftime("%I:%M %p").lstrip("0"),
                "hours_worked": log[4]
            })

        return work_logs # returns a dictionary containing the staff worklogs' title, date, time, and hours worked
    
    # create new work_log for staff 
    # ONLY essential to be filled is staff_id and performance_id [hours_worked is calculated here]
    def create_work_log(self, new_log):
        staff = self.staff_repo.locate_staff(new_log.staff_id)

        if staff[2] != "Hourly":
            return "Only hourly staffs are counted for work logs."
        
        # if new_log.performance_id is None:
        # return "Performance id does not exist."

        # performance_time =
        # start_dt = datetime.combine(date.today(), performance_time[0])
        # end_dt = datetime.combine(date.today(), performance_time[1])

        # new_log.hours_worked = int((end_dt - start_dt).total_seconds() / 3600)

        # self.work_log_repo.create_work_log(new_log)

        # return "Added new work log successfully."
        
        