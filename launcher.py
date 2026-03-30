import sys
import time
from PyQt5 import QtCore, QtGui, QtWidgets

from enemies import *
from towers import *
from scoreboard import *
from gameboard import *

import globals


class TowerDefence(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__() 

        self.setFixedSize(800, 520)
        self.setWindowTitle('Dat Tower Defence!')
        self.mainBoard = gameBoard(self)
        self.secondaryBoard = scoreBoard(self)

        self.setCentralWidget(self.mainBoard)
        
        self.mainBoard.start()
        self.secondaryBoard.start()

        self.timer = QtCore.QBasicTimer()
        self.timer.start(globals.gameSpeed, self)
        self.update()
        self.isFastForward = False

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.mainBoard.timedLoop()
            self.repaint()
        else:
            super().timerEvent(event)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_P:
            self.mainBoard.pause()
        elif event.key() == QtCore.Qt.Key_F:
            self.isFastForward = not self.isFastForward
            speed = globals.gameSpeed // 10 if self.isFastForward else globals.gameSpeed
            self.timer.start(speed, self)
    
    def mousePressEvent(self, event):
        self.mainBoard.placeTowers()

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.MouseMove:
            if event.buttons() == QtCore.Qt.NoButton and str(source).find("gameBoard") > 0:
                pos = event.pos()
                self.mainBoard.updateMouse(pos.x(), pos.y())
                self.mainBoard.isMouseIn = True
            else:
                self.mainBoard.isMouseIn = False
                self.mainBoard.repaint()
        
        return super().eventFilter(source, event)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    towerdef = TowerDefence()
    towerdef.show()
    app.installEventFilter(towerdef)
    sys.exit(app.exec_())