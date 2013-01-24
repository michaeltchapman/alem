from random import uniform
from panda3d.core import Texture, BitMask32
from panda3d.core import CollisionSphere, CollisionHandlerQueue, CollisionNode

class TreeManager(object):
    def __init__(self, app):
        self.app = app
        self.index = 0

    def add_tree(self, pos, level):
        tree = Tree(self.app, pos, level, self.index)
        self.index = self.index + 1
        self.app.scene.append(tree)


class Tree(object):
    def __init__(self, app, pos, level, index):
        self.hp = 200 * level
        self.app = app

        self.np = app.render.attachNewNode("tree%d" % index)
        self.np.setPos(pos)

        self.level = level
        self.pursuers = []

        self.model = app.loader.loadModel('models/tree1')
        tex = app.loader.loadTexture("textures/"+'tree1'+".jpg") #Load the texture
        tex.setWrapU(Texture.WMClamp)                    # default is repeat, which will give
        tex.setWrapV(Texture.WMClamp)                    # artifacts at the edges
        self.model.setTexture(tex, 1)                           #Set the texture
        self.model.reparentTo(self.np)

        self.model.setHpr(uniform(-180,180),0,0)
        self.model.setScale(2)

        self.cn = self.np.attachNewNode(CollisionNode('tree_c_%d' % index))
        self.cs = CollisionSphere(0,0.0,0.0,6)
        self.cn.node().addSolid(self.cs)

        self.cn.node().setFromCollideMask(BitMask32(0x01))
        self.cn.node().setIntoCollideMask(BitMask32(0x00))

        self.cqueue = CollisionHandlerQueue()
        app.cTrav.addCollider(self.cn, self.cqueue)

    def update(self, timer):
        for i in range(self.cqueue.getNumEntries()):
            collided_name = self.cqueue.getEntry(i).getIntoNodePath().getName()
            #enemy collision
            if collided_name[0] == 'e':
                self.app.enemy_manager.handle_collision(collided_name, self, timer)
                # drop loot when killed by panda
                if self.hp < 0:
                    self.app.item_manager.add_item(self.np.getPos(), "upgrade", self.level)

            #hit by bullet    
            if collided_name[0] == 'b':    
                if self.hp < 0:
                    bullet = self.app.bullet_manager.get_bullet(collided_name)
                    bullet.apply_effect(self)
                    self.app.bullet_manager.remove_bullet(collided_name)

        # tree is dead
        if self.hp < 0:
            for p in self.pursuers:
                p.ai_b.pursue(self.app.player.np)

            self.app.scene.remove(self)
            self.np.detachNode()



