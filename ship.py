from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

# Word list
words = ['Apple', 'Journey', 'Window', 'Blue', 'Mountain', 'Happy', 'Sunshine', 'River', 'Cloud', 'Garden']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game')
def game():
    return render_template('index1.html')

@app.route('/get_word')
def get_word():
    return jsonify({'word': random.choice(words)})

@app.route('/submit_score', methods=['POST'])
def submit_score():
    data = request.json
    score = data.get('score', 0)
    with open('game_result.txt', 'w') as file:
        file.write(f"Game Over! Your Score: {score}")
    return jsonify({'message': 'Score saved'})

if __name__ == '__main__':
    app.run(debug=True)