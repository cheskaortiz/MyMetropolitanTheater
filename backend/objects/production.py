# -- Production & Performance
# CREATE TABLE Production (
#     production_id INTEGER PRIMARY KEY,
#     title VARCHAR(255) NOT NULL,
#     start_date DATE,
#     end_date DATE
# );

# CREATE TABLE Production (
#     production_id SERIAL PRIMARY KEY,
#     title VARCHAR(255) NOT NULL,
#     start_date DATE,
#     end_date DATE
# );

class Production:
    def __init__(self, productionId=None, title=None, startDate=None, endDate=None):
        self.productionId = productionId
        self.title = title
        self.startDate = startDate
        self.endDate = endDate
