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
from tree import Tree


from loader import set_app, load_object

import sys
import cProfile

class Alem(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        base.setFrameRateMeter(True)

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

        self.music = self.loader.loadSfx('sounds/onegameamonthjan.ogg')
        self.music.setVolume(0.2)
        self.music.play()

        self.box = loader.loadModel("models/box")
        self.box.setPos(3,3,0)
        self.box.setScale(1)
        self.box.reparentTo(self.render)

        #self.tree = Tree(self,Point3(7,1,0),1)
        self.trees = self.gen_trees()


    def camera_task(self):    
        self.camera.setPos(self.player.position.x, self.player.position.y , 400)
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

        self.accept("escape", sys.exit)

    def update(self, task):
        if(self.mouseWatcherNode.hasMouse()):
            self.mouse_pos.x = self.mouseWatcherNode.getMouseX()
            self.mouse_pos.y = self.mouseWatcherNode.getMouseY()

        self.camera_task()
        # Bullet reaping
        self.bullet_manager.update(task.time)
        self.ai_world.update()
        self.cTrav.traverse(self.render)
        for entity in self.scene:
            entity.update(task.time)
        self.camera_task()
        self.update_hud()
        return Task.cont


    def update_hud(self):
        self.hud.GetElementById("health").last_child.text = "%d" % self.player.hp
        self.hud.GetElementById("score").last_child.text = "%d" % self.player.score

        self.hud.GetElementById("wood").last_child.text = "%d" % self.player.wood
        self.hud.GetElementById("stone").last_child.text = "%d" % self.player.stone
        self.hud.GetElementById("souls").last_child.text = "%d" % self.player.souls


    # should move creation into the manager
    def gen_enemies(self, scene):
        enemies = []
        for i in range(randint(50,100)):
        #for i in range(1):
            enemy = Enemy(Point3(uniform(-400,400), uniform(-400,400), 0), i, self, self.enemy_manager, uniform(1,3), randint(1,4))
            #enemy = Enemy(Point3(30.0,30.0,0.0), i, self, self.enemy_manager, 1, 1)
            enemies.append(enemy)
            scene.append(enemy)
        return enemies    

    # make this configurable
    def gen_background(self):
        bg_x = 50
        bg_y = 50

        tile_count = 20

        backgrounds = []

        self.bgnp = self.render.attachNewNode("bg")

        for i in range(-tile_count,tile_count):
            for j in range(-tile_count,tile_count):
                backgrounds.append(load_object("grass", pos = Point2(i*bg_x, j*bg_y), transparency = False, scale = 50))
        for background in backgrounds:
            background.reparentTo(self.bgnp)

        self.bgnp.flattenStrong()    
        return backgrounds

    def gen_trees(self):
        trees = []
        for i in range(randint(20,40)):
            trees.append(Tree(self, Point3(uniform(-100,100), uniform(-100,100), 0), i))
        return trees    


    # probably put this here since it's creating scene entities?
    def spawn_bullet(self, player):
        self.bullet_manager.create_bullet(player)

def _wrap_with_profiling(entry_point):
    """
    run the given argumentless function entry_point using the python profiler

    trap any SystemExits and KeyboardInterrupts so we can
    still spam the profing results to stdout
    """
    def wrapped_entry_point():
        import pstats
        import cProfile
        p = cProfile.Profile()
        def safety_net(entry_point):
            try:
                entry_point(arg)
            except SystemExit:
                pass
            except KeyboardInterrupt:
                pass
        p.runcall(lambda : safety_net(entry_point))
        s = pstats.Stats(p)
        s.sort_stats('cumulative').print_stats(25)
    return wrapped_entry_point

if __name__ == "__main__":
    app = Alem()
    cProfile.run('app.run()', '/home/mc/projects/alem/alem/profile')
    #app.run()