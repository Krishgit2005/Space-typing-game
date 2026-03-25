import os

base_dir = r"C:\Users\krishdavane\.gemini\antigravity\scratch\Space-typing-game\templates"

# Patch index1.html
with open(os.path.join(base_dir, "index1.html"), "r", encoding="utf-8") as f:
    content = f.read()

# Replace head / style
old_head = """    <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.4.0/p5.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.4.0/addons/p5.sound.min.js"></script>
    <style>
        body {
            position: relative;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            min-height: 100vh;
            width: 100vw;
            margin: 0;
            padding: 0;
            background: url('static/outer-space-cosmos-stars-background-600nw-2153688383.webp') no-repeat center center fixed;
            background-size: cover;
            color: #fff;
            font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
            font-size: 22px;
            text-align: center;
            overflow: hidden;
        }"""
new_head = """    <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.4.0/p5.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.4.0/addons/p5.sound.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800&family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <style>
        body {
            position: relative;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            min-height: 100vh;
            width: 100vw;
            margin: 0;
            padding: 0;
            background-color: #0b0c10;
            background-image: 
                radial-gradient(circle at 15% 50%, rgba(0, 242, 254, 0.15), transparent 40%),
                radial-gradient(circle at 85% 30%, rgba(255, 69, 0, 0.15), transparent 40%),
                url('static/outer-space-cosmos-stars-background-600nw-2153688383.webp');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            color: #fff;
            font-family: 'Inter', sans-serif;
            font-size: 22px;
            text-align: center;
            overflow: hidden;
        }"""
content = content.replace(old_head, new_head)

# Replace body::before, canvas, modal, lasers, explosions
old_body_before = """        body::before {
            content: "";
            position: fixed;
            inset: 0;
            background: rgba(0, 0, 0, 0.55);
            z-index: 0;
            pointer-events: none;
        }
        canvas {
            display: block;
            margin: 0 auto;
            border-radius: 18px;
            box-shadow: 0 18px 50px rgba(0, 0, 0, 0.6);
            z-index: 1;
        }"""
new_body_before = """        body::before {
            content: "";
            position: fixed;
            inset: 0;
            background: rgba(10, 10, 18, 0.5);
            backdrop-filter: blur(4px);
            z-index: 0;
            pointer-events: none;
        }
        canvas {
            display: block;
            margin: 0 auto;
            border-radius: 20px;
            box-shadow: 0 0 30px rgba(0, 242, 254, 0.2), inset 0 0 15px rgba(0, 242, 254, 0.1);
            border: 2px solid rgba(0, 242, 254, 0.3);
            z-index: 1;
        }"""
content = content.replace(old_body_before, new_body_before)

old_modal = """        .modal {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0, 0, 0, 0.85);
            padding: 26px 28px;
            border-radius: 16px;
            text-align: center;
            display: flex;
            flex-direction: column;
            align-items: center;
            width: min(420px, 90vw);
            box-shadow: 0 16px 40px rgba(0, 0, 0, 0.65);
            border: 2px solid rgba(255, 255, 255, 0.25);
            z-index: 2;
        }
        .modal h2 {
            margin: 0 0 14px;
            font-size: 2.2rem;
        }
        .modal button {
            font-size: 20px;
            padding: 12px 22px;
            margin: 10px 0;
            cursor: pointer;
            border: 2px solid rgba(255, 255, 255, 0.4);
            border-radius: 12px;
            color: white;
            width: 90%;
            max-width: 260px;
            transition: transform 0.15s ease, background 0.15s ease;
        }
        .modal button:hover {
            transform: translateY(-2px);
            opacity: 0.95;
        }
        .modal button:active {
            transform: translateY(1px);
        }
        .easy { background-color: #2BBE2B; }
        .medium { background-color: #F09C00; }
        .hard { background-color: #E23C3C; }"""
new_modal = """        .modal {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(20, 20, 30, 0.6);
            backdrop-filter: blur(12px);
            padding: 30px 40px;
            border-radius: 20px;
            text-align: center;
            display: flex;
            flex-direction: column;
            align-items: center;
            width: min(420px, 90vw);
            box-shadow: 0 10px 40px rgba(0, 242, 254, 0.2);
            border: 2px solid rgba(0, 242, 254, 0.3);
            z-index: 2;
        }
        .modal h2 {
            font-family: 'Orbitron', sans-serif;
            margin: 0 0 20px;
            font-size: 2.2rem;
            color: #fff;
            text-transform: uppercase;
            text-shadow: 0 0 15px #00f2fe;
            letter-spacing: 2px;
        }
        .modal button {
            font-family: 'Orbitron', sans-serif;
            font-size: 18px;
            font-weight: 600;
            padding: 14px 24px;
            margin: 10px 0;
            cursor: pointer;
            border: none;
            border-radius: 12px;
            color: white;
            width: 100%;
            max-width: 260px;
            transition: all 0.2s ease;
            text-transform: uppercase;
            letter-spacing: 1.5px;
        }
        .easy { background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); box-shadow: 0 0 15px rgba(56, 239, 125, 0.4); }
        .medium { background: linear-gradient(135deg, #f2994a 0%, #f2c94c 100%); box-shadow: 0 0 15px rgba(242, 153, 74, 0.4); }
        .hard { background: linear-gradient(135deg, #ed213a 0%, #93291e 100%); box-shadow: 0 0 15px rgba(237, 33, 58, 0.4); }
        .modal button:hover {
            transform: translateY(-3px);
            filter: brightness(1.1);
        }
        .modal button:active {
            transform: translateY(1px);
        }"""
content = content.replace(old_modal, new_modal)

old_go = """        .game-over-container {
            display: none;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
            margin-bottom: 5px;
            padding: 26px 28px;
            background: rgba(0, 0, 0, 0.9);
            border-radius: 18px;
            border: 2px solid rgba(255, 255, 255, 0.3);
            box-shadow: 0 16px 36px rgba(0, 0, 0, 0.65);
            z-index: 2;
            min-width: 320px;
        }
        .game-over-container h1 {
            margin: 0 0 10px;
            font-size: 2.6rem;
        }
        .game-over-container p {
            margin: 0;
            font-size: 1.5rem;
        }
        .game-over-buttons {
            display: flex;
            gap: 18px;
            margin-top: 16px;
        }
        .game-over-buttons button {
            font-size: 18px;
            padding: 12px 20px;
            cursor: pointer;
            border: none;
            border-radius: 10px;
            min-width: 140px;
            transition: transform 0.15s ease;
        }
        .game-over-buttons button:hover {
            transform: translateY(-1px);
        }
        .try-again {
            background-color: #4CAF50;
            color: white;
        }
        .exit {
            background-color: #f44336;
            color: white;
        }"""
new_go = """        .game-over-container {
            display: none;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
            margin-bottom: 5px;
            padding: 30px 40px;
            background: rgba(20, 20, 30, 0.7);
            backdrop-filter: blur(15px);
            border-radius: 20px;
            border: 2px solid rgba(255, 69, 0, 0.5);
            box-shadow: 0 10px 40px rgba(255, 69, 0, 0.3);
            z-index: 2;
            min-width: 340px;
        }
        .game-over-container h1 {
            font-family: 'Orbitron', sans-serif;
            margin: 0 0 15px;
            font-size: 3rem;
            color: #ff4d4d;
            text-shadow: 0 0 20px #ff0000, 0 0 40px #ff0000;
            letter-spacing: 3px;
        }
        .game-over-container p {
            margin: 0;
            font-size: 1.8rem;
            font-family: 'Orbitron', sans-serif;
            color: #00f2fe;
            text-shadow: 0 0 10px #00f2fe;
        }
        .game-over-buttons {
            display: flex;
            gap: 18px;
            margin-top: 25px;
        }
        .game-over-buttons button {
            font-family: 'Orbitron', sans-serif;
            font-size: 16px;
            font-weight: 600;
            padding: 12px 24px;
            cursor: pointer;
            border: none;
            border-radius: 12px;
            min-width: 140px;
            transition: all 0.2s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: white;
        }
        .try-again {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            box-shadow: 0 0 15px rgba(56, 239, 125, 0.4);
        }
        .exit {
            background: linear-gradient(135deg, #434343 0%, #000000 100%);
            box-shadow: 0 0 15px rgba(67, 67, 67, 0.4);
            border: 1px solid #444;
        }
        .game-over-buttons button:hover {
            transform: translateY(-3px);
            filter: brightness(1.1);
        }"""
content = content.replace(old_go, new_go)

# Adding textFont('Orbitron');
content = content.replace("rocketX = width / 2;\n            textSize(24);", "rocketX = width / 2;\n            textFont('Orbitron');\n            textSize(24);")

# Replacing lasers
old_draw_fx = """            for (let i = lasers.length - 1; i >= 0; i--) {
                stroke(255, 0, 0);
                strokeWeight(4);
                drawingContext.shadowBlur = 15;
                drawingContext.shadowColor = 'red';
                line(lasers[i].x1, lasers[i].y1, lasers[i].x2, lasers[i].y2);
                strokeWeight(1);
                drawingContext.shadowBlur = 0;
                lasers[i].lifetime--;
                if (lasers[i].lifetime <= 0) lasers.splice(i, 1);
            }
            
            for (let i = explosions.length - 1; i >= 0; i--) {
                drawingContext.shadowBlur = 20;
                drawingContext.shadowColor = 'orange';
                fill(255, 165, 0, explosions[i].lifetime * 12);
                circle(explosions[i].x, explosions[i].y, 50);
                drawingContext.shadowColor = 'red';
                fill(255, 0, 0, explosions[i].lifetime * 12);
                circle(explosions[i].x, explosions[i].y, 30);
                drawingContext.shadowBlur = 0;
                explosions[i].lifetime--;
                if (explosions[i].lifetime <= 0) explosions.splice(i, 1);
            }"""
new_draw_fx = """            for (let i = lasers.length - 1; i >= 0; i--) {
                stroke(0, 242, 254);
                strokeWeight(5);
                drawingContext.shadowBlur = 20;
                drawingContext.shadowColor = '#00f2fe';
                line(lasers[i].x1, lasers[i].y1, lasers[i].x2, lasers[i].y2);
                stroke(255);
                strokeWeight(2);
                line(lasers[i].x1, lasers[i].y1, lasers[i].x2, lasers[i].y2);
                strokeWeight(1);
                drawingContext.shadowBlur = 0;
                lasers[i].lifetime--;
                if (lasers[i].lifetime <= 0) lasers.splice(i, 1);
            }
            
            for (let i = explosions.length - 1; i >= 0; i--) {
                drawingContext.shadowBlur = 20;
                drawingContext.shadowColor = '#00f2fe';
                noFill();
                stroke(0, 242, 254, explosions[i].lifetime * 12);
                strokeWeight(3);
                let radius = 60 - explosions[i].lifetime * 2;
                circle(explosions[i].x, explosions[i].y, radius);
                
                drawingContext.shadowColor = '#fff';
                stroke(255, 255, 255, explosions[i].lifetime * 12);
                strokeWeight(1);
                circle(explosions[i].x, explosions[i].y, radius - 10);
                
                noStroke();
                drawingContext.shadowBlur = 0;
                explosions[i].lifetime--;
                if (explosions[i].lifetime <= 0) explosions.splice(i, 1);
            }"""
content = content.replace(old_draw_fx, new_draw_fx)

old_text = """                if (userInput.length > 0 && wordText.toLowerCase().startsWith(userInput.toLowerCase())) {
                    let typedPart = wordText.substring(0, userInput.length);
                    let restPart = wordText.substring(userInput.length);
                    
                    fill(0, 255, 0);
                    drawingContext.shadowColor = 'lime';
                    text(typedPart, words[i].x, words[i].y);
                    
                    fill(255);
                    drawingContext.shadowColor = 'white';
                    text(restPart, words[i].x + textWidth(typedPart), words[i].y);
                } else {
                    fill(255);
                    text(wordText, words[i].x, words[i].y);
                }"""
new_text = """                if (userInput.length > 0 && wordText.toLowerCase().startsWith(userInput.toLowerCase())) {
                    let typedPart = wordText.substring(0, userInput.length);
                    let restPart = wordText.substring(userInput.length);
                    
                    fill('#00f2fe');
                    drawingContext.shadowColor = '#00f2fe';
                    text(typedPart, words[i].x, words[i].y);
                    
                    fill(255);
                    drawingContext.shadowColor = 'white';
                    text(restPart, words[i].x + textWidth(typedPart), words[i].y);
                } else {
                    fill(255);
                    text(wordText, words[i].x, words[i].y);
                }"""
content = content.replace(old_text, new_text)

with open(os.path.join(base_dir, "index1.html"), "w", encoding="utf-8") as f:
    f.write(content)

# Patch login overviews
pages = ["login.html", "register.html"]
for p in pages:
    with open(os.path.join(base_dir, p), "r", encoding="utf-8") as f:
        html = f.read()
    
    col = "FF4500" if p == "login.html" else "008CBA"
    hov = "E03E00" if p == "login.html" else "007B9A"
    
    old_sty = f'''    <style>
        body {{
            background-image: url("{{{{ url_for('static', filename='outer-space-cosmos-stars-background-600nw-2153688383.webp') }}}}");
            background-size: cover;
            color: white; font-family: "Segoe UI", sans-serif;
            text-align: center; margin: 0; min-height: 100vh;
            display: flex; justify-content: center; align-items: center;
        }}
        .container {{
            background: rgba(0,0,0,0.8); padding: 40px; border-radius: 12px;
            border: 2px solid rgba(255,255,255,0.3); width: 300px;
        }}
        input {{
            width: 90%; padding: 10px; margin: 10px 0; border-radius: 5px; border: none; font-size: 16px;
        }}
        button {{
            padding: 10px 20px; font-size: 18px; border-radius: 5px;
            border: none; background: #{col}; color: white; cursor: pointer;
            width: 100%; margin-top: 15px;
        }}
        button:hover {{ background: #{hov}; }}
        .flash {{ color: #ffeb3b; margin-bottom: 10px; }}
        a {{ color: #4CAF50; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
    </style>'''
    
    new_sty = f'''    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800&family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <style>
        body {{
            background-color: #0b0c10;
            background-image: 
                radial-gradient(circle at 15% 50%, rgba(0, 242, 254, 0.15), transparent 40%),
                radial-gradient(circle at 85% 30%, rgba(255, 69, 0, 0.15), transparent 40%),
                url("{{{{ url_for('static', filename='outer-space-cosmos-stars-background-600nw-2153688383.webp') }}}}");
            background-size: cover; background-position: center; background-attachment: fixed;
            color: white; font-family: 'Inter', sans-serif;
            text-align: center; margin: 0; min-height: 100vh;
            display: flex; justify-content: center; align-items: center;
        }}
        body::before {{
            content: ""; position: fixed; inset: 0;
            background: rgba(10, 10, 18, 0.6); backdrop-filter: blur(4px);
            z-index: 0; pointer-events: none;
        }}
        .container {{
            background: rgba(30, 30, 40, 0.3); backdrop-filter: blur(12px);
            padding: 40px; border-radius: 20px;
            border: 2px solid rgba(0, 242, 254, 0.3); width: 320px;
            box-shadow: 0 4px 30px rgba(0, 242, 254, 0.15); z-index: 1;
        }}
        h2 {{ font-family: 'Orbitron', sans-serif; text-transform: uppercase; letter-spacing: 2px; text-shadow: 0 0 10px #00f2fe; margin-top: 0; }}
        input {{
            width: 90%; padding: 12px; margin: 10px 0; border-radius: 10px; border: 1px solid rgba(255,255,255,0.2); 
            background: rgba(0,0,0,0.4); color: white; font-size: 16px; transition: all 0.2s ease;
        }}
        input:focus {{ outline: none; border-color: #00f2fe; box-shadow: 0 0 10px rgba(0,242,254,0.3); }}
        button {{
            font-family: 'Orbitron', sans-serif; padding: 12px 20px; font-size: 16px; font-weight: 600;
            border-radius: 10px; border: none; 
            background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
            color: white; cursor: pointer; width: 100%; margin-top: 15px; margin-bottom: 15px;
            box-shadow: 0 0 15px rgba(0, 242, 254, 0.4); transition: all 0.2s ease; text-transform: uppercase; letter-spacing: 1.5px;
        }}
        button:hover {{ transform: translateY(-3px); box-shadow: 0 0 25px rgba(255, 255, 255, 0.3), 0 0 15px rgba(0, 242, 254, 0.6); }}
        button:active {{ transform: translateY(1px); }}
        .flash {{ color: #ffeb3b; margin-bottom: 15px; }}
        a {{ color: #00f2fe; text-decoration: none; font-weight: 600; transition: color 0.2s; }}
        a:hover {{ color: #fff; text-shadow: 0 0 10px #00f2fe; text-decoration: none; }}
        p {{ font-size: 14px; color: #ddd; }}
    </style>'''
    
    html = html.replace(old_sty, new_sty)
    with open(os.path.join(base_dir, p), "w", encoding="utf-8") as f:
        f.write(html)
