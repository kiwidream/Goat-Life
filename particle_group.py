import pyglet
import sys
import random
import math
from drawable import Drawable
from particle import Particle

class ParticleGroup(Drawable):

  def __init__(self, game, tx, ty, group, type, decay, lifetime, spawn_rate, spawn_angle, variance, rx=0, ry=0):
    super().__init__(game, tx, ty)
    self.spawn_period = 1 / spawn_rate
    self.spawn_angle = spawn_angle
    self.spawn_angle_variance = variance
    self.spawn_dt = 0
    self.spawning = True
    self.particles = []
    self.type = type
    self.lifetime = lifetime
    self.decay = decay
    self.group = group
    self.rx = rx
    self.ry = ry

  def update(self, dt):

    if self.spawning:
      self.spawn_dt += dt
      self.lifetime -= dt

      if self.lifetime <= 0:
        self.spawning = False

    elif len(self.particles) == 0:
      self.needs_deletion = True

    if self.spawn_dt >= self.spawn_period:
      self.spawn_dt = 0
      vy = 0
      vz = 10
      vx = math.cos(self.spawn_angle + (random.random() - 0.5) * self.spawn_angle_variance) * 1
      offset_tx = (random.random() - 0.5) * self.rx
      offset_ty = (random.random() - 0.5) * self.ry
      self.particles.append(Particle(self.game, self.tx + offset_tx, self.ty + offset_ty, self.group, self.type, self.decay, vx, vy, vz))
      sys.stdout.flush()

    Drawable.handle_deletion(self.particles)

    for particle in self.particles:
      particle.update(dt)

  def draw(self):
    for particle in self.particles:
      particle.draw()