from flask import Flask, request, jsonify, session, render_template, redirect, url_for
import bcrypt
import mysql.connector
from connectionDictionary import mysql as db_config

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def home():
    return render_template('home.html')
def get_db_connection():
    conn = mysql.connector.connect(
        host=db_config['location'],
        user=db_config['user'],
        password=db_config['password'],
        database="nonameyet"
    )
    return conn

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
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

        return render_template('login.html', message='User registered successfully.')
    else:
        return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT hashed_password FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and bcrypt.checkpw(password, user[0].encode('utf-8')):
            session['user'] = username
            if username == 'admin':
                return redirect(url_for('admin'))
            return redirect(url_for('select_team'))
        else:
            return render_template('login.html', error='Wrong username or password')
    else:
        return render_template('login.html')


@app.route('/select_team', methods=['GET'])
def select_team():
    if 'user' not in session:
        return jsonify({'message': 'You need to login first'}), 401

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT name FROM teams ORDER BY name")
    teams = cursor.fetchall()
    cursor.execute("SELECT DISTINCT yearID FROM teams ORDER BY yearID DESC")
    years = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('select_team.html', teams=teams, years=years)


@app.route('/team_roster', methods=['GET'])
def team_roster():
    if 'user' not in session:
        return jsonify({'message': 'You need to login first'}), 401

    team_name = request.args.get('team_name')
    year = int(request.args.get('year'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
           INSERT INTO user_selections (username, team_name, year, timestamp)
           VALUES (%s, %s, %s, NOW())
       """, (session['user'], team_name, year))
    conn.commit()

    cursor.execute("""
        SELECT DISTINCT p.playerid, p.nameFirst, p.nameLast, b.AB, b.H, b.BB, b.SO, b.2B, b.3B, b.HR,
               f.POS, f.G
        FROM batting b
        JOIN people p ON b.playerID = p.playerID
        JOIN teams t ON b.teamID = t.teamID
        JOIN fielding f ON f.playerID = p.playerID AND f.yearID = b.yearID AND f.teamID = b.teamID
        WHERE t.name = %s AND b.yearID = %s
        ORDER BY p.nameLast, p.nameFirst, f.POS
    """, (team_name, year))

    batting_stats = []
    for record in cursor.fetchall():
        player_id = record[0]
        name = f"{record[1]} {record[2]}"
        at_bats = int(record[3])
        hits = int(record[4])
        walks = int(record[5])
        strikeouts = int(record[6])
        doubles = int(record[7])
        triples = int(record[8])
        home_runs = int(record[9])
        position = record[10]
        games_at_position = int(record[11])

        avg = round(hits / at_bats, 3) if at_bats > 0 else 0
        obp = round((hits + walks) / (at_bats + walks) if at_bats + walks > 0 else 0, 3)
        slg = round((hits + doubles * 2 + triples * 3 + home_runs * 4) / at_bats if at_bats > 0 else 0, 3)

        batting_stats.append({
            'player_id': player_id,
            'name': name,
            'position': position,
            'games': games_at_position,
            'avg': f"{avg:.3f}",
            'obp': f"{obp:.3f}",
            'slg': f"{slg:.3f}"
        })


    cursor.execute("""
            SELECT DISTINCT p.playerid, p.nameFirst, p.nameLast, pi.G, pi.GS, pi.IPouts/3 as IP, pi.H, pi.BB, pi.SO
            FROM pitching pi
            JOIN people p ON pi.playerID = p.playerID
            JOIN teams t ON t.teamID = pi.teamID
            WHERE t.name = %s AND pi.yearID = %s
        """, (team_name, year))
    pitchers = cursor.fetchall()

    pitching_stats = []
    for pitcher in pitchers:
        player_id = pitcher[0]
        name = f"{pitcher[1]} {pitcher[2]}"
        games = int(pitcher[3])
        games_started = int(pitcher[4])
        innings_pitched = float(pitcher[5])
        hits = int(pitcher[6])
        walks = int(pitcher[7])
        strikeouts = int(pitcher[8])

        whip = (hits + walks) / innings_pitched if innings_pitched else 0
        k_per_9 = (strikeouts * 9) / innings_pitched if innings_pitched else 0

        pitching_stats.append({
            'player_id': player_id,
            'name': name,
            'games': games,
            'games_started': games_started,
            'innings_pitched': innings_pitched,
            'whip': f"{whip:.2f}",
            'k_per_9': f"{k_per_9:.2f}"
        })

    cursor.close()
    conn.close()

    return render_template('team_roster.html', batting_stats=batting_stats, pitching_stats=pitching_stats,
                           team_name=team_name, year=year)


@app.route('/admin', methods=['GET'])
def admin():
    if 'user' not in session:
        return jsonify({'message': 'You need to login first'}), 401

    if session['user'] != 'admin':
        return jsonify({'message': 'Unauthorized'}), 403

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_selections")
    user_logs = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM user_selections")
    total_requests = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return render_template('admin.html', user_logs=user_logs, total_requests=total_requests)


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/player_stats/<player_id>')
def player_stats(player_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DISTINCT p.nameFirst, p.nameLast, b.yearID, t.name, b.G, b.AB, b.H, b.HR, b.RBI
        FROM batting b
        JOIN people p ON b.playerID = p.playerID
        JOIN teams t ON b.teamID = t.teamID
        WHERE b.playerID = %s
        ORDER BY b.yearID ASC
    """, (player_id,))
    stats = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('player_stats.html', stats=stats, player_name=stats[0][0] + ' ' + stats[0][1] if stats else 'Unknown Player')


if __name__ == '__main__':
    app.run(debug=True)