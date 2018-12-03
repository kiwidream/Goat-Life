import pyglet
import sys
import random
import math
from drawable import Drawable

class Particle(Drawable):

  def __init__(self, game, tx, ty, z, group, type, decay, vx, vy, vz, do_rot, bullet, spawned_by, friction):
    super().__init__(game, tx, ty)
    self.z = z
    self.friction = friction
    self.init_sprite('particle_'+type+'.png', group)
    self.vx, self.vy, self.vz = vx, vy, vz
    self.decay = self.max_decay = decay
    self.update_dt = 0
    self.do_rot = do_rot
    self.bullet = bullet
    self.spawned_by = spawned_by

  def update(self, dt):
    self.tx += self.vx * dt
    self.ty += self.vy * dt
    self.z += self.vz * dt
    self.z = max(self.z, 0)

    self.vx *= self.friction
    self.vy *= self.friction

    self.need_pos_update = True

    self.decay -= dt

    self.update_dt += dt

    if len(self.sprites) > 0 and self.update_dt > 0.05:
      self.update_dt = 0
      if self.do_rot:
        angle = math.atan2(self.vy, self.vx)
        self.sprites[0].rotation = -angle / math.pi * 180 - 90

      self.sprites[0].opacity = max(int(255 * self.decay / self.max_decay), 0)
      self.sprites[0].group = self.game.world.group_for(self.ty - 2)

    if self.decay <= 0:
      self.needs_deletion = True

    if self.bullet and len(self.sprites) > 0 and not self.needs_deletion:
      offset = self.game.dungeon_offset / self.game.TILE_WIDTH if self.game.world.state == self.game.world.DUNGEON else 0

      sprite = self.sprites[0]
      xa2, ya2, xb2, yb2 = (0, 0, sprite.width, sprite.height)
      xa2 += (self.tx - offset) * self.game.TILE_WIDTH
      ya2 += (self.ty - offset) * self.game.TILE_WIDTH
      xb2 += (self.tx - offset) * self.game.TILE_WIDTH
      yb2 += (self.ty - offset) * self.game.TILE_WIDTH
      hitbox2 = (xa2, ya2, xb2, yb2)

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

      ptx = self.tx - offset
      pty = self.ty - offset

      for tx in range(self.game.world.WIDTH[self.game.world.state]):
        for ty in range(self.game.world.HEIGHT[self.game.world.state]):
          tile = self.game.world.tile_at(tx, ty, self.game.world.state)
          if tile:
            for entity in tile.entities + [self.game.world.character]:
              if entity.entity_i == self.spawned_by or entity.particle_hitbox is None:
                continue

              etx = entity.tx - offset
              ety = entity.ty - offset

              xa1, ya1, xb1, yb1 = entity.particle_hitbox
              xa1 += etx * self.game.TILE_WIDTH
              ya1 += ety * self.game.TILE_WIDTH
              xb1 += etx * self.game.TILE_WIDTH
              yb1 += ety * self.game.TILE_WIDTH
              hitbox1 = (xa1, ya1, xb1, yb1)

              sys.stdout.flush()

              if self.game.aabb_intersects(hitbox1, hitbox2):
                entity.shove(None, self.vx, -self.vy)
                entity.inflict_damage(self, 1)
                self.needs_deletion = True
                return