#!/usr/bin/python

from math import pi, sin, cos
from direct.showbase.ShowBase import ShowBase
from direct.task import Task

from panda3d.core import Point2, Point3, Texture

from player import Player

app = None

def load_object(tex = None, pos = Point2(0,0), depth = 0, transparency = True, scaleX = 1, scaleY = 1, scale = None):
    global app
    obj = app.loader.loadModel("models/plane")
    obj.reparentTo(app.render)

    obj.setPos(Point3(pos.getX(), pos.getY(), depth))

    if (scale == None):
        obj.setScale(scaleX, 1, scaleY)
    else:
        obj.setScale(scale)

    obj.setBin("unsorted", 0) # ignore draw order (z-fighting fix)       
    obj.setDepthTest(True)   # Don't disable depth write like the tut says
    obj.setHpr(0, -90, 0)

    if transparency:
        obj.setTransparency(1) #All of our objects are transparent
    else:
        obj.setTransparency(0) #All of our objects are transparent
    if tex:
        tex = app.loader.loadTexture("textures/"+tex+".png") #Load the texture
        tex.setWrapU(Texture.WMClamp)                    # default is repeat, which will give
        tex.setWrapV(Texture.WMClamp)                    # artifacts at the edges
        obj.setTexture(tex, 1)                           #Set the texture

    return obj

class Alem(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        global app
        app = self

        self.scene = []
        self.player = Player(self)
        self.scene.append(self.player)

        self.backgrounds = self.gen_background()

        self.rl = base.camLens.makeCopy()

        self.taskMgr.add(self.update, "update")

        self.set_keys()

    def camera_task(self):    
        self.camera.setPos(self.player.position.x, self.player.position.y , 20)
        self.camera.setHpr(0,-90,0)

    def set_keys(self):
        self.accept("a", self.player.move_left, [True])
        self.accept("a-up", self.player.move_left, [False])

        self.accept("d", self.player.move_right, [True])
        self.accept("d-up", self.player.move_right, [False])

        self.accept("w", self.player.move_up, [True])
        self.accept("w-up", self.player.move_up, [False])

        self.accept("s", self.player.move_down, [True])
        self.accept("s-up", self.player.move_down, [False])

    def update(self, task):
        for entity in self.scene:
            entity.update(task.time)
        self.camera_task()
        return Task.cont

    def gen_background(self):
        bg_x = 5
        bg_y = 5

        tile_count = 10

        backgrounds = []

        for i in range(10):
            for j in range(10):
                backgrounds.append(load_object("grass", pos = Point2(i*bg_x, j*bg_y), transparency = False, scale = 5))

        return backgrounds

if __name__ == "__main__":
    print "works"
    app = Alem()
    app.run()
