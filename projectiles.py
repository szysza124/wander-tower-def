import math
from PyQt5 import QtCore

class Projectile(object):
    def __init__(self, origin, destination):
        self.origin = origin
        self.destination = destination
        self.pos_x = origin.getCenter().x()
        self.pos_y = origin.getCenter().y()
        self.speed = 5
        self.hit = False

    def move(self):
        dx = self.destination.getCenter().x() - self.pos_x
        dy = self.destination.getCenter().y() - self.pos_y
        dist = math.hypot(dx, dy)
        if dist <= self.speed:
            self.hit = True
        elif dist > 0:
            self.pos_x += (dx / dist) * self.speed
            self.pos_y += (dy / dist) * self.speed

    def dealDamage(self):
        self.destination.health -= self.origin.damage