from database_connection import get_connection
from database import Database

def start_database():
    conn = get_connection()

    if conn:
        return Database(conn)
    else:
        return False