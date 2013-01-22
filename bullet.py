from panda3d.core import Point2, Vec3, CollisionSphere, CollisionNode, BitMask32
from math import radians, cos, sin, hypot

from loader import load_object

def distance_check(obj1, obj2):
    return hypot(obj1.x - obj2.x, obj1.y - obj2.y) > 200

class BulletManager():
    def __init__(self, app):
        self.app = app
        self.bullet_index = 0
        self.bullets = {}

    def create_bullet(self, launched_by):
        bullet = Bullet(self.app, launched_by, self.bullet_index)
        self.app.scene.append(bullet)

        self.bullets["bullet_cn_%d" % self.bullet_index] = bullet
        self.bullet_index = self.bullet_index + 1

    def remove_bullet(self, bullet_id):
        bullet = self.bullets[bullet_id]
        if not bullet.deleted:
            self.app.scene.remove(bullet)
            bullet.np.removeNode()
        bullet.deleted = True

    def get_bullet(self, bullet_id):
        #return self.bullets[bullet_id.split['/'][-1]]
        return self.bullets[bullet_id]


    def update(self, time):
        for bullet in self.bullets.items():
            if not bullet[1].deleted:
                if distance_check(bullet[1].np.getPos(), self.app.player.np.getPos()):
                    self.remove_bullet(bullet[0])

class Bullet():
    movespeed = 1.5
    def __init__(self, app, launched_by, index):
        self.app = app
        self.model = load_object("bullet", pos=Point2(0,0), depth=1, scale=10.0)
        self.launched_by = launched_by
        self.deleted = False

        self.np = app.render.attachNewNode("bullet_%d" % index)
        self.np.setHpr(self.launched_by.np.getHpr())
        self.np.setScale(0.1)
 
        rads = radians(self.launched_by.np.getHpr().x)
        self.movement = Vec3(self.movespeed * cos(rads), self.movespeed * sin(rads), 0)
        self.model.reparentTo(self.np)
        self.np.setPos(self.launched_by.np.getPos() + self.movement)

        self.cn = self.np.attachNewNode(CollisionNode('bullet_cn_%d' % index))
        self.cs = CollisionSphere(self.model.getPos(), 1)
        self.cn.node().addSolid(self.cs)
        #self.cn.show()

        self.cn.node().setFromCollideMask(BitMask32(0x00))
        self.cn.node().setIntoCollideMask(BitMask32(0x10))


    def update(self, time):
        self.np.setPos(self.np.getPos() + self.movement)

    def apply_effect(self, target):
        target.hp = target.hp - 10


