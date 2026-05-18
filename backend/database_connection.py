import psycopg2
def get_connection():
    try:
        conn = psycopg2.connect(
            database="MyMetropolitanTheaterDatabase", #change to your created database
            user="postgres",
            password="AKOSICYAN69", #change to your own password
            host="127.0.0.1",
            port=5432,
        )
    except:
        conn = False
    
    if not conn:
        print("Connection to the PostgreSQL encountered and error.")

    return conn

