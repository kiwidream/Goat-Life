import pyglet
import sys
import random
from drawable import Drawable

class Particle(Drawable):

  def __init__(self, game, tx, ty, group, type, decay, vx, vy, vz):
    super().__init__(game, tx, ty)
    self.init_sprite('particle_'+type+'.png', group)
    self.vx, self.vy, self.vz = vx, vy, vz
    self.decay = self.max_decay = decay
    self.update_dt = 0

  def update(self, dt):
    self.tx += self.vx * dt
    self.ty += self.vy * dt
    self.z += self.vz * dt

    self.need_pos_update = True

    self.decay -= dt

    self.update_dt += dt

    if len(self.sprites) > 0 and self.update_dt > 0.05:
      self.update_dt = 0
      self.sprites[0].opacity = max(int(255 * self.decay / self.max_decay), 0)
      self.sprites[0].group = self.game.world.group_for(self.ty-0.1)

    if self.decay <= 0:
      self.needs_deletion = True