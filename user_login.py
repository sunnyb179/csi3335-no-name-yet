from flask import Flask, request, jsonify, session
import bcrypt
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="nguyen12",
        database="nonameyet"
    )
    return conn

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password'].encode('utf-8')

    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    if cursor.fetchone():
        return jsonify({'message': 'Username already exists'}), 409

    cursor.execute("INSERT INTO users (username, hashed_password) VALUES (%s, %s)", (username, hashed_password.decode('utf-8')))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password'].encode('utf-8')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT hashed_password FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user and bcrypt.checkpw(password, user[0].encode('utf-8')):
        session['user'] = username
        return jsonify({'message': 'Logged in successfully'}), 200
    else:
        return jsonify({'message': 'Wrong username or password'}), 401

if __name__ == '__main__':
    app.run(debug=True)
