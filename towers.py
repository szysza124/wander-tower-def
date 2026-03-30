import sys
import time
from PyQt5 import QtCore, QtGui
from math import sqrt

from enemies import *


# tower objects 
# tower objects 
class Tower(object):
    def __init__(self): 
        self.position_x = -100
        self.position_y = -100
        self.occupied = []
        self.retailvalue = 1000
        self.level = 1
        self.upgrade_cost = 200
   
        self.size = 0
        self.shotrange = 0
        self.cost = 0
        self.damage = 0
        self.rof = 0
        self.color = QtGui.QColor(0, 0, 0, 0) 
        self.cooldown = 0

    def getColor(self):
        return self.color

    def getCenter(self):
        center_x = self.position_x + (self.size * 20 // 2)
        center_y = self.position_y + (self.size * 20 // 2)
        return QtCore.QPoint(center_x, center_y)

    def getOccupied(self):
        return self.occupied

    def getRange(self):
        return self.shotrange

    def getLevel(self):
        return self.level
    
    def upgrade(self):
        import globals         
        if self.level < 3 and globals.money >= self.upgrade_cost:
            globals.money -= self.upgrade_cost
            self.level += 1
            self.damage += 1      
            self.shotrange = self.shotrange//0.9   
        
            self.retailvalue += self.upgrade_cost
            self.upgrade_cost = int(self.upgrade_cost * 1.5) 
            return True
        return False

    def inRange(self, enemy):
        dx = self.getCenter().x() - enemy.getCenter().x()
        dy = self.getCenter().y() - enemy.getCenter().y()
        return int(sqrt(pow(dx, 2) + pow(dy, 2))) <= self.shotrange

    
class PinkTower(Tower):
    def __init__(self):
        super().__init__() 
        self.color = QtGui.QColor(255, 80, 100, 255)
        self.name = "mini helper"
        self.size = 1
        self.shotrange = 120
        self.cost = 200
        self.damage = 1
        self.rof = 5

    def determineTarget(self, targets):
        new_targets = []
        for i in targets:
            if self.inRange(i):
                new_targets.append(i)
        try:
            return [new_targets[-1]] 
        except IndexError:
            return []


class GreenTower(Tower):
    def __init__(self):
        super().__init__()
        
        self.color = QtGui.QColor(0, 200, 100, 255)
        self.name = "gargatuan"
        self.size = 2
        self.shotrange = 200
        self.cost = 300
        self.damage = 1
        self.rof = 1

    def determineTarget(self, targets):
        new_targets = []
        for i in targets:
            if self.inRange(i):
                new_targets.append(i)
        try:
            return [new_targets[-1], new_targets[-2]]
        except IndexError:
            try:
                return [new_targets[-1]]
            except IndexError:
                return []


class PurpleTower(Tower):
    def __init__(self):
        super().__init__()
        self.color = QtGui.QColor(25, 180, 10, 255)
        self.size = 2
        self.shotrange = 160
        self.cost = 200
        self.damage = 2
        self.rof = 1

    def determineTarget(self, targets):
        new_targets = []
        for i in targets:
            if self.inRange(i):
                new_targets.append(i)
        try:
            return [new_targets[-1]]
        except IndexError:
            return []


class BlueTower(Tower):
    def __init__(self):
        super().__init__()
        self.color = QtGui.QColor(55, 80, 100, 255)
        self.size = 2
        self.shotrange = 100
        self.cost = 200
        self.damage = 3
        self.rof = 1

    def determineTarget(self, targets):
        new_targets = []
        for i in targets:
            if self.inRange(i):
                new_targets.append(i)
        try:
            return [new_targets[-1]]
        except IndexError:
            return []