#!/usr/bin/python

from math import pi, sin, cos
from direct.showbase.ShowBase import ShowBase
from direct.task import Task

from random import randint, random, uniform

from panda3d.core import Point2, Point3, Texture, CollisionTraverser
from panda3d.rocket import LoadFontFace, RocketRegion, RocketInputHandler
from panda3d.ai import AIWorld, AICharacter


from player import Player
from enemy import Enemy, EnemyManager
from bullet import Bullet, BulletManager


from loader import set_app, load_object

class Alem(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        set_app(self)

        app = self

        # Rocket Gui
        LoadFontFace("gui/Raleway.otf")
        self.region = RocketRegion.make('pandaRocket', app.win)
        self.region.setActive(1)
        self.context = self.region.getContext()
        self.hud = self.context.LoadDocument('gui/hud.rml')
        ih = RocketInputHandler()
        app.mouseWatcher.attachNewNode(ih)
        self.region.setInputHandler(ih)
        self.hud.Show()

        self.cTrav = CollisionTraverser('coltrav')
        #self.cTrav.showCollisions(self.render)
        self.ai_world = AIWorld(render)

        self.enableParticles()

        self.scene = []
        self.player = Player(self)
        self.scene.append(self.player)

        self.backgrounds = self.gen_background()

        self.enemy_manager = EnemyManager(self)
        self.enemies = self.gen_enemies(self.scene)

        self.bullet_manager = BulletManager(self)
        self.bullet_count = 0

        self.taskMgr.add(self.update, "update")

        self.mouse_pos = Point2(0,0)

        self.set_keys()

        self.music = self.loader.loadSfx('sounds/onegameamonthjan.wav')
        self.music.setVolume(0.2)
        self.music.play()


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

        self.accept("mouse1", self.player.activate, [True])
        self.accept("mouse1-up", self.player.activate, [False])

    def update(self, task):
        if(self.mouseWatcherNode.hasMouse()):
            self.mouse_pos.x = self.mouseWatcherNode.getMouseX()
            self.mouse_pos.y = self.mouseWatcherNode.getMouseY()

        self.camera_task()
        self.ai_world.update()
        self.cTrav.traverse(self.render)
        for entity in self.scene:
            entity.update(task.time)
        self.camera_task()
        self.update_hud()
        return Task.cont


    def update_hud(self):
        self.hud.GetElementById("health").last_child.text = "%d" % self.player.hp

    # should move creation into the manager
    def gen_enemies(self, scene):
        enemies = []
        for i in range(randint(50,100)):
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
        self.bullet_manager.create_bullet(player)



if __name__ == "__main__":
    app = Alem()
    app.run()
