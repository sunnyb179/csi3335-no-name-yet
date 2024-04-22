import mysql.connector
from mysql.connector import Error

def create_connection():

    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='nguyen12',
            database='nonameyet'
        )
        if connection.is_connected():
            db_info = connection.get_server_info()
            print("Successfully connected to MariaDB server version", db_info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database:", record)
    except Error as e:
        print("Error while connecting to MariaDB", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MariaDB connection is closed")

create_connection()
