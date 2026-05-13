# CREATE TABLE Performance (
#     performance_id INTEGER PRIMARY KEY,
#     production_id INTEGER NOT NULL,
#     time TIME,
#     date DATE,
#     total_seats INTEGER,
#     FOREIGN KEY (production_id) REFERENCES Production(production_id)
# );

class Performance:
    def __init__(self, performanceId=None, productionId=None, startTime=None, endTime=None, date=None, totalSeats=None):
        self.performanceId = performanceId
        self.productionId = productionId
        self.startTime = startTime
        self.endTime = endTime
        self.date = date
        self.totalSeats = totalSeats