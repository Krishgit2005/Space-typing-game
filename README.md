# Space Typing Game

A lightweight Flask web game that tests your typing speed and accuracy while dodging falling words in a space-themed environment.

## 🚀 Setup (Quick Start)

1) Install Flask:

```powershell
python -m pip install flask
```

2) Run the server:

```powershell
python ship.py
```

3) Open the game in your browser:

- Main menu: `http://127.0.0.1:5000/`
- Game screen: `http://127.0.0.1:5000/game`

## 🎮 How to Play

- Choose a difficulty.
- Type the falling words.
- Press **Enter** or **Space** to fire when the word matches.
- Lose a life if a word reaches the bottom line.
- The game ends when lives reach zero or the timer runs out.

## 📁 Project Structure

- `ship.py` — Flask server
- `templates/` — HTML pages
- `static/` — images, GIFs, and audio assets

## 📌 Notes

- Assets are served from `/static/`.
- The game uses p5.js in the browser.
  Addeing feature of multiplayers.
