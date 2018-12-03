import pyglet
import sys
import random
import math
from drawable import Drawable
from pyglet.window import key
from enemy import Enemy
from spell import Spell

class Mage(Enemy):

  def __init__(self, game, tx, ty, group):
    super().__init__(game, tx, ty, group, True)
    for i in range(2):
      self.init_sprite('character_d_'+str(i)+'.png', group)
    self.particle_hitbox = (2,-1,14,16)
    self.hitbox = (0,0,7,3)
    self.target_min_dist = 1
    self.target_max_dist = 3
    self.health = 8
    self.attack_dt = 1.6
    self.speed = random.random() * 0.4 + 0.3
    self.attack_period = 1.2
    self.anim_dead = 0
    self.target = self.game.world.character
    self.override_enemy = True
    self.spells = [Spell(game, i) for i in list(Spell.TYPE.keys())]

  def update(self, dt):
    super().update(dt)

    self.set_visible_sprite(1 if self.attack_dt < 0.5 else 0)
    sprite = self.get_visible_sprite()

    if self.dead:
      self.anim_dead += dt
      sprite.opacity = max(255 * (1 - self.anim_dead / 0.5), 0)
      if self.anim_dead >= 0.5:
        self.needs_deletion = True
        self.game.world.character.xp += self.game.KILL_XP * 2

    if self.attack_dt < self.attack_period:
      self.attack_dt += dt

    if self.target_reached:
      if self.attack_dt >= self.attack_period:
        rs = random.randint(0, len(self.spells)-1)
        offset = self.game.dungeon_offset / self.game.TILE_WIDTH
        self.spawn_spell(self.target.tx - offset, self.target.ty - offset, self.spells[rs])
        self.attack_dt = 0

    sprite.group = self.game.world.group_for(self.ty - 1)