import pyglet
import sys
import random
import math
from drawable import Drawable
from pyglet.window import key
from entity import Entity

class Character(Entity):

  DOWN = 4
  UP = 5
  RIGHT = 6
  LEFT = 7

  def __init__(self, game, tx, ty, group):
    super().__init__(game, tx, ty, group)
    self.particle_hitbox = (0,0,7,18)
    self.speed = 1.5
    self.level = 1
    self.xp = 0
    self.direction = self.DOWN
    for i in range(4, 8):
      self.init_sprite('character_p_'+str(i)+'.png', group)

    self.hitbox = (0,0,7,3)

  def update(self, dt):
    super().update(dt)
    vel_x = 0
    vel_y = 0

    if self.game.world.progression != self.game.world.TITLE and self.game.world.progression != self.game.world.TITLE_COMPLETE:
      if self.game.keys[key.D]:
        vel_x = self.speed
        self.direction = self.RIGHT
      elif self.game.keys[key.A]:
        vel_x = -self.speed
        self.direction = self.LEFT

      if self.game.keys[key.W]:
        vel_y = self.speed
        self.direction = self.UP
      elif self.game.keys[key.S]:
        vel_y = -self.speed
        self.direction = self.DOWN

    if vel_x != 0 or vel_y != 0:
      angle = math.atan2(vel_y, vel_x)
      self.vx = math.cos(angle) * self.speed
      self.vy = math.sin(angle) * self.speed
    else:
      self.vx = 0
      self.vy = 0

    self.set_visible_sprite(self.direction-4)
    sprite = self.get_visible_sprite()

    sprite.group = self.game.world.group_for(self.ty - 1)

    if self.xp > 100:
      self.level += 1
      self.xp = 0