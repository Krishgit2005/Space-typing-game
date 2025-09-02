from flask import Flask, render_template, redirect, url_for
import subprocess
import os

app = Flask(__name__)

game_script = 'space.py'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start-game')
def start_game():
    try:
        if os.name == 'nt':  # Windows
            subprocess.Popen(['python', game_script], creationflags=subprocess.CREATE_NO_WINDOW)
        else:  # Mac/Linux 
            subprocess.Popen(['python3', game_script])
    except Exception as e:
        return f"Error starting game: {e}"
    return redirect(url_for('game_result'))

@app.route('/game-result')
def game_result():
    result = "Game Over! No score available."
    if os.path.exists('game_result.txt'):
        with open('game_result.txt', 'r') as file:
            result = file.read().strip()
    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
