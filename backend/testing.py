from start_database import start_database
from objects.staff_obj import Staff
from objects.log_in_obj import LogIn

def testing():
    db = start_database()

    if db:
        result = db.service.work_log.get_work_logs(2)
        print(result)

testing()

