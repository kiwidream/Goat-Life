import pyglet
import sys
import random
import math
from drawable import Drawable
from particle import Particle

class ParticleGroup(Drawable):

  def __init__(self, game, rtx, rty, z, group, type, decay, lifetime, spawn_rate, vx=0, vy=0, vz=0, rx=0, ry=0, rvx=0, rvy=0, do_rot=False, bullet=False, spawned_by=None, friction=0.985):
    tx = 0
    ty = 0
    super().__init__(game, tx, ty)
    self.spawn_period = 1 / spawn_rate
    self.spawned_by = spawned_by
    self.spawn_dt = self.spawn_period
    self.spawning = True
    self.particles = []
    self.type = type
    self.lifetime = lifetime
    self.decay = decay
    self.friction = friction
    self.group = group
    self.do_rot = do_rot
    self.rtx = rtx
    self.rty = rty
    self.base_tx = 0
    self.base_ty = 0
    self.z = z
    self.vx = vx
    self.vy = vy
    self.vz = vz
    self.rvx = rvx
    self.rvy = rvy
    self.rx = rx
    self.ry = ry
    self.bullet = bullet

  def update(self, dt):
    self.tx = self.base_tx + self.rtx
    self.ty = self.base_ty + self.rty

    if self.spawning:
      self.spawn_dt += dt
      self.lifetime -= dt

      if self.lifetime <= 0:
        self.spawning = False

    elif len(self.particles) == 0:
      self.needs_deletion = True

    if self.spawn_dt >= self.spawn_period:
      self.spawn_dt = 0
      vy = self.vy + (random.random() - 0.5) * self.rvy
      vz = self.vz
      vx = self.vx + (random.random() - 0.5) * self.rvx
      offset_tx = (random.random() - 0.5) * self.rx
      offset_ty = (random.random() - 0.5) * self.ry
      self.particles.append(Particle(self.game, self.tx + offset_tx, self.ty + offset_ty, self.z, self.group, self.type, self.decay, vx, vy, vz, self.do_rot, self.bullet, self.spawned_by, self.friction))

    Drawable.handle_deletion(self.particles)

    for particle in self.particles:
      particle.update(dt)

  def draw(self):
    for particle in self.particles:
      particle.draw()

  def delete(self):
    for particle in self.particles:
      particle.delete()

    super().delete()