from random import randint, random, uniform
from math import atan2, degrees, radians, sin, cos

from panda3d.core import Vec3, Vec4, CollisionNode, CollisionSphere, CollisionHandlerQueue, BitMask32, Point3
from panda3d.ai import AIWorld, AICharacter

from direct.particles.Particles import Particles
from direct.particles.ParticleEffect import ParticleEffect
from direct.particles.ForceGroup import ForceGroup
from panda3d.physics import BaseParticleEmitter,BaseParticleRenderer,PointParticleRenderer


from direct.actor.Actor import Actor

class EnemyManager():
    def __init__(self, app):
        self.model = Actor('models/panda-model', {"walk" : "models/panda-walk4"})
        self.model.setHpr(0,0,0)
        self.model.setPos(0,0,0)
        self.model.setScale(0.01)
        self.model.setPlayRate(2.0, "walk")
        self.model.loop("walk")
        self.model.hide()

        self.enemies = {}

    def add_instance(self,enemy):
        self.model.show()
        self.model.instanceTo(enemy.np)
        self.enemies[enemy.cn.getName()] = enemy

    def handle_collision(self, enemy, target, timer):
        self.enemies[enemy].apply_effect(target, timer)

class Enemy():
    def __init__(self, pos, index, app, manager, level, style):
        self.position = pos
        self.app = app
        self.np = app.render.attachNewNode("enemy%d" % index)

        if style == 1:
            self.np.setColorScale(1.0, 1.0, 1.0, 1.0)
            self.movespeed = 2.5
            self.max_movespeed = 30
        else:
            self.movespeed = 0.5
            self.max_movespeed = 25

        if style == 2:
            self.activate_delay = 0.01
            self.np.setColorScale(0.6, 1.0, 1.0, 1.0)
        else:
            self.activate_delay = 0.1

        if style == 3:
            self.hp = 50 * level
            self.np.setColorScale(0.0, 1.0, 0.5, 1.0)
        else:
            self.hp = 100 * level

        if style == 4:
            self.damage = 20
            self.np.setColorScale(1.0, 1.0, 0.0, 1.0)
        else:
            self.damage = 10

        self.dead = 0.0
        self.level = level
        self.style = style
        self.particle_clean = False

        # this allows us to detach the instance nodepath
        # on death, but keep one with no model to attach particle effects
        self.dnp = app.render.attachNewNode("enemy_top%d" % index)

        self.np.setPos(self.position)

        self.np.setHpr(uniform(1,360),0,0)
        self.np.setScale(level)

        colsize = 3.0
        self.cn = self.np.attachNewNode(CollisionNode('enemy_cn_%d' % index))
        self.cs0 = CollisionSphere(0.0, colsize/2,0.0,colsize)
        self.cs1 = CollisionSphere(0.0, -colsize/2,0.0,colsize)
        self.cs2 = CollisionSphere(0.0, -colsize/3*4,0.0,colsize/2)
        self.cn.node().addSolid(self.cs0)
        self.cn.node().addSolid(self.cs1)
        self.cn.node().addSolid(self.cs2)
        #self.cn.show() # debug

        self.cqueue = CollisionHandlerQueue()
        app.cTrav.addCollider(self.cn, self.cqueue)

        self.cn.node().setIntoCollideMask(BitMask32(0x01))
        self.cn.node().setFromCollideMask(BitMask32(0x10))

        self.last_activated = 0.0

        manager.add_instance(self)


        # name, nodepath, mass, move_force, max_force
        self.ai_char = AICharacter('enemy_ai_%d' % index, self.np, 100, self.movespeed, self.max_movespeed)
        app.ai_world.addAiChar(self.ai_char)
        self.ai_b = self.ai_char.getAiBehaviors()
        self.ai_b.pursue(app.player.np)

        self.load_particle_config()
    
    def update(self, time):

        a = 0
        # Handle collsions
        for i in range(self.cqueue.getNumEntries()):
           collided_name = self.cqueue.getEntry(i).getIntoNodePath().getName()
           #handle bullets
           if collided_name[0] == 'b': 
               bullet = self.app.bullet_manager.get_bullet(collided_name)
               bullet.apply_effect(self)
               self.app.bullet_manager.remove_bullet(collided_name)

        if self.cqueue.getNumEntries() != 0:
            self.np.setColorScale(1.0, self.hp / 100.0, self.hp / 100.0, 1.0)
       
        """
        desired = self.app.player.position - self.np.getPos()
        angle = degrees(atan2(desired.y, desired.x))
        
        hpr = self.np.getHpr()
        if hpr.x > 360:
            hpr.x = hpr.x - 360
        if hpr.x < -360:
            hpr.x = hpr.x + 360

        diff = angle - hpr.x 

        if diff > 180.0:
            diff = diff - 360

        if diff < -180.0:
            diff = diff + 360

        if diff > 5.0:
            diff = 5.0
        if diff < -5.0:
            diff = -5.0

        new = Vec3(diff, 0, 0) + hpr
        #self.np.setHpr(new)
        
        # move forward
        r = radians(new.x)
        curr = self.np.getPos()
        diff = Vec3(self.movespeed * cos(r), self.movespeed * sin(r), 0)
        self.np.setPos(curr + diff)"""

        if self.hp < 0.0 and self.dead == 0.0:
            self.dead = time 
            self.app.scene.remove(self)
            # Create particle effect before we go
            self.dnp.setPos(self.np.getPos())
            self.particles.start(parent = self.dnp, renderParent = self.app.render)
            self.np.detachNode()

            # Drop some loot
            self.app.item_manager.add_item(self.np.getPos(), "soul", self.level)
            # Give the player some points
            self.app.player.score = self.app.player.score + 100

    def apply_effect(self, target, timer):
        if self.last_activated - timer + self.activate_delay < 0.0:
            self.last_activated = timer
            target.hp = target.hp - self.damage
        if target.np.getName()[0] == 't':
            target.pursuers.append(self)
            #self.ai_b = self.ai_char.getAiBehaviors()
            #self.ai_b.pursue(self.np.getPos())
            self.ai_b.pauseAi("pursue")

    def load_particle_config(self):
        self.particles = ParticleEffect()
        self.particles.reset()
        self.particles.setPos(0.000, 0.000, 0.000)
        self.particles.setHpr(0.000, 0.000, 0.000)
        self.particles.setScale(1.000, 1.000, 1.000)
        p0 = Particles('particles-1')
        # Particles parameters
        p0.setFactory("PointParticleFactory")
        p0.setRenderer("SpriteParticleRenderer")
        p0.setEmitter("SphereVolumeEmitter")
        p0.setPoolSize(20)
        p0.setBirthRate(0.0100)
        p0.setLitterSize(20)
        p0.setLitterSpread(0)
        p0.setSystemLifespan(1.0100)
        p0.setLocalVelocityFlag(1)
        p0.setSystemGrowsOlderFlag(1)
        # Factory parameters
        p0.factory.setLifespanBase(1.0000)
        p0.factory.setLifespanSpread(0.0000)
        p0.factory.setMassBase(1.0000)
        p0.factory.setMassSpread(0.0100)
        p0.factory.setTerminalVelocityBase(1200.0000)
        p0.factory.setTerminalVelocitySpread(0.0000)
        # Point factory parameters
        # Renderer parameters
        p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAOUT)
        p0.renderer.setUserAlpha(0.05)
        # Sprite parameters
        p0.renderer.setTexture(self.app.loader.loadTexture('effects/dust.png'))
        p0.renderer.setColor(Vec4(1.00, 0.10, 0.10, 0.50))
        p0.renderer.setXScaleFlag(2)
        p0.renderer.setYScaleFlag(2)
        p0.renderer.setAnimAngleFlag(0)
        p0.renderer.setInitialXScale(0.100 * self.level)
        p0.renderer.setFinalXScale(0.200 * self.level)
        p0.renderer.setInitialYScale(0.100 * self.level)
        p0.renderer.setFinalYScale(0.200 * self.level)
        p0.renderer.setNonanimatedTheta(0.0000)
        p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPBLENDLINEAR)
        p0.renderer.setAlphaDisable(0)
        # Emitter parameters
        p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        p0.emitter.setAmplitude(1.0000)
        p0.emitter.setAmplitudeSpread(0.0000)
        p0.emitter.setOffsetForce(Vec3(0.0000, 0.0000, 0.0000))
        p0.emitter.setExplicitLaunchVector(Vec3(1.0000, 0.0000, 0.0000))
        p0.emitter.setRadiateOrigin(Point3(0.0000, 0.0000, 0.0000))
        # Sphere Volume parameters
        p0.emitter.setRadius(0.1000)
        self.particles.addParticles(p0)
        f0 = ForceGroup('gravity')
        # Force parameters
        self.particles.addForceGroup(f0)
