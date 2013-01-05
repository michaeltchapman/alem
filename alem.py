#!/usr/bin/python

from math import pi, sin, cos
from direct.showbase.ShowBase import ShowBase
from direct.task import Task

from player import Player

class Alem(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.scene = []
        self.player = Player(self)
        self.scene.append(self.player)

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
        self.camera_task()
        for entity in self.scene:
            entity.update(task.time)
        return Task.cont


if __name__ == "__main__":
    print "works"
    app = Alem()
    app.run()
