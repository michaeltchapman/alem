from random import randint, random, uniform
from math import atan2, degrees, radians, sin, cos

from panda3d.core import Vec3, CollisionNode, CollisionSphere, CollisionHandlerQueue, BitMask32

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

        self.enemies = {}

    def add_instance(self,enemy):
        self.model.show()
        self.model.instanceTo(enemy.np)
        self.enemies[enemy.cn.getName()] = enemy

    def handle_collision(self, enemy, target, timer):
        self.enemies[enemy].apply_effect(target, timer)

class Enemy():
    movespeed = 0.01
    activate_delay = 0.1
    def __init__(self, pos, index, app, manager):
        self.position = pos
        self.app = app
        self.hp = 50

        self.np = app.render.attachNewNode("enemy%d" % index)
        self.np.setPos(self.position)

        self.np.setHpr(uniform(1,360),0,0)

        colsize = 0.2
        self.cn = self.np.attachNewNode(CollisionNode('enemy_cn_%d' % index))
        self.cs0 = CollisionSphere(colsize/2,0.0,0.0,colsize)
        self.cs1 = CollisionSphere(-colsize/2,0.0,0.0,colsize)
        self.cn.node().addSolid(self.cs0)
        self.cn.node().addSolid(self.cs1)
        self.cn.show() # debug

        self.cqueue = CollisionHandlerQueue()
        app.cTrav.addCollider(self.cn, self.cqueue)

        self.cn.node().setIntoCollideMask(BitMask32(0x01))
        self.cn.node().setFromCollideMask(BitMask32(0x10))

        self.last_activated = 0.0

        manager.add_instance(self)
    
    def update(self, time):
        a = 0
        # Handle collsions
        for i in range(self.cqueue.getNumEntries()):
           collided_name = self.cqueue.getEntry(i).getIntoNodePath().getName()
           #handle bullets
           if ("bullet" in collided_name):
               bullet = self.app.bullet_manager.get_bullet(collided_name)
               bullet.apply_effect(self)
               self.app.bullet_manager.remove_bullet(collided_name)

           #handle player    
           #elif ("player" in collided_name):
           #    self.apply_effect(self.app.player)
            
        # turn to look at player
        if self.cqueue.getNumEntries() != 0:
            self.np.setColorScale(1.0, self.hp / 100.0, self.hp / 100.0, 1.0)

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

        if self.hp < 0.0:
            self.app.scene.remove(self)
            self.np.removeNode()


    def apply_effect(self, target, timer):
        if self.last_activated - timer + self.activate_delay < 0.0:
            self.last_activated = timer
            target.hp = target.hp - 10
