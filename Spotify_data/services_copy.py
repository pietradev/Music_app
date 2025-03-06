from dotenv import load_dotenv
import pymysql
import os

load_dotenv()

# username = os.getenv("DB_NAME")
# password = os.getenv("DB_PASSWORD")
# host = "localhost"



username = 'poliveira'
password = 'Pmao*2401'
host = 'rowan-projects-classes.c8boum2y64fr.us-east-1.rds.amazonaws.com'
database = 'music_db'

def db_connection(host, user, password, database):
    try:
        conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            cursorclass=pymysql.cursors.DictCursor  # Ensures results are returned as dictionaries
        )
        print("Connection was successfully established")
        cursor = conn.cursor()
        return cursor, conn
    except pymysql.MySQLError as e:
        print(f"Database connection failed: {e}")
        return None, None

def insert_data_into_db(playlist_name, tracks_info, cursor, conn):
    try:
        cursor.execute("""
            INSERT INTO music_db.playlist (name)
            VALUES(%s)
        """, (playlist_name,))
        conn.commit()
        print(f"Playlist '{playlist_name}' inserted successfully!")
    except pymysql.MySQLError as e:  # Update exception type
        print("MySQL Error:", e)
    finally:
        cursor.close()
        conn.close()



