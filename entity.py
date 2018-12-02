import pyglet
import sys
import random
from drawable import Drawable
import math
from particle_group import ParticleGroup

class Entity(Drawable):

  def __init__(self, game, tx, ty, group):
    super().__init__(game, tx, ty)
    self.anim_dt = random.random() * 0.8
    self.stretched = False
    self.particle_groups = []

    self.target = None
    self.speed = 2
    self.group = group
    self.last_dx = 0
    self.last_dy = 0
    self.vx = 0
    self.vy = 0
    self.target_reached = False
    self.do_bounce = True
    self.hitbox = None

  #self, game, tx, ty, z, group, type, decay, lifetime, spawn_rate, vx=0, vy=0, vz=0, rx=0, ry=0, rvx=0, rvy=0, friction=0.985
  def spawn_smoke(self):
    self.particle_groups.append(ParticleGroup(self.game, 0.4, -0.1, 10, self.group, 'smoke', 1.5, 10, 40, 0, 0, 15, 0.25, 0, 0.15, 0))

  def spawn_flames(self):
    dx = 0 if self.last_dx > 0 else 0.2
    self.particle_groups.append(ParticleGroup(self.game, dx, -0.1, 0, self.group, 'flame', 1, 5, 12, 0, 0, 10, 0.4, 0, 0.2, 0))

  def spawn_seeds(self, tx, ty):
    dx = tx - self.tx
    dy = ty - self.ty
    self.particle_groups.append(ParticleGroup(self.game, -0.1, -0.2, 20, self.group, 'seed', 5, 1, 8, dx/2, dy/2, -8, 0, 0, 0.2, 0.2))

  def draw(self):
    for group in self.particle_groups:
      group.draw()

    super().draw()

  def update(self, dt):
    self.target_reached = False
    if self.do_bounce:
      self.anim_dt += dt
    sprite = self.get_visible_sprite()

    if self.anim_dt >= 0.8 and sprite:
      sprite.scale_y = int(self.stretched) * 0.06 + 1
      self.stretched = not self.stretched
      self.anim_dt = 0

    if self.target:
      dx = self.target.tx - self.tx
      self.last_dx = dx
      dy = self.target.ty - self.ty - 0.1
      self.last_dy = dy

      if abs(dx) > 0.1 and abs(dy) > 0.1:
        angle = math.atan2(dy, dx)
        self.vx = math.cos(angle) * self.speed
        self.vy = math.sin(angle) * self.speed
      else:
        self.target_reached = True
        self.vx = 0
        self.vy = 0

    Drawable.handle_deletion(self.particle_groups)

    for group in self.particle_groups:
      group.base_tx = self.tx
      group.base_ty = self.ty
      group.update(dt)

    self.move(self.vx * dt, 0)
    self.move(0, self.vy * dt)

    self.need_pos_update = True

    super().update(dt)

  def move(self, dx, dy):
    self.tx += dx
    self.ty += dy
    intersect = False
    if self.hitbox and self.game.world.state == self.game.world.DUNGEON:
      dirs = {
        'N':  (0,1),
        'NW': (-1,1),
        'NE': (1,1),
        'W':  (-1,0),
        'E':  (1,0),
        'S':  (0,-1),
        'SE': (1,-1),
        'SW': (-1,-1),
        'NONE': (0,0)
      }
      offset = self.game.dungeon_offset / self.game.TILE_WIDTH

      xa2, ya2, xb2, yb2 = self.hitbox
      xa2 += (self.tx - offset) * self.game.TILE_WIDTH
      ya2 += (self.ty - offset) * self.game.TILE_WIDTH
      xb2 += (self.tx - offset) * self.game.TILE_WIDTH
      yb2 += (self.ty - offset) * self.game.TILE_WIDTH
      hitbox2 = (xa2, ya2, xb2, yb2)

      for (tdx, tdy) in dirs.values():
        tx = self.tx + tdx - offset
        ty = self.ty + tdy - offset
        tile = self.game.world.tile_at(tx, ty, self.game.world.DUNGEON)
        for hitbox in tile.hitboxes:
          xa1, ya1, xb1, yb1 = hitbox
          xa1 += tile.tx * self.game.TILE_WIDTH
          ya1 += tile.ty * self.game.TILE_WIDTH
          xb1 += tile.tx * self.game.TILE_WIDTH
          yb1 += tile.ty * self.game.TILE_WIDTH
          hitbox1 = (xa1, ya1, xb1, yb1)
          if self.aabb_intersects(hitbox1, hitbox2):
            intersect = True
            self.tx -= dx
            self.ty -= dy
            break

        if intersect:
          break

  def aabb_intersects(self, hitbox1, hitbox2):
    xa1, ya1, xb1, yb1 = hitbox1
    xa2, ya2, xb2, yb2 = hitbox2

    xt = xa1 < xb2 and xb1 > xa2
    yt = ya1 < yb2 and yb1 > ya2

    return xt and yt
