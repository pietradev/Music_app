from dotenv import load_dotenv
import mysql.connector
import os

load_dotenv()

# username = os.getenv("DB_NAME")
# password = os.getenv("DB_PASSWORD")
# host = "localhost"
# database = "music_app"


# username = 'poliveira'
# password = 'Pmao*24011997'
# host = 'rowan-projects-classes.c8boum2y64fr.us-east-1.rds.amazonaws.com'
# database = 'music_db'


def db_connection(host, user, password, database):
    
    conn = mysql.connector.connect(
            host =host,
            username=user,
            password = password,
            database = database,
            auth_plugin="mysql_native_password"  # Add this line

    )


    if conn:
        print("Connection was sucessfully established")
        cursor = conn.cursor()
        return cursor, conn

def insert_data_into_db(playlist_name, tracks_info, cursor, conn):
    try:
        cursor.execute("""
                       INSERT INTO music_app.playlist (name)
                       VALUES(%s)
                       
                       """, (playlist_name,) )  
        conn.commit()  
        print(f"Playlist '{playlist_name}' inserted successfully!")
    except mysql.connector.Error as e:
        print("MYSQL ERROR:", e)
    
    finally:
        cursor.close()
        conn.close()


