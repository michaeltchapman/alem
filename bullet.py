from panda3d.core import Point2, Vec3
from math import radians, cos, sin

from loader import load_object

class Bullet():
    movespeed = 0.1
    def __init__(self, app, launched_by, index):
        self.app = app
        self.model = load_object("bullet", pos=Point2(0,0), depth=1)

        self.launched_by = launched_by

        self.np = app.render.attachNewNode("bullet_%d" % index)
        self.np.setHpr(self.launched_by.np.getHpr())
        self.np.setScale(0.1)

        rads = radians(self.launched_by.np.getHpr().x)
        self.movement = Vec3(self.movespeed * cos(rads), self.movespeed * sin(rads), 0)
        self.model.reparentTo(self.np)
        self.np.setPos(self.launched_by.np.getPos() + self.movement)

    def update(self, time):
        self.np.setPos(self.np.getPos() + self.movement)

