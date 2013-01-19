from panda3d.core import Point2, Point3, NodePath, CollisionNode
from panda3d.core import CollisionSphere, CollisionHandlerQueue, BitMask32, Texture
from math import atan2, pi, degrees
from sys import path

class Player():
    left_move = False
    right_move = False
    up_move = False
    down_move = False
    activate_switch = False

    move_speed = 0.9
    activate_delay = 0.07

    def __init__(self, app):
        self.position = Point3(-30,-30,0)
        self.hp = 100

        self.points = 0
        self.wood = 0
        self.stone = 0
        self.souls = 0

        self.dead = False
        self.np = app.render.attachNewNode("player")
        self.np.setPos(self.position)

        self.model = app.loader.loadModel('models/aneta')

        self.model.reparentTo(self.np)
        self.model.setScale(8.0)
        self.model.setPos(0,0,0)
        self.model.setHpr(90,0,0)
        self.app = app

        self.cn = self.np.attachNewNode(CollisionNode('player'))
        self.cs = CollisionSphere(0,0.0,0.0,4.0)
        self.cn.node().addSolid(self.cs)

        self.cn.show()

        self.cqueue = CollisionHandlerQueue()
        app.cTrav.addCollider(self.cn, self.cqueue)

        self.cn.node().setIntoCollideMask(BitMask32(0x00))
        self.cn.node().setFromCollideMask(BitMask32(0x01))

        self.last_activated = 0.0

        self.rifle_sound = app.loader.loadSfx('sounds/rifle2.wav')
        self.rifle_sound.setVolume(0.2)

    def update(self, timer):


        if self.cqueue.getNumEntries() != 0:
            self.np.setColorScale(1.0, self.hp / 100.0, self.hp / 100.0, 1.0)
        for i in range(self.cqueue.getNumEntries()):
            collided_name = self.cqueue.getEntry(i).getIntoNodePath().getName()
            if collided_name[0] == 'e':
                self.app.enemy_manager.handle_collision(collided_name, self, timer)
                
        if self.activate_switch and self.last_activated - timer + self.activate_delay < 0.0:
            self.app.spawn_bullet(self)
            self.last_activated = timer
            self.rifle_sound.play()

        if self.left_move:
            self.position.x = self.position.x - self.move_speed
        if self.right_move:
            self.position.x = self.position.x + self.move_speed
        if self.up_move:
            self.position.y = self.position.y + self.move_speed
        if self.down_move:
            self.position.y = self.position.y - self.move_speed

        self.np.setPos(self.position.x, self.position.y, 0)

        mouse = self.app.mouse_pos
        near = Point3()
        far = Point3()
        self.app.camLens.extrude(mouse, near, far)
        camp = self.app.camera.getPos()
        near *= 20

        if near.x != 0:
            # There's a wierd camera bug here.
            #angle = atan2(near.z + camp.y - self.position.y, near.x + camp.x - self.position.x)
            angle = atan2(near.z, near.x)
        else:
            angle = pi/2 

        self.angle = angle
        self.np.setHpr(degrees(angle), 0, 0)

        if self.hp < 0.0:
            self.dead = True

        return

    def move_left(self, switch):
        self.left_move = switch

    def move_right(self, switch):
        self.right_move = switch

    def move_up(self, switch):
        self.up_move = switch

    def move_down(self, switch):
        self.down_move = switch
    
    def activate(self, switch):
        self.activate_switch = switch





