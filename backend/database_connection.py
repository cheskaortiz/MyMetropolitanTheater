import psycopg2
def get_connection():
    try:
        return psycopg2.connect(
            database="MyMetropolitanTheater", #change to your created database
            user="postgres",
            password="Sherlin21@@@", #change to your own password
            host="127.0.0.1",
            port=5432,
        )
    except:
        return False
conn = get_connection()
if conn:
    print("Connection to the PostgreSQL established successfully.")
else:
    print("Connection to the PostgreSQL encountered and error.")