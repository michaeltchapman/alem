#!/usr/bin/python

from math import pi, sin, cos
from direct.showbase.ShowBase import ShowBase
from direct.task import Task

from random import randint, random, uniform

from panda3d.core import Point2, Point3, Texture

from player import Player
from enemy import Enemy, EnemyManager
from bullet import Bullet

from loader import set_app, load_object

class Alem(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        set_app(self)

        app = self

        self.scene = []
        self.player = Player(self)
        self.scene.append(self.player)

        self.backgrounds = self.gen_background()

        self.enemy_manager = EnemyManager(self)
        self.enemies = self.gen_enemies(self.scene)
        self.bullet_count = 0

        self.taskMgr.add(self.update, "update")

        self.mouse_pos = Point2(0,0)

        self.set_keys()

    def camera_task(self):    
        self.camera.setPos(self.player.position.x, self.player.position.y , 20)
        self.camera.setHpr(0,-90,0)

    def get_cam(self):
        return self.camera.getPos()

    def set_keys(self):
        self.accept("a", self.player.move_left, [True])
        self.accept("a-up", self.player.move_left, [False])

        self.accept("d", self.player.move_right, [True])
        self.accept("d-up", self.player.move_right, [False])

        self.accept("w", self.player.move_up, [True])
        self.accept("w-up", self.player.move_up, [False])

        self.accept("s", self.player.move_down, [True])
        self.accept("s-up", self.player.move_down, [False])

        self.accept("mouse1", self.player.activate, [])

    def update(self, task):
        if(self.mouseWatcherNode.hasMouse()):
            self.mouse_pos.x = self.mouseWatcherNode.getMouseX()
            self.mouse_pos.y = self.mouseWatcherNode.getMouseY()

        self.camera_task()
        for entity in self.scene:
            entity.update(task.time)
        self.camera_task()
        return Task.cont

    def gen_enemies(self, scene):
        enemies = []
        for i in range(randint(1,100)):
        #for i in range(1):
            enemy = Enemy(Point3(uniform(5,40), uniform(5,40), 0), i, self, self.enemy_manager)
            #enemy = Enemy(Point3(5.0,5.0,0.0), i, self)
            enemies.append(enemy)
            scene.append(enemy)

    # make this configurable
    def gen_background(self):
        bg_x = 5
        bg_y = 5

        tile_count = 10

        backgrounds = []

        for i in range(10):
            for j in range(10):
                backgrounds.append(load_object("grass", pos = Point2(i*bg_x, j*bg_y), transparency = False, scale = 5))

        return backgrounds

    # probably put this here since it's creating scene entities?
    def spawn_bullet(self, player):
        self.scene.append(Bullet(self,player,self.bullet_count))





if __name__ == "__main__":
    app = Alem()
    app.run()
