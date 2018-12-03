import pyglet
import sys
import random
from drawable import Drawable
from entity import Entity
import math
from particle_group import ParticleGroup

class Goat(Entity):

  STANDING = 0
  EATING = [1, 2]
  CHEVRON = 3

  def __init__(self, game, tx, ty, group):
    super().__init__(game, tx, ty, group)
    self.anim_eat_dt = 0
    self.anim_chevron_dt = 0
    self.anim_eating_offset = 0
    self.anim_eat2_dt = 0
    self.state = self.STANDING
    self.target_dt = 0

    self.dying = False
    self.dying_dt = 0
    self.hunger_dt = 0

    for i in range(1, 4):
      self.init_sprite('goat_'+str(i)+'.png', group)

    self.init_sprite('chevron.png', group)
    self.sprites[self.CHEVRON].visible = False

  def update(self, dt):
    super().update(dt)
    self.set_visible_sprite(self.state)

    sprite = self.get_visible_sprite()

    if self.dying and self.dying_dt < 4:
      self.state = self.STANDING
      self.do_bounce = False
      self.dying_dt += dt
      if self.dying_dt > 0.8:
        self.col = (50, 50, 50)

      if self.dying_dt > 1.5:
        sprite.opacity = int(max((4 - self.dying_dt) / 2.5 * 255, 0))
    elif self.dying and len(self.particle_groups) == 0:
      self.needs_deletion = True

    if not self.dying:
      if self.target is None:
        self.hunger_dt += dt
        if self.hunger_dt >= 30:
          self.dying = True
        self.target_dt += dt
        if self.target_dt > 0.4:
          self.target_dt = 0
          rx = random.randint(-1, 1)
          ry = random.randint(-1, 1)
          tx = int(rx + self.tx)
          ty = int(ry + self.ty)
          tile = self.game.world.tile_at(tx, ty)

          if tile and tile.grass_tufts and len(tile.grass_tufts) > 0:
            self.target = tile.grass_tufts[0]
      elif self.target_reached:
        self.state = self.EATING[self.anim_eating_offset]
        self.hunger = 0

        self.anim_eat2_dt += dt
        self.anim_eat_dt += dt

        if self.anim_eat2_dt > 1:
          self.anim_eat2_dt = 0
          self.anim_eating_offset = 1 - self.anim_eating_offset

        if self.anim_eat_dt > 1.5:
          self.target.remaining_grass -= 1
          self.anim_eat_dt = 0

          if self.target.remaining_grass == 0:
            self.target.needs_deletion = True
            self.target = None
            self.state = self.STANDING

    chevron_sprite = self.sprites[self.CHEVRON]
    chevron_sprite.visible = self.game.world.sacrifice_mode

    if self.game.world.sacrifice_mode:
      rel_y = math.sin(self.anim_chevron_dt * math.pi) * 2
      self.sprites_rel[self.CHEVRON] = (-5 if self.last_dx > 0 else 5, rel_y + 15)
      chevron_sprite.opacity = 255 if self.hovered else 90
      self.anim_chevron_dt += dt
      if self.anim_chevron_dt > 2:
        self.anim_chevron_dt = 0

    if self.last_dx > 0:
      sprite.scale_x = -1
      self.sprites_rel[self.visible_sprite] = (self.sprites[0].width // 2, 0)
    else:
      sprite.scale_x = 1
      self.sprites_rel[self.visible_sprite] = (0, 0)

    self.need_pos_update = True

    self.group = new_group = self.game.world.group_for(self.ty-1)
    chevron_sprite.group, sprite.group = new_group, new_group