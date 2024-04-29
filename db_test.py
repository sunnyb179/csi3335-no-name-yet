import mysql.connector  # Import the connector module
from mysql.connector import Error
from connectionDictionary import mysql as db_config

def create_connection():
    connection = None
    try:
        # Connect to the MySQL server using credentials from db_config dictionary
        connection = mysql.connector.connect(
            host=db_config['location'],
            user=db_config['user'],
            password=db_config['password'],
        )
        if connection.is_connected():
            cursor = connection.cursor()
            # Drop the database if it exists and then create it again
            cursor.execute("DROP DATABASE IF EXISTS nonameyet")
            print("Existing database dropped.")
            cursor.execute("CREATE DATABASE nonameyet")
            print("Database 'nonameyet' created successfully.")

            # Use the new database
            cursor.execute("USE nonameyet")

            # Load SQL from a file and execute it
            with open('nonameyet.sql', 'r') as file:
                sql_script = file.read()

            # Execute large SQL script with feedback
            statements = sql_script.split(';')
            total_statements = len(statements)
            executed_count = 0
            for statement in statements:
                if statement.strip():
                    try:
                        cursor.execute(statement)
                        executed_count += 1
                        if executed_count % 10 == 0:
                            print(f"Executed {executed_count}/{total_statements} statements.")
                    except Error as e:
                        print(f"Error executing statement {executed_count + 1}: {e}")
                        continue

            print("SQL script 'nonameyet.sql' executed successfully. All statements processed.")

    except Error as e:
        print("Error while connecting to MariaDB", e)
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("MariaDB connection is closed")


create_connection()
