import mysql.connector
import bcrypt

# Database connection information
db_config = {
    'user': 'root',
    'password': 'nguyen12',
    'host': 'localhost',
    'database': 'nonameyet'
}

# Admin credentials
admin_username = 'admin'
admin_password = 'admin123'

hashed_password = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt())

try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = %s", (admin_username,))
    if cursor.fetchone():
        print("Admin user already exists.")
    else:
        cursor.execute("INSERT INTO users (username, hashed_password) VALUES (%s, %s)", (admin_username, hashed_password.decode('utf-8')))
        conn.commit()
        print("Admin user created successfully.")

except mysql.connector.Error as err:
    print("Database error:", err)
finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
