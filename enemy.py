import pyglet
import sys
import random
import math
from drawable import Drawable
from pyglet.window import key
from entity import Entity

class Enemy(Entity):

  def __init__(self, game, tx, ty, group, override=False):
    super().__init__(game, tx, ty, group)
    if not override:
      for i in range(2):
        self.init_sprite('enemy_skeleton_'+str(i)+'.png', group)
    self.particle_hitbox = (2,-1,12,19)
    self.hitbox = (0,0,7,3)
    self.target_min_dist = 0.5
    self.target_max_dist = 2.5
    self.health = 3
    self.attack_dt = 1.6
    self.speed = random.random() * 0.4 + 0.25
    self.attack_period = 1.6
    self.anim_dead = 0
    self.target = self.game.world.character
    self.override_enemy = False

  def update(self, dt):
    super().update(dt)

    if self.override_enemy:
      return

    self.set_visible_sprite(1 if self.attack_dt < 0.5 else 0)
    sprite = self.get_visible_sprite()

    if self.dead:
      self.anim_dead += dt
      sprite.opacity = max(255 * (1 - self.anim_dead / 0.5), 0)
      if self.anim_dead >= 0.5:
        self.needs_deletion = True
        self.game.world.character.xp += self.game.KILL_XP

    if self.attack_dt < self.attack_period:
      self.attack_dt += dt

    if self.target_reached:
      if self.attack_dt >= self.attack_period:
        self.target.shove(self)
        self.target.inflict_damage(self, 1)
        self.attack_dt = 0

    sprite.group = self.game.world.group_for(self.ty - 1)