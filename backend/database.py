from all_service import Service

class Database:
    def __init__(self, conn):
        self.service = Service(conn)
