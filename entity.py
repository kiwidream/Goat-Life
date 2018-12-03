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
    self.entity_i = self.game.entity_count
    self.game.entity_count += 1
    self.dead = False
    self.target = None
    self.speed = 0.5
    self.group = group
    self.last_dx = 0
    self.last_dy = 0
    self.vx = 0
    self.vy = 0
    self.target_reached = False
    self.do_bounce = True
    self.hitbox = None
    self.seen_waste_seed = False
    self.target_min_dist = 0.1
    self.target_max_dist = 4
    self.health_anim_dt = 0.3
    self.health = 8
    self.attack_dt = 0
    self.attack_period = 1.6
    self.col = (255, 255, 255)
    self.shove_x = 0
    self.shove_y = 0
    self.target_update_dt = 0.15

  #self, game, tx, ty, z, group, type, decay, lifetime, spawn_rate, vx=0, vy=0, vz=0, rx=0, ry=0, rvx=0, rvy=0, friction=0.985
  def spawn_smoke(self):
    self.particle_groups.append(ParticleGroup(self.game, 0.4, -0.1, 10, self.group, 'smoke', 1.5, 10, 40, 0, 0, 15, 0.25, 0, 0.15, 0))

  def spawn_flames(self):
    dx = 0 if self.last_dx > 0 else 0.2
    self.particle_groups.append(ParticleGroup(self.game, dx, -0.1, 0, self.group, 'flame', 1, 5, 12, 0, 0, 10, 0.4, 0, 0.2, 0))

  def spawn_seeds(self, tx, ty):
    off = 0 if self.game.world.state == self.game.world.OVERWORLD else self.game.dungeon_offset / self.game.TILE_WIDTH
    dx = tx - self.tx + off
    dy = ty - self.ty + off - 0.2
    if off > 0 and not self.seen_waste_seed:
      self.seen_waste_seed = True
      self.game.world.textbox.text.append("I don't think I should waste seeds like this..")
      self.game.world.textbox.faces.append(0)
    self.particle_groups.append(ParticleGroup(self.game, -0.1+off, -0.2+off, 20, self.group, 'seed', 5, 1, 8, dx/2, dy/2, -8, 0, 0, 0.2, 0.2))

  def spawn_spell(self, tx, ty, spell):
    if self.game.world.state == self.game.world.OVERWORLD:
      return
    off = 0 if self.game.world.state == self.game.world.OVERWORLD else self.game.dungeon_offset / self.game.TILE_WIDTH
    dx = tx - self.tx + off - 0.1
    dy = ty - self.ty + off - 0.1

    angle = math.atan2(dy, dx)
    vx = math.cos(angle) * spell.speed
    vy = math.sin(angle) * spell.speed
    self.particle_groups.append(ParticleGroup(self.game, 0.1+off, -0.2+off, 10, self.group, 'spell_'+str(spell.id), 6, 10, 0.01, vx, vy, 0, 0.1, 0.1, 0, 0, True, True, self.entity_i))

  def inflict_damage(self, attacker, amount):
    self.health -= amount
    self.health_anim_dt = 0
    if self.health <= 0:
      self.dead = True

  def draw(self):
    for group in self.particle_groups:
      group.draw()

    super().draw()

  def shove(self, shover=None, dx=0, dy=0):
    if shover:
      dx = shover.tx - self.tx
      dy = shover.ty - self.ty

    angle = math.atan2(dy, dx)
    self.shove_x = math.cos(-angle) * 2
    self.shove_y = math.sin(-angle) * 2

  def update(self, dt):
    self.target_reached = False

    if self.do_bounce:
      self.anim_dt += dt
    sprite = self.get_visible_sprite()
    sprite.color = self.col

    red_color = (255, 160, 160)
    if self.health_anim_dt < 0.3:
      self.col = red_color
      self.health_anim_dt += dt
    elif self.col == red_color:
      self.col = (255, 255, 255)

    if self.anim_dt >= 0.8 and sprite:
      sprite.scale_y = int(self.stretched) * 0.06 + 1
      self.stretched = not self.stretched
      self.anim_dt = 0

    if self.target:
      self.target_update_dt += dt

    if self.target and self.target_update_dt >= 0.15:
      self.target_update_dt = random.random() * 0.075
      dx = self.target.tx - self.tx
      self.last_dx = dx
      dy = self.target.ty - self.ty - 0.1
      self.last_dy = dy

      if (abs(dx) > self.target_min_dist or abs(dy) > self.target_min_dist) and (abs(dx) < self.target_max_dist or abs(dy) < self.target_max_dist):
        angle = math.atan2(dy, dx)
        self.vx = math.cos(angle) * self.speed
        self.vy = math.sin(angle) * self.speed
      else:
        self.vx = 0
        self.vy = 0

      if abs(dx) <= self.target_min_dist and abs(dy) <= self.target_min_dist:
        self.target_reached = True

    Drawable.handle_deletion(self.particle_groups)

    for group in self.particle_groups:
      group.base_tx = self.tx - (512 if self.game.world.state == self.game.world.DUNGEON else 0)
      group.base_ty = self.ty - (512 if self.game.world.state == self.game.world.DUNGEON else 0)
      group.update(dt)

    self.shove_x *= 0.9
    self.shove_y *= 0.9

    self.move((self.vx + self.shove_x) * dt, 0)
    self.move(0, (self.vy + self.shove_y) * dt)

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
        if tile:
          for hitbox in tile.hitboxes:
            xa1, ya1, xb1, yb1 = hitbox
            xa1 += tile.tx * self.game.TILE_WIDTH
            ya1 += tile.ty * self.game.TILE_WIDTH
            xb1 += tile.tx * self.game.TILE_WIDTH
            yb1 += tile.ty * self.game.TILE_WIDTH
            hitbox1 = (xa1, ya1, xb1, yb1)
            if self.game.aabb_intersects(hitbox1, hitbox2):
              intersect = True
              self.tx -= dx
              self.ty -= dy
              break

          if intersect:
            break
