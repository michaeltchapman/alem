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
    secondary_switch = False

    def __init__(self, app):
        self.position = Point3(-30,-30,0)

        #upgradeable stats
        self.hp = 100
        self.move_speed = 0.9
        self.fire_rate = 0.1
        self.build_rate = 1.0
        self.fire_arcs = 1
        self.bullet_speed = 1.2
        self.bullet_explodesize = 0.5
        self.bullet_damage = 10
        self.bullet_scale = 0.1

        self.score = 0
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

        #self.cn.show()

        self.cqueue = CollisionHandlerQueue()
        app.cTrav.addCollider(self.cn, self.cqueue)

        self.cn.node().setIntoCollideMask(BitMask32(0x00))
        self.cn.node().setFromCollideMask(BitMask32(0x01))

        self.last_activated = 0.0
        self.last_built = 0.0

        self.rifle_sound = app.loader.loadSfx('sounds/rifle2.ogg')
        self.rifle_sound.setVolume(0.2)

    def update(self, timer):
        if self.cqueue.getNumEntries() != 0:
            self.np.setColorScale(1.0, self.hp / 100.0, self.hp / 100.0, 1.0)
        for i in range(self.cqueue.getNumEntries()):
            collided_name = self.cqueue.getEntry(i).getIntoNodePath().getName()
            # enemy is attacking us
            if collided_name[0] == 'e':
                self.app.enemy_manager.handle_collision(collided_name, self, timer)
                #self.cqueue.getEntry(i).getIntoNodePath().getParent().apply_effect(self,timer)
                # TODO play sound

            # pick up item    
            if collided_name[0] == 'i':
                self.app.item_manager.pickup(collided_name, self)
                print "hp %f" % self.hp
                print "move_speed %f" % self.move_speed
                print "fire_rate %f" % self.fire_rate
                print "fire_arcs %f" % self.fire_arcs
                print "bullet_speed %f" % self.bullet_speed
                print "bullet_explodesize %f" % self.bullet_explodesize
                print "bullet_damage %f" % self.bullet_damage
                
        if self.activate_switch and self.last_activated - timer + self.fire_rate < 0.0:
            self.app.bullet_manager.create_bullet(self, self.bullet_speed, self.bullet_scale, self.bullet_damage)
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

        # need the click position for tree palcement
        if self.secondary_switch and self.last_built - timer + self.build_rate < 0.0 and self.souls != 0:
            self.app.tree_manager.add_tree(Point3(near.x*20, near.z*20, 0) + self.np.getPos(), self.souls)
            self.last_built = timer
            self.souls = 0

        if self.hp < 0.0 and self.dead == False:
            self.dead = True
            self.app.scene.remove(self)

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

    def build(self, switch):
        self.secondary_switch = switch




