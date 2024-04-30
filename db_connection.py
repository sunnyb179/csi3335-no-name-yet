import mysql.connector
from mysql.connector import Error, errorcode
from csi3335sp2023 import mysql_dict

def prepare_database():
    try:
        # Initial connection to check/create database
        connection = mysql.connector.connect(
            host=mysql_dict['location'],
            user=mysql_dict['user'],
            password=mysql_dict['password']
        )
        cursor = connection.cursor()
        cursor.execute("SHOW DATABASES LIKE 'nonameyet'")
        if cursor.fetchone() is None:
            cursor.execute("CREATE DATABASE nonameyet")
            print("Database 'nonameyet' created successfully.")
        cursor.close()
        connection.close()

        # Connect to the specific database
        connection = mysql.connector.connect(
            host=mysql_dict['location'],
            user=mysql_dict['user'],
            password=mysql_dict['password'],
            database=mysql_dict['database']
        )
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")
        if not cursor.fetchall():  # If no tables, assume the database is empty
            with open('nonameyet.sql', 'r') as file:
                sql_script = file.read()
            statements = sql_script.split(';')
            total_statements = len(statements)
            executed_count = 0
            for statement in statements:
                if statement.strip():
                    try:
                        cursor.execute(statement)
                    except mysql.connector.Error as err:
                        print(f"Error executing statement {executed_count + 1}: {err.msg}")
                        if err.errno == errorcode.ER_SYNTAX_ERROR:
                            continue  # Skip syntax errors and continue with next statements
                    executed_count += 1
                    if executed_count % 10 == 0:
                        print(f"Executed {executed_count}/{total_statements} statements.")
            print("SQL script 'nonameyet.sql' executed successfully. All statements processed.")
        cursor.close()
        connection.close()
    except Error as e:
        print("Error during database initialization:", e)



def get_db_connection():
    """Create and return a new connection to the database."""
    try:
        return mysql.connector.connect(
            host=mysql_dict['location'],
            user=mysql_dict['user'],
            password=mysql_dict['password'],
            database=mysql_dict['database']
        )
    except Error as e:
        print(f"Error connecting to the database: {e}")
        return None


prepare_database()
