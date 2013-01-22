from random import uniform
from panda3d.core import Texture
from panda3d.core import CollisionSphere, CollisionHandlerQueue, CollisionNode



class Tree(object):
    def __init__(self, app, pos, index):
        self.hp = 100
        self.app = app

        self.np = app.render.attachNewNode("tree%d" % index)
        self.np.setPos(pos)

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


    def update(self, timer):
        pass

