import json

blockSize = 20
boardWidth = 600
boardHeight = 520

money = 1000
score = 0
lives = 100

currentWave = 0
isPaused = False
gameSpeed = 30

with open('map.json') as f:
    enemyPath = json.load(f)["enemyPath"]