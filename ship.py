from flask import Flask, render_template, jsonify, request, session, redirect, url_for, flash
import random
import os
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'super_secret_space_key_999'

DATABASE = 'database.db'

def init_db():
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                high_score INTEGER DEFAULT 0
            )
        ''')
        conn.commit()
        conn.close()

init_db()

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Word list
words = ['Apple', 'Journey', 'Window', 'Blue', 'Mountain', 'Happy', 'Sunshine', 'River', 'Cloud', 'Garden']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        
        if user:
            flash('Username already exists.')
            conn.close()
            return redirect(url_for('register'))
            
        password_hash = generate_password_hash(password)
        conn.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, password_hash))
        conn.commit()
        conn.close()
        
        flash('Registration successful, please login.')
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/game')
def game():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index1.html')

@app.route('/get_word')
def get_word():
    return jsonify({'word': random.choice(words)})

@app.route('/submit_score', methods=['POST'])
def submit_score():
    data = request.json
    score = data.get('score', 0)
    
    if 'user_id' in session:
        conn = get_db_connection()
        user = conn.execute('SELECT high_score FROM users WHERE id = ?', (session['user_id'],)).fetchone()
        if user and score > dict(user).get('high_score', 0):
            conn.execute('UPDATE users SET high_score = ? WHERE id = ?', (score, session['user_id']))
            conn.commit()
            
        # Refetch all users to respond with leaderboard
        users = conn.execute('SELECT username, high_score FROM users ORDER BY high_score DESC LIMIT 10').fetchall()
        conn.close()
        
        scores = [{'name': u['username'], 'score': u['high_score']} for u in users]
        return jsonify({'message': 'Score saved', 'scores': scores})
        
    return jsonify({'message': 'Unauthorized', 'scores': []}), 401

@app.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    conn = get_db_connection()
    users = conn.execute('SELECT username, high_score FROM users ORDER BY high_score DESC LIMIT 10').fetchall()
    conn.close()
    
    scores = [{'name': user['username'], 'score': user['high_score']} for user in users]
    return jsonify({'scores': scores})

if __name__ == '__main__':
    app.run(debug=True)