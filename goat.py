import pyglet
import sys
import random
from drawable import Drawable
import math
from particle_group import ParticleGroup

class Goat(Drawable):

  STANDING = 0
  EATING = [1, 2]
  CHEVRON = 3

  def __init__(self, game, tx, ty, group):
    super().__init__(game, tx, ty)
    self.anim_dt = random.random() * 0.8
    self.anim_eat_dt = 0
    self.anim_chevron_dt = 0
    self.stretched = False
    self.state = self.STANDING
    self.target_grass = None
    self.speed = 1
    self.anim_eating_offset = 0
    self.anim_eat2_dt = 0
    self.particle_group = None
    self.group = group

    for i in range(1, 4):
      self.init_sprite('goat_'+str(i)+'.png', group)

    self.init_sprite('chevron.png', group)
    self.sprites[self.CHEVRON].visible = False

  def spawn_flames(self):
    self.particle_group = ParticleGroup(self.game, self.tx, self.ty, self.group, 'flame', 1, 5, 20, math.pi / 2, math.pi / 6, 0.4)

  def draw(self):
    if self.particle_group:
      self.particle_group.draw()

    super().draw()

  def update(self, dt):
    self.set_visible_sprite(self.state)

    sprite = self.get_visible_sprite()
    self.anim_dt += dt
    last_dx = 0
    if self.anim_dt >= 0.8:
      sprite.scale_y = int(self.stretched) * 0.06 + 1
      self.stretched = not self.stretched
      self.anim_dt = 0

    if self.target_grass is None:
      rx = random.randint(-1, 1)
      ry = random.randint(-1, 1)
      tx = int(rx + self.tx)
      ty = int(ry + self.ty)
      tile = self.game.world.tile_at(tx, ty)

      if tile and tile.grass_tufts and len(tile.grass_tufts) > 0:
        self.target_grass = tile.grass_tufts[0]
    else:
      dx = self.target_grass.tx - self.tx
      last_dx = dx
      dy = self.target_grass.ty - self.ty - 0.1

      if abs(dx) > 0.1 and abs(dy) > 0.1:
        angle = math.atan2(dy, dx)
        self.tx += math.cos(angle) * self.speed * dt
        self.ty += math.sin(angle) * self.speed * dt
      else:
        self.state = self.EATING[self.anim_eating_offset]

        self.anim_eat2_dt += dt
        self.anim_eat_dt += dt

        if self.anim_eat2_dt > 1:
          self.anim_eat2_dt = 0
          self.anim_eating_offset = 1 - self.anim_eating_offset

        if self.anim_eat_dt > 1.5:
          self.target_grass.remaining_grass -= 1
          self.anim_eat_dt = 0

          if self.target_grass.remaining_grass == 0:
            self.target_grass.needs_deletion = True
            self.target_grass = None
            self.state = self.STANDING

    chevron_sprite = self.sprites[self.CHEVRON]
    chevron_sprite.visible = self.game.world.sacrifice_mode

    if self.game.world.sacrifice_mode:
      rel_y = math.sin(self.anim_chevron_dt * math.pi) * 2
      self.sprites_rel[self.CHEVRON] = (-5 if last_dx > 0 else 5, rel_y + 15)
      chevron_sprite.opacity = 255 if self.hovered else 90
      self.anim_chevron_dt += dt
      if self.anim_chevron_dt > 2:
        self.anim_chevron_dt = 0

    if last_dx > 0:
      sprite.scale_x = -1
      self.sprites_rel[self.visible_sprite] = (self.sprites[0].width // 2, 0)
    else:
      sprite.scale_x = 1
      self.sprites_rel[self.visible_sprite] = (0, 0)

    if self.particle_group:
      if self.particle_group.needs_deletion:
        self.particle_group = None
      else:
        self.particle_group.tx = self.tx + (0 if last_dx > 0 else 0.2)
        self.particle_group.ty = self.ty - 0.1
        self.particle_group.update(dt)

    self.need_pos_update = True

    self.group = new_group = self.game.world.group_for(self.ty)
    chevron_sprite.group, sprite.group = new_group, new_group