import sys
import time
import json
import copy
from PyQt5 import QtCore, QtGui, QtWidgets

from towers import *
from enemies import *
from projectiles import *

import globals


class gameBoard(QtWidgets.QFrame):
    def __init__(self, parent):
        super().__init__(parent) 
        self.controller = parent

        self.mouse_x = -1
        self.mouse_y = -1

        self.currentWave = 1
        self.isWaveSent = False
        self.isWaveInProgress = False

        self.graceUnits = 4

        self.NoU_sent = 0

        self.isLastWave = False
        self.isMouseIn = False
        self.isTowerSelected = False
        self.isTowerClicked = False

        self.lastPlacedTower = Tower()

        self.projectileOccupancy = []
        self.towerOccupancy = []
        self.enemyOccupancy = []
        self.nonOccupiable = []

    def start(self):
        self.setStyleSheet("QWidget { background: #A9F5D0 }") 
        self.setFixedSize(globals.boardWidth, globals.boardHeight)
        for i in globals.enemyPath:
            self.nonOccupiable.append([i[0]*globals.blockSize, i[1]*globals.blockSize])

    def pause(self):
        print("paused") 

    def gameOver(self, qp):
        for i in range(len(self.enemyOccupancy)):
            self.enemyOccupancy.pop()
        for i in range(len(self.towerOccupancy)):
            self.towerOccupancy.pop()
        for i in range(len(self.nonOccupiable)):
            self.nonOccupiable.pop()

        qp.setPen(QtGui.QColor(0, 34, 3))
        qp.setFont(QtGui.QFont('Decorative', 50))
        qp.drawText(95, 280, "GAME OVER!")
        self.controller.timer.stop() 

    def winner(self, qp):
        for i in range(len(self.enemyOccupancy)):
            self.enemyOccupancy.pop()
        for i in range(len(self.towerOccupancy)):
            self.towerOccupancy.pop()
        for i in range(len(self.nonOccupiable)):
            self.nonOccupiable.pop()

        qp.setPen(QtGui.QColor(0, 34, 3))
        qp.setFont(QtGui.QFont('Decorative', 50))
        qp.drawText(125, 280, "WINNER!")
        self.controller.timer.stop() 

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        if globals.lives <= 0:
            self.gameOver(qp)
        elif self.isLastWave and len(self.enemyOccupancy) == 0: 
            self.winner(qp)
        else:
            self.waveManager()
            self.drawGrid(qp)
            self.drawPath(qp)
            self.drawTowers(qp)
            self.drawProjectiles(qp)
            if self.isTowerSelected:
                self.drawOutline(qp)
            if self.isTowerClicked:
                self.selectTower(qp, self.lastPlacedTower)
            self.drawEnemies(qp)
            self.drawEnemyHP(qp)
        qp.end()


    def waveManager(self):
        with open('waves.json') as json_data: 
            data = json.load(json_data)

        id = data["wave_"+str(self.currentWave)]["type"]
        NoU = int(data["wave_"+str(self.currentWave)]["units"])
        try:
            hp = int(data["wave_"+str(self.currentWave)]["HP"])
            if hp <= 0:
                print("hp error in json file (<= 0). hp set to 100")
                hp = 100
        except ValueError:
            print("value error in json file. hp set to 100")
            hp = 100

        
        if self.isWaveSent and self.isWaveInProgress == False:
    
            if self.NoU_sent == 0 or len(self.enemyOccupancy) == 0: 
                self.enemyOccupancy.insert(0, getattr(sys.modules[__name__], id)(copy.deepcopy(globals.enemyPath), hp))
                self.NoU_sent += 1
           
            elif self.NoU_sent < data["wave_"+str(self.currentWave)]["units"] + self.graceUnits:
                if not len(self.enemyOccupancy) == 0:
                    if self.enemyOccupancy[0].position_x >= data["wave_"+str(self.currentWave)]["delay"]:
                        self.enemyOccupancy.insert(0, getattr(sys.modules[__name__], id)(copy.deepcopy(globals.enemyPath), hp))
                        self.NoU_sent += 1
                        print(self.NoU_sent)
               
                if self.NoU_sent == data["wave_"+str(self.currentWave)]["units"]:
                    self.isWaveSent = False
                    self.isWaveInProgress = True
                    try:
                        id = data["wave_"+str(self.currentWave + 1)]["type"]
                        self.currentWave += 1
                        self.NoU_sent = 0
                    except Exception: 
                        self.isLastWave = True
                        self.NoU_sent = 0

        if self.isWaveInProgress and len(self.enemyOccupancy) == 0:
            self.isWaveInProgress = False
            self.isWaveSent = False
            globals.money = globals.money+(self.currentWave*100)
            print("survivor bonus: "+str(self.currentWave*100))

    def drawGrid(self, qp):
        pen = QtGui.QPen(QtGui.QColor(25, 180, 40, 55), 2, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        for i in range(0, 600, globals.blockSize):
            qp.drawLine(i, 0, i, globals.boardHeight)
            qp.drawLine(0, i, globals.boardWidth, i)

    def moveEnemies(self):
        if len(self.towerOccupancy) > 0: 
            for i in self.enemyOccupancy:
                i.move()

    def drawEnemies(self, qp):
        for i in self.enemyOccupancy:
            qp.setBrush(i.color)
            qp.drawEllipse(i.getCenter(), i.size, i.size)
            if i.isFinished:
                globals.lives -= 1
        self.enemyOccupancy[:] = [tup for tup in self.enemyOccupancy if tup.isFinished == False]
        self.enemyOccupancy[:] = [tup for tup in self.enemyOccupancy if tup.isDead == False]
            
    def drawPath(self, qp):
        qp.setPen(QtCore.Qt.NoPen)
        qp.setBrush(QtGui.QColor(255, 80, 100, 255))
        for i in globals.enemyPath:
            qp.drawRect(i[0]*globals.blockSize, i[1]*globals.blockSize, 20, 20)

    def drawTowers(self, qp):
        color = QtGui.QColor(0, 0, 0)
        qp.setPen(color)
        
        for i in self.towerOccupancy:
            qp.setBrush(i.color)
            qp.drawRect(i.position_x, i.position_y, i.size*globals.blockSize, i.size*globals.blockSize)
            qp.setFont(QtGui.QFont('Arial', 8, QtGui.QFont.Bold))
            text_rect = QtCore.QRect(i.position_x, i.position_y,  i.size*globals.blockSize, i.size*globals.blockSize)
            qp.drawText(text_rect, QtCore.Qt.AlignCenter, "v" + str(i.level))

     

    def get_x(self):
        if self.mouse_x > globals.boardWidth-40 and self.lastPlacedTower.size == 2:
            return globals.boardWidth-40
        return self.mouse_x

    def get_y(self):
        if self.mouse_y > globals.boardHeight-40 and self.lastPlacedTower.size == 2:
            return globals.boardHeight-40
        return self.mouse_y

    def drawOutline(self, qp):
        if self.isMouseIn:
            qp.setPen(QtCore.Qt.NoPen)
            qp.setBrush(self.lastPlacedTower.getColor())
            qp.drawRect(self.myround(self.get_x()), self.myround(self.get_y()), self.lastPlacedTower.size*20, self.lastPlacedTower.size*20)
            qp.setBrush(QtGui.QColor(0, 0, 0, 55))
            
            center_x = self.myround(self.get_x()) + (self.lastPlacedTower.size * 20 // 2)
            center_y = self.myround(self.get_y()) + (self.lastPlacedTower.size * 20 // 2)
            center = QtCore.QPoint(center_x, center_y)
            
            qp.drawEllipse(center, self.lastPlacedTower.shotrange, self.lastPlacedTower.shotrange)
            
        if not self.checkPlacement() and self.isMouseIn:
            qp.setPen(QtCore.Qt.NoPen)
            qp.setBrush(QtGui.QColor(0, 0, 0, 155))
            qp.drawRect(self.myround(self.get_x()), self.myround(self.get_y()), self.lastPlacedTower.size*20, self.lastPlacedTower.size*20)

    def selectTower(self, qp, t):
        qp.setPen(QtCore.Qt.NoPen)
        qp.setBrush(QtGui.QColor(0, 0, 0, 55))
        qp.drawEllipse(t.getCenter(), t.shotrange, t.shotrange)

    def myround(self, x, base=20):
        return x - (x % base)

    def updateMouse(self, x, y):
        self.mouse_y = y
        self.mouse_x = x
        self.repaint()

    def checkPlacement(self):
        if self.lastPlacedTower.size == 1:
            if [self.myround(self.get_x()), self.myround(self.get_y())] in self.nonOccupiable:
                return False
        elif self.lastPlacedTower.size == 2:
            if [self.myround(self.get_x()), self.myround(self.get_y())] in self.nonOccupiable or \
               [self.myround(self.get_x()), self.myround(self.get_y())+globals.blockSize] in self.nonOccupiable or \
               [self.myround(self.get_x())+globals.blockSize, self.myround(self.get_y())] in self.nonOccupiable or \
               [self.myround(self.get_x())+globals.blockSize, self.myround(self.get_y())+globals.blockSize] in self.nonOccupiable:
                return False
        return True

    def placeTowers(self):
        if self.checkPlacement() and self.isTowerSelected:
            self.lastPlacedTower.position_x = self.myround(self.get_x())
            self.lastPlacedTower.position_y = self.myround(self.get_y())

            if self.isMouseIn and globals.money >= self.lastPlacedTower.cost:
                self.towerOccupancy.append(self.lastPlacedTower)
                self.isTowerSelected = False
                self.isTowerClicked = True
                globals.money -= self.lastPlacedTower.cost

                if self.lastPlacedTower.size == 1:
                    self.nonOccupiable.append([self.myround(self.get_x()), self.myround(self.get_y())])
                    self.lastPlacedTower.occupied.append([self.myround(self.get_x()), self.myround(self.get_y())])
                elif self.lastPlacedTower.size == 2:
                    self.nonOccupiable.append([self.myround(self.get_x()), self.myround(self.get_y())])
                    self.nonOccupiable.append([self.myround(self.get_x())+globals.blockSize, self.myround(self.get_y())])
                    self.nonOccupiable.append([self.myround(self.get_x()), self.myround(self.get_y())+globals.blockSize])
                    self.nonOccupiable.append([self.myround(self.get_x())+globals.blockSize, self.myround(self.get_y())+globals.blockSize])

                    self.lastPlacedTower.occupied.append([self.myround(self.get_x()), self.myround(self.get_y())])
                    self.lastPlacedTower.occupied.append([self.myround(self.get_x())+globals.blockSize, self.myround(self.get_y())])
                    self.lastPlacedTower.occupied.append([self.myround(self.get_x()), self.myround(self.get_y())+globals.blockSize])
                    self.lastPlacedTower.occupied.append([self.myround(self.get_x())+globals.blockSize, self.myround(self.get_y())+globals.blockSize])
            else:
                self.lastPlacedTower = Tower()
                self.isTowerSelected = False

        elif self.isMouseIn:
            for i in self.towerOccupancy:
                if [self.myround(self.get_x()), self.myround(self.get_y())] in i.getOccupied():
                    print("print tower stats")
                    self.lastPlacedTower = i
                    self.isTowerSelected = False
                    self.isTowerClicked = True
                    break
                else:
                    self.isTowerClicked = False
        self.repaint()

    def targettedEnemies(self):
        pass

    def timedLoop(self):
        self.moveEnemies()
        for t in self.towerOccupancy:
            if t.cooldown > 0:
                t.cooldown -= 1
            else:
                targets = t.determineTarget(self.enemyOccupancy)
                if targets:
                    for k in targets:
                        self.projectileOccupancy.append(Projectile(t, k))
                    t.cooldown = t.rof * 5
        self.dealDamage()

    def dealDamage(self):
        for p in self.projectileOccupancy:
            p.move()
            if p.hit:
                p.dealDamage()
        self.projectileOccupancy = [p for p in self.projectileOccupancy if not p.hit]

    def drawProjectiles(self, qp):
        qp.setPen(QtCore.Qt.NoPen)
        qp.setBrush(QtGui.QColor(0, 0, 0))
        for p in self.projectileOccupancy:
            qp.drawEllipse(QtCore.QPoint(int(p.pos_x), int(p.pos_y)), 4, 4)

    def drawEnemyHP(self, qp):
        qp.setPen(QtGui.QColor(0, 34, 3))
        qp.setFont(QtGui.QFont('Decorative', 6))
        for i in self.enemyOccupancy:
            qp.drawText(i.getHPcoord().x(), i.getHPcoord().y(), str(i.health))