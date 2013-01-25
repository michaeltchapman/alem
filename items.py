from panda3d.core import Vec3, Texture, Vec4, BitMask32
from panda3d.core import CollisionSphere, CollisionNode

from math import sin, fabs

from random import uniform, randint

class ItemManager(object):
    def __init__(self, app):
        self.items = {}
        self.index = 0
        self.app = app

    def add_item(self, pos, item, arg):
        if item == "soul":
            item = Soul(arg)
        if item == "upgrade":
            item = Upgrade(arg)
        i = Item(self.app, pos, item, self.index)
        self.items["item_c_%d" % self.index] = i
        self.app.scene.append(i)
        self.index = self.index + 1

    def pickup(self, item, player):
        self.items[item].item.apply_effect(player)
        self.remove_item(item)

    def remove_item(self, item):
        self.app.scene.remove(self.items[item])
        self.items[item].np.detachNode()
        self.items[item] = None

# purple pickup
class Soul(object):
    color = Vec4(0.15, -0.15, 0.15, 1.0)
    def __init__(self, count):
        self.count = int(count)

    def apply_effect(self, target):
        target.souls = target.souls + self.count

types = ["hp", "move_speed", "fire_rate", "fire_arcs", "bullet_speed", "bullet_explodesize", "bullet_damage"]
# purple pickup
class Upgrade(object):
    color = Vec4(0.15, 0.15, -0.15, 1.0)
    def __init__(self, level):
        # (key, value) tuple
        self.upgrade = self.generate_upgrade(level)

    def generate_upgrade(self,level):
        # Distribute this according to value
        # (create some rarity)
        t = types[randint(0,len(types)-1)]
        #t = types[0]

        if t == "hp":
            r = 10.0*level + 60
        if t == "move_speed":
            r = 0.05
        if t == "fire_rate":
            r = -0.001
        if t == "fire_arcs":
            r = 1
        if t == "bullet_speed":
            r = level
        if t == "bullet_explodesize":
            r = level * 0.05
        if t == "bullet_damage":
            r = 5.0*level
        return (t,r)    

    def apply_effect(self, target):
        setattr(target, self.upgrade[0], getattr(target, self.upgrade[0]) + self.upgrade[1])


# All loot objects
class Item(object):
    spin_speed = Vec3(2,0.0,0.0)
    def __init__(self, app, pos, item, index):

        self.np = app.render.attachNewNode("item_%d" % index)

        self.model = app.loader.loadModel('models/box')
        self.model.reparentTo(self.np)
        self.model.setScale(0.4)
        self.model.setColorScale(0.8, 0.8, 0.5, 1.0)

        self.np.setPos(pos)

        self.cn = self.np.attachNewNode(CollisionNode('item_c_%d' % index))
        self.cs = CollisionSphere(0,0.0,0.0,4)
        self.cn.node().addSolid(self.cs)

        self.cn.node().setFromCollideMask(BitMask32(0x00))
        self.cn.node().setIntoCollideMask(BitMask32(0x01))

        self.item = item

    def update(self, timer):
        # highlight by cycling color and spinning
        t = fabs(sin(timer*2))*0.75 + 0.1
        v = Vec4(t,t,t,0)

        self.model.setColorScale(v+self.item.color)
        self.np.setHpr(self.np.getHpr() + self.spin_speed)

