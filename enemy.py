from random import randint, random, uniform
from math import atan2, degrees, radians, sin, cos

from panda3d.core import Vec3

from direct.actor.Actor import Actor

class EnemyManager():
    def __init__(self, app):
        self.model = Actor('models/panda-model', {"walk" : "models/panda-walk4"})
        self.model.setHpr(90,0,0)
        self.model.setPos(0,0,0)
        self.model.setScale(0.0005)
        self.model.setPlayRate(2.0, "walk")
        self.model.loop("walk")
        self.model.hide()

    def add_instance(self,enemy):
        self.model.show()
        self.model.instanceTo(enemy.np)

class Enemy():
    movespeed = 0.01
    def __init__(self, pos, index, app, manager):
        self.position = pos
        self.app = app

        self.np = app.render.attachNewNode("enemy%d" % index)
        self.np.setPos(self.position)

        manager.add_instance(self)

        self.np.setHpr(uniform(1,360),0,0)
    
    def update(self, time):
        # turn to look at player
        desired = self.app.player.position - self.np.getPos()
        angle = degrees(atan2(desired.y, desired.x))

        hpr = self.np.getHpr()
        if hpr.x > 360:
            hpr.x = hpr.x - 360
        if hpr.x < -360:
            hpr.x = hpr.x + 360

        diff = angle - hpr.x 

        if diff > 180.0:
            diff = diff - 360

        if diff < -180.0:
            diff = diff + 360

        if diff > 5.0:
            diff = 5.0
        if diff < -5.0:
            diff = -5.0

        new = Vec3(diff, 0, 0) + hpr
        self.np.setHpr(new)

        # move forward
        r = radians(new.x)

        curr = self.np.getPos()
        diff = Vec3(self.movespeed * cos(r), self.movespeed * sin(r), 0)
        self.np.setPos(curr + diff)


        #self.np.setPos()


