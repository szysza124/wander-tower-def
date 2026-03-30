import sys
import time
from PyQt5 import QtCore, QtGui, QtWidgets

from towers import *
import globals


class scoreBoard(QtWidgets.QFrame):
    def __init__(self, parent):
        super().__init__(parent) 
        self.mainBoard = parent.mainBoard
        self.controller = parent
        self.isPaused = False

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.showGameStats(qp)
        self.showTowerStats(qp)
        qp.end()

    def start(self):
        self.setStyleSheet("QWidget { background: #A4A4A4 }") 
        self.setGeometry(600, 0, 200, 520)

        y_off = 85
        btn1 = QtWidgets.QPushButton("Tower 1", self)
        btn1.move(10, y_off)

        btn2 = QtWidgets.QPushButton("Tower 2", self)
        btn2.move(110, y_off)

        btn3 = QtWidgets.QPushButton("Tower 3", self)
        btn3.move(10, y_off+30)

        btn4 = QtWidgets.QPushButton("Tower 4", self)
        btn4.move(110, y_off+30)

        self.setupPauseButton()
        self.setupNextWaveButton()
        self.setupUpgradeButton()

        btn1.clicked.connect(self.towerOne)
        btn2.clicked.connect(self.towerTwo)
        btn3.clicked.connect(self.towerThree)
        btn4.clicked.connect(self.towerFour)

    def showTowerStats(self, qp):
        y_off = 150
        qp.setPen(QtGui.QColor(0, 0, 0))
        qp.setBrush(QtGui.QColor(0, 0, 0, 0))
        qp.drawRect(10, y_off, 180, 80)

        if self.mainBoard.isTowerClicked or self.mainBoard.isTowerSelected:
            qp.setPen(QtGui.QColor(0, 34, 3))
            qp.setFont(QtGui.QFont('Decorative', 10))
            qp.drawText(15, y_off+15, "DAMAGE: " + str(self.mainBoard.lastPlacedTower.damage))
            qp.drawText(15, y_off+30, "RANGE: " + str(self.mainBoard.lastPlacedTower.shotrange))
            qp.drawText(15, y_off+45, "RoF: " + str(self.mainBoard.lastPlacedTower.rof))
            qp.drawText(15, y_off+60, "VALUE: " + str(self.mainBoard.lastPlacedTower.cost))
            qp.drawText(15, y_off+75, "LEVEL: " + str(self.mainBoard.lastPlacedTower.level))

    def showGameStats(self, qp):
        y_off = 5
        qp.setPen(QtGui.QColor(0, 0, 0))
        qp.setBrush(QtGui.QColor(0, 0, 0, 0))
        qp.drawRect(10, y_off, 180, y_off + 70)
        qp.setPen(QtGui.QColor(0, 34, 3))
        qp.setFont(QtGui.QFont('Decorative', 10))
        qp.drawText(15, 20, "MONEY: "+ str(globals.money))
        qp.drawText(15, 35, "LIVES: "+ str(globals.lives))
        qp.drawText(15, 50, "SCORE: "+ str(globals.score))
        qp.drawText(15, 65, "NEXT WAVE: "+ str(self.mainBoard.currentWave))

    def towerSelected(self):
        self.mainBoard.isTowerSelected = True
        self.mainBoard.isTowerClicked = False
        
    def towerOne(self):
        self.towerSelected()
        self.mainBoard.lastPlacedTower = PinkTower()

    def towerTwo(self):
        self.towerSelected()
        self.mainBoard.lastPlacedTower = GreenTower()

    def towerThree(self):
        self.towerSelected()
        self.mainBoard.lastPlacedTower = PurpleTower()

    def towerFour(self):
        self.towerSelected()
        self.mainBoard.lastPlacedTower = BlueTower()

    
    def setupPauseButton(self):
        self.pauseBtn = QtWidgets.QPushButton("Pause", self)
        self.pauseBtn.move(110, 480)
        self.pauseBtn.clicked.connect(self.pauseGame) 

    def pauseGame(self):
        if self.isPaused == False:
            self.pauseBtn.setText('Play')
            print("game paused") 
            self.isPaused = True 
            self.controller.timer.stop()  
        else:
            self.pauseBtn.setText('Pause')
            print("playing game") 
            self.isPaused = False 
            self.controller.timer.start(globals.gameSpeed, self.controller)  

    def setupNextWaveButton(self):
        self.nextWaveBtn = QtWidgets.QPushButton("Next Wave", self)
        self.nextWaveBtn.move(15, 480)
        self.nextWaveBtn.clicked.connect(self.nextWaveAction) 

    def nextWaveAction(self):
        self.mainBoard.isWaveSent = True

    def setupUpgradeButton(self):
        self.upgradeBtn = QtWidgets.QPushButton("upgrade",self)
        self.upgradeBtn.move(10, 250) 
        self.upgradeBtn.clicked.connect(self.upgradeAction)

    def upgradeAction(self):
        if self.mainBoard.isTowerClicked:
            if self.mainBoard.lastPlacedTower.upgrade():
                self.mainBoard.repaint
                self.repaint
            else:
                print("no money or max level")

    def buttonClicked(self):
        sender = self.sender()
        print("button was pressed", sender.text())

    def showTime(self, qp):
        qp.setPen(QtGui.QColor(0, 34, 3))
        qp.setFont(QtGui.QFont('Decorative', 10))
        qp.drawText(10, 20, "GAME TICKS: ")
        # print("TIME REDRAWN!")

    def towerOptions(self, qp):
        pass