import mysql.connector

mysql_dict = {
    'host': 'localhost',
    'user': 'root',
    'password': 'nguyen12',
    'database': 'nonameyet'
}

def get_db_connection():
    conn = mysql.connector.connect(
        host=mysql_dict['host'],
        user=mysql_dict['user'],
        password=mysql_dict['password'],
        database=mysql_dict['database']
    )
    return conn