let words = [];
let userInput = "";
let score = 0;
let lives = 5;
let explosions = [];
let lasers = [];
let rocketFlames;
let rocketX;
let gameOver = false;
let scoreSubmitted = false;
let timer = 300; // 5 minutes standard
let timerInterval;
let wordSpawnRate = 3000;
let speed = 0.5;
let targetX = null;
let borderY = 450;
let rocketY = 500;
let rocketWidth = 350;
let rocketHeight = 320;
let spaceBg;
let backspaceInterval = null;
let backspaceDelay = 300;
let backspaceSpeed = 100;
let currentDifficulty = "easy";

let gameStartTime = null;
let wordsTyped = 0;          
let totalCharsTyped = 0;     
let totalCharsCorrect = 0;
let wpmTimeline = [];        
let wpmSnapshotInterval = null;
let lastSnapshotWordsTyped = 0;
let lastSnapshotTime = 0;

let menuMusic;
let gameMusic;
let gameOverSound;
let explosionSound;
let currentAudio = null;

let wordSpawnTimeout = null;
let freezeTimer = 0;
let bossActive = false;
let bossEntity = null;
let wordsClearedSinceBoss = 0;

const wordsShort = ["chair", "table", "lamp", "sofa", "broom", "dish", "spoon", "apple", "milk", "bread", "water", "juice", "shirt", "pants", "socks", "dress", "shoes", "hat", "scarf", "belt", "tree", "grass", "cloud", "river", "sun", "moon", "star", "rain", "car", "bike", "bus", "train", "plane", "taxi", "boat"];
const wordsMedium = ["blanket", "pillow", "mirror", "banana", "coffee", "cookie", "jacket", "gloves", "flower", "mountain", "scooter", "subway"];
const wordsLong = ["sunshine", "journey", "window", "garden", "beautiful", "adventure", "spaceship", "universe", "galaxies", "asteroid", "telescope"];
const powerUpTypes = ["emp", "freeze", "shield"];

function preload() {
    rocketFlames = loadImage('static/igor-schteinberg-cartoon-rocke-unscreen.gif');
    spaceBg = loadImage('static/supawork-d6eaa225fbe34a529710cb81ab131702.gif');
    menuMusic = loadSound('static/space-chords-loop-310493.mp3');
    gameMusic = loadSound('static/star-wars-style-battle-music-148641.mp3');
    gameOverSound = loadSound('static/mario_world_ending.mp3');
    explosionSound = loadSound('static/laser-gun-105781.mp3');
}

function setup() {
    let cnv = createCanvas(800, 600);
    cnv.id('p5-game-canvas');
    cnv.parent(document.body);
    cnv.style('display', 'none');
    cnv.style('margin', 'auto');
    rocketX = width / 2;
    textFont('Orbitron');
    textSize(24);
    window.addEventListener('keydown', function(e) {
        if(e.keyCode == 32 && e.target == document.body) {
            e.preventDefault();
        }
    });

    let mod = document.getElementById("difficulty-modal");
    if(mod) {
        mod.innerHTML = `
            <h2>Choose Difficulty</h2>
            <button class="easy" onclick="startGame('easy')">Easy</button>
            <button class="medium" onclick="startGame('medium')">Medium</button>
            <button class="hard" onclick="startGame('hard')">Hard</button>
        `;
    }
}



function startGame(difficulty) {
    if (typeof userStartAudio === 'function') userStartAudio();
    currentDifficulty = difficulty;
    let mod = document.getElementById("difficulty-modal");
    if(mod) mod.style.display = "none";
    let cnv = document.getElementById("p5-game-canvas");
    if(cnv) cnv.style.display = "block";

    if (currentAudio) currentAudio.stop();
    gameMusic.loop();
    currentAudio = gameMusic;

    // Reset game state
    words = [];
    score = 0;
    lives = 5;
    gameOver = false;
    scoreSubmitted = false;
    timer = 180;
    userInput = "";
    freezeTimer = 0;
    bossActive = false;
    bossEntity = null;
    wordsClearedSinceBoss = 0;

    // Reset WPM tracking
    wordsTyped = 0;
    totalCharsTyped = 0;
    totalCharsCorrect = 0;
    wpmTimeline = [];
    lastSnapshotWordsTyped = 0;
    lastSnapshotTime = 0;
    gameStartTime = Date.now();

    if (difficulty === "easy") {
        wordSpawnRate = 3000;
        speed = 0.3;
    } else if (difficulty === "medium") {
        wordSpawnRate = 2500;
        speed = 0.5;
    } else if (difficulty === "hard") {
        wordSpawnRate = 2000;
        speed = 0.8;
    }

    clearInterval(timerInterval);
    if(wordSpawnTimeout) clearTimeout(wordSpawnTimeout);
    scheduleNextWord();
    timerInterval = setInterval(updateTimer, 1000);

    // WPM snapshot every 5 seconds
    if (wpmSnapshotInterval) clearInterval(wpmSnapshotInterval);
    wpmSnapshotInterval = setInterval(takeWpmSnapshot, 5000);
}

function scheduleNextWord() {
    if (gameOver) return;
    spawnWord();
    let elapsedSec = gameStartTime ? Math.floor((Date.now() - gameStartTime) / 1000) : 0;
    let tier = Math.floor(elapsedSec / 15);
    let currentSpawnRate = wordSpawnRate * Math.pow(0.85, tier);
    currentSpawnRate = Math.max(currentSpawnRate, 800); // Floor cap
    if(bossActive) currentSpawnRate = 4000;

    wordSpawnTimeout = setTimeout(scheduleNextWord, currentSpawnRate);
}

function spawnBoss() {
    bossActive = true;
    wordsClearedSinceBoss = 0;
    bossEntity = {
        words: [
            wordsMedium[Math.floor(Math.random() * wordsMedium.length)],
            wordsLong[Math.floor(Math.random() * wordsLong.length)],
            wordsLong[Math.floor(Math.random() * wordsLong.length)]
        ],
        currentWordIdx: 0,
        y: -150,
        x: width/2,
        speed: speed * 0.4
    };
}

function spawnWord() {
    if (bossActive) return;

    if (wordsClearedSinceBoss >= 15 && currentDifficulty !== "easy") {
        spawnBoss();
        return;
    }

    let elapsedSec = gameStartTime ? Math.floor((Date.now() - gameStartTime) / 1000) : 0;
    let tier = Math.floor(elapsedSec / 20);
    


    let listToUse = wordsShort;
    if (tier === 1) {
        listToUse = Math.random() > 0.4 ? wordsShort : wordsMedium;
    } else if (tier >= 2) {
        let r = Math.random();
        if (r < 0.2) listToUse = wordsLong;
        else if (r < 0.6) listToUse = wordsMedium;
        else listToUse = wordsShort;
    }

    const randomWord = listToUse[Math.floor(Math.random() * listToUse.length)];
    let wordWidth = textWidth(randomWord);
    let minX = 40;
    let maxX = width - wordWidth - 40;
    if (maxX < minX) return;
    
    let currentSpeed = speed * (1.0 + (tier * 0.2));
    
    let wType = 'normal';
    if(Math.random() < 0.1) {
        wType = powerUpTypes[Math.floor(Math.random() * powerUpTypes.length)];
    }

    words.push({ text: randomWord, x: random(minX, maxX), y: -20, speed: currentSpeed, type: wType });
}

// ── WPM helpers ──
function getCurrentWpm() {
    if (!gameStartTime) return 0;
    let elapsedMinutes = (Date.now() - gameStartTime) / 60000;
    if (elapsedMinutes < 0.001) return 0;
    return Math.round(wordsTyped / elapsedMinutes);
}

function takeWpmSnapshot() {
    if (gameOver || !gameStartTime) return;
    let elapsed = (Date.now() - gameStartTime) / 1000;
    let wpm = getCurrentWpm();
    wpmTimeline.push({ time: Math.round(elapsed), wpm: wpm });
    lastSnapshotWordsTyped = wordsTyped;
    lastSnapshotTime = elapsed;
}

function getAccuracy() {
    if (totalCharsTyped === 0) return 100;
    return Math.round((totalCharsCorrect / totalCharsTyped) * 100);
}

function getPeakWpm() {
    if (wpmTimeline.length === 0) return getCurrentWpm();
    return Math.max(...wpmTimeline.map(p => p.wpm), getCurrentWpm());
}

function draw() {
    background(spaceBg);
    image(rocketFlames, rocketX - 175, rocketY - 110, rocketWidth, rocketHeight);
    stroke(255, 0, 0);
    line(0, borderY, width, borderY);
    noStroke();

    if (gameOver) {
        if (!scoreSubmitted) {
            scoreSubmitted = true;
            clearInterval(timerInterval);
            clearInterval(wpmSnapshotInterval);
            if(wordSpawnTimeout) clearTimeout(wordSpawnTimeout);

            takeWpmSnapshot();
            let finalWpm = getCurrentWpm();
            let accuracy = getAccuracy();
            let peakWpm = getPeakWpm();

            document.getElementById("game-over-container").style.display = "flex";
            document.getElementById("final-score").innerText = `Score: ${score} words`;
            document.getElementById("final-wpm").innerText = finalWpm;
            document.getElementById("final-accuracy").innerText = accuracy + "%";
            document.getElementById("peak-wpm").innerText = peakWpm;

            setTimeout(() => drawWpmChart(), 100);

            fetch('/submit_score', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ score: score })
            })
            .then(r => r.json())
            .then(data => {
                let lbList = document.getElementById("leaderboard-list");
                lbList.innerHTML = '';
                if(data.scores && data.scores.length > 0) {
                    data.scores.forEach(s => {
                        let li = document.createElement('li');
                        li.innerText = `${s.name}: ${s.score}`;
                        lbList.appendChild(li);
                    });
                } else {
                    lbList.innerHTML = '<li>No scores yet!</li>';
                }
            })
            .catch(err => console.error(err));

            fetch('/submit_wpm', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ wpm: finalWpm, accuracy: accuracy, difficulty: currentDifficulty, words_typed: wordsTyped })
            }).catch(err => console.error(err));

            if (currentAudio !== gameOverSound) {
                if (currentAudio) currentAudio.stop();
                gameOverSound.play();
                currentAudio = gameOverSound;
            }
        }
        return;
    }

    // ── HUD ──
    let liveWpm = getCurrentWpm();
    fill(255);
    textSize(20);
    textAlign(LEFT);
    text(`Score: ${score}`, 10, 30);
    text(`Lives: ${"❤️".repeat(lives)}`, 10, 60);
    text(`Type: ${userInput}`, 10, 90);
    text(`Time: ${timer}s`, 10, 120);
    if(freezeTimer > 0) {
        fill('#00f2fe');
        text(`Freeze: ${freezeTimer}s`, 10, 150);
    }
    
    drawWpmBadge(liveWpm);

    if (targetX !== null) {
        if (abs(rocketX - targetX) < 2) {
            rocketX = targetX;
            targetX = null;
        } else {
            rocketX += (targetX - rocketX) * 0.1; // Smooth movement
        }
    } else {
        // Return to center
        if (abs(rocketX - width/2) > 2) {
            rocketX += (width/2 - rocketX) * 0.05;
        }
    }

    // Freeze logic multiplier
    let currentSpeedMult = freezeTimer > 0 ? 0.3 : 1.0;

    // Draw Boss
    if (bossActive && bossEntity) {
        bossEntity.y += bossEntity.speed * currentSpeedMult;
        
        // draw boss ship (placeholder large rect)
        fill(50, 0, 50, 200);
        stroke('#ff00ff');
        strokeWeight(4);
        rectMode(CENTER);
        rect(bossEntity.x, bossEntity.y, 200, 100, 20);
        rectMode(CORNER);
        noStroke();
        fill('#fff');
        textAlign(CENTER);
        text("BOSS", bossEntity.x, bossEntity.y - 10);
        
        let targetWord = bossEntity.words[bossEntity.currentWordIdx];
        if (userInput.length > 0 && targetWord.toLowerCase().startsWith(userInput.toLowerCase())) {
            let typedPart = targetWord.substring(0, userInput.length);
            let restPart = targetWord.substring(userInput.length);
            fill('#00f2fe');
            text(typedPart, bossEntity.x - textWidth(targetWord)/2 + textWidth(typedPart)/2, bossEntity.y + 30);
            fill(255);
            text(restPart, bossEntity.x + textWidth(typedPart)/2, bossEntity.y + 30);
        } else {
            fill(255);
            text(targetWord, bossEntity.x, bossEntity.y + 30);
        }
        textAlign(LEFT);

        if (bossEntity.y > borderY) {
            lives -= 3;
            bossActive = false;
            bossEntity = null;
            shakeScreen();
            if (lives <= 0) gameOver = true;
        }
    }

    // Draw Words
    for (let i = words.length - 1; i >= 0; i--) {
        words[i].y += words[i].speed * currentSpeedMult;
        let wordText = words[i].text;
        
        // Style by type
        drawingContext.shadowBlur = 8;
        if (words[i].type === 'emp') { fill('#ff00ff'); drawingContext.shadowColor = '#ff00ff'; }
        else if (words[i].type === 'freeze') { fill('#00f2fe'); drawingContext.shadowColor = '#00f2fe'; }
        else if (words[i].type === 'shield') { fill('#38ef7d'); drawingContext.shadowColor = '#38ef7d'; }
        else { fill(255); drawingContext.shadowColor = 'white'; }

        if (userInput.length > 0 && wordText.toLowerCase().startsWith(userInput.toLowerCase())) {
            let typedPart = wordText.substring(0, userInput.length);
            let restPart = wordText.substring(userInput.length);
            fill('#00f2fe');
            drawingContext.shadowColor = '#00f2fe';
            text(typedPart, words[i].x, words[i].y);
            fill(255);
            drawingContext.shadowColor = 'white';
            text(restPart, words[i].x + textWidth(typedPart), words[i].y);
        } else {
            text(wordText, words[i].x, words[i].y);
        }
        drawingContext.shadowBlur = 0;

        if (words[i].y > borderY) {
            lives--;
            shakeScreen();
            
            words.splice(i, 1);
            if (lives <= 0) gameOver = true;
        }
    }

    // Draw lasers
    for (let i = lasers.length - 1; i >= 0; i--) {
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

    // Draw explosions (Particles)
    for (let i = explosions.length - 1; i >= 0; i--) {
        let ex = explosions[i];
        for(let p of ex.particles) {
            p.x += p.vx; p.y += p.vy;
            fill(p.color);
            circle(p.x, p.y, p.size * (ex.lifetime/20));
        }
        ex.lifetime--;
        if (ex.lifetime <= 0) explosions.splice(i, 1);
    }
}

function drawWpmBadge(wpm) {
    let bw = 130, bh = 38, bx = width - bw - 10, by = 8;
    drawingContext.save();
    drawingContext.fillStyle = 'rgba(0, 242, 254, 0.12)';
    drawingContext.strokeStyle = 'rgba(0, 242, 254, 0.5)';
    drawingContext.lineWidth = 1.5;
    let r = 10;
    drawingContext.beginPath();
    drawingContext.moveTo(bx + r, by);
    drawingContext.lineTo(bx + bw - r, by);
    drawingContext.quadraticCurveTo(bx + bw, by, bx + bw, by + r);
    drawingContext.lineTo(bx + bw, by + bh - r);
    drawingContext.quadraticCurveTo(bx + bw, by + bh, bx + bw - r, by + bh);
    drawingContext.lineTo(bx + r, by + bh);
    drawingContext.quadraticCurveTo(bx, by + bh, bx, by + bh - r);
    drawingContext.lineTo(bx, by + r);
    drawingContext.quadraticCurveTo(bx, by, bx + r, by);
    drawingContext.closePath();
    drawingContext.fill();
    drawingContext.stroke();
    drawingContext.restore();

    noStroke();
    textSize(11);
    fill(150, 230, 255, 160);
    textAlign(RIGHT);
    text('WPM', width - 14, by + 16);
    textSize(20);
    fill('#00f2fe');
    drawingContext.shadowBlur = 10;
    drawingContext.shadowColor = '#00f2fe';
    text(wpm, width - 14, by + 33);
    drawingContext.shadowBlur = 0;
    textAlign(LEFT);
}

function drawWpmChart() {
    const cvs = document.getElementById('wpm-timeline-canvas');
    if (!cvs) return;
    const dpr = window.devicePixelRatio || 1;
    const w = cvs.offsetWidth;
    const h = 120;
    cvs.width = w * dpr;
    cvs.height = h * dpr;
    const ctx = cvs.getContext('2d');
    ctx.scale(dpr, dpr);
    ctx.clearRect(0, 0, w, h);

    let data = wpmTimeline.length > 0 ? wpmTimeline : [{time: 0, wpm: 0}, {time: 60, wpm: getCurrentWpm()}];
    if (data.length < 2) data = [{time: 0, wpm: 0}, ...data, {time: 60, wpm: getCurrentWpm()}];
    let maxWpm = Math.max(...data.map(d => d.wpm), 1);
    let pad = { top: 12, right: 12, bottom: 28, left: 38 };
    let cw = w - pad.left - pad.right;
    let ch = h - pad.top - pad.bottom;

    ctx.strokeStyle = 'rgba(255,255,255,0.07)';
    ctx.lineWidth = 1;
    for (let i = 0; i <= 4; i++) {
        let y = pad.top + (ch / 4) * i;
        ctx.beginPath(); ctx.moveTo(pad.left, y); ctx.lineTo(pad.left + cw, y); ctx.stroke();
        let label = Math.round(maxWpm * (1 - i / 4));
        ctx.fillStyle = 'rgba(255,255,255,0.35)'; ctx.font = '10px Inter'; ctx.textAlign = 'right';
        ctx.fillText(label, pad.left - 4, y + 4);
    }
    ctx.fillStyle = 'rgba(255,255,255,0.35)'; ctx.textAlign = 'center';
    let maxTime = data[data.length - 1].time || 60;
    for (let s = 0; s <= maxTime; s += 15) { ctx.fillText(s + 's', pad.left + (s / maxTime) * cw, h - 6); }

    let grd = ctx.createLinearGradient(0, pad.top, 0, pad.top + ch);
    grd.addColorStop(0, 'rgba(0,242,254,0.35)'); grd.addColorStop(1, 'rgba(0,242,254,0.02)');
    ctx.fillStyle = grd; ctx.beginPath(); ctx.moveTo(pad.left, pad.top + ch);
    data.forEach((pt, idx) => { ctx.lineTo(pad.left + (pt.time / maxTime) * cw, pad.top + ch - (pt.wpm / maxWpm) * ch); });
    ctx.lineTo(pad.left + (data[data.length-1].time / maxTime) * cw, pad.top + ch); ctx.closePath(); ctx.fill();

    ctx.beginPath(); ctx.strokeStyle = '#00f2fe'; ctx.lineWidth = 2.5; ctx.lineJoin = 'round';
    ctx.shadowColor = '#00f2fe'; ctx.shadowBlur = 8;
    data.forEach((pt, idx) => {
        let x = pad.left + (pt.time / maxTime) * cw, y = pad.top + ch - (pt.wpm / maxWpm) * ch;
        if (idx === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    });
    ctx.stroke(); ctx.shadowBlur = 0;

    data.forEach(pt => {
        let x = pad.left + (pt.time / maxTime) * cw, y = pad.top + ch - (pt.wpm / maxWpm) * ch;
        ctx.beginPath(); ctx.arc(x, y, 3.5, 0, Math.PI * 2); ctx.fillStyle = '#00f2fe'; ctx.fill();
        ctx.strokeStyle = '#fff'; ctx.lineWidth = 1; ctx.stroke();
    });
}

function shootLaser() {
    let targetObj = null;
    let targetIdx = -1;
    let isBoss = false;

    // Check Boss
    if (bossActive && bossEntity) {
        let bWord = bossEntity.words[bossEntity.currentWordIdx];
        if (bWord.toLowerCase() === userInput.toLowerCase()) {
            isBoss = true;
            targetObj = bossEntity;
        }
    }

    // Check normal words
    if (!targetObj) {
        for (let i = 0; i < words.length; i++) {
            if (words[i].type !== 'asteroid' && words[i].text.toLowerCase() === userInput.toLowerCase()) {
                targetObj = words[i];
                targetIdx = i;
                break;
            }
        }
    }

    if (targetObj) {
        let laserStartX = rocketX;
        let laserStartY = rocketY - rocketHeight/6;
        let tx = isBoss ? targetObj.x : targetObj.x + textWidth(targetObj.text)/2;
        let ty = isBoss ? targetObj.y + 30 : targetObj.y;
        
        lasers.push({ x1: laserStartX, y1: laserStartY, x2: tx, y2: ty, lifetime: 10 });
        
        let parts = [];
        for(let p=0; p<15; p++) {
           parts.push({
               x: tx, y: ty, 
               vx: (Math.random()-0.5)*10, vy: (Math.random()-0.5)*10, 
               size: Math.random()*8 + 2,
               color: '#00f2fe'
           });
        }
        explosions.push({ particles: parts, lifetime: 20 });
        explosionSound.play();

        if(isBoss) {
            targetObj.currentWordIdx++;
            score += 5;
            if(targetObj.currentWordIdx >= targetObj.words.length) {
                bossActive = false;
                bossEntity = null;
                wordsClearedSinceBoss = 0;
            }
        } else {
            if(targetObj.type === 'emp') {
                score += words.length;
                words = []; // clear only words
            } else if(targetObj.type === 'freeze') {
                freezeTimer = 5;
            } else if(targetObj.type === 'shield') {
                lives++;
            }

            if(targetIdx !== -1 && targetObj.type !== 'emp') words.splice(targetIdx, 1);
            score++;
            wordsClearedSinceBoss++;
        }
        
        wordsTyped++;
        totalCharsCorrect += userInput.length;
        totalCharsTyped += userInput.length;
        userInput = "";
        return;
    }

    if (userInput.length > 0) {
        totalCharsTyped += userInput.length; 
        shakeScreen();
        userInput = "";
        if (currentDifficulty === "medium" || currentDifficulty === "hard") {
            lives--;
            if (lives <= 0) gameOver = true;
        }
    }
}

function shakeScreen() {
    let intensity = 10, duration = 300, start = Date.now();
    let interval = setInterval(() => {
        if (Date.now() - start > duration) {
            clearInterval(interval);
            document.body.style.transform = "translate(0, 0)";
            return;
        }
        let xOffset = (Math.random() * intensity * 2) - intensity;
        let yOffset = (Math.random() * intensity * 2) - intensity;
        document.body.style.transform = `translate(${xOffset}px, ${yOffset}px)`;
    }, 50);
}

function keyPressed() {
    if (gameOver) return;
    if (keyCode === 8) {
        if (!backspaceInterval) {
            userInput = userInput.slice(0, -1);
            backspaceInterval = setTimeout(() => {
                backspaceInterval = setInterval(() => {
                    if (userInput.length > 0) userInput = userInput.slice(0, -1);
                    else { clearInterval(backspaceInterval); backspaceInterval = null; }
                }, backspaceSpeed);
            }, backspaceDelay);
        }
        return false;
    } else if (keyCode === 13 || keyCode === 32) {
        shootLaser();
        return false;
    } else if (key.length === 1 && key.match(/[a-z]/i)) {
        userInput += key.toLowerCase();
        
        let tWord = null;
        if(bossActive && bossEntity) {
            let bWord = bossEntity.words[bossEntity.currentWordIdx];
            if (bWord.toLowerCase().startsWith(userInput.toLowerCase())) tWord = bossEntity;
        }
        
        if(!tWord) {
            for (let word of words) {
                if (word.text.toLowerCase().startsWith(userInput.toLowerCase())) {
                    tWord = word;
                    break;
                }
            }
        }
        
        if(tWord) {
            if (bossActive && tWord === bossEntity) {
               targetX = tWord.x;
           } else {
               targetX = tWord.x + textWidth(tWord.text)/2;
           }
        }
    }
}

function keyReleased() {
    if (keyCode === 8 && backspaceInterval) {
        clearTimeout(backspaceInterval);
        if (typeof backspaceInterval === 'number') clearInterval(backspaceInterval);
        backspaceInterval = null;
    }
}

function updateTimer() {
    if(freezeTimer > 0) freezeTimer--;
    if (timer > 0) timer--;
    else { gameOver = true; clearInterval(timerInterval); }
}

function restartGame() {
    if (currentAudio) currentAudio.stop();
    location.reload();
}

function exitGame() {
    if (currentAudio) currentAudio.stop();
    window.history.back();
}
