import pyglet
import sys
import random
from drawable import Drawable
from entity import Entity
from tile import Tile
from grass_tuft import GrassTuft

class DungeonEntry(Entity):

  def __init__(self, game, tx, ty, group):
    super().__init__(game, tx, ty, group)
    self.progress = 0
    self.progress_dt = 0
    self.char_dt = 0
    self.group = group
    self.do_bounce = False
    self.remove_character = False
    self.spawn_smoke()
    for i in range(0, 4):
      s_i = self.init_sprite('entry_'+str(i)+'.png', group)
      self.sprites[s_i].visible = False

    self.char_i = [0,0]
    self.char_i[0] = self.init_sprite('character_d_0.png', group)
    self.char_i[1] = self.init_sprite('character_d_1.png', group)
    self.sprites[self.char_i[0]].visible = False
    self.sprites[self.char_i[1]].visible = False

  def update(self, dt):
    if self.progress < 3:
      self.progress_dt += dt
      if self.progress_dt > 2:
        self.progress += 1
        self.progress_dt = 0

    self.set_visible_sprite(self.progress)

    if self.progress >= 2:
      if self.remove_character and self.char_dt > 0:
        self.char_dt -= dt
      elif self.char_dt < 2:
        self.char_dt += dt

      state = 1 if self.game.world.sacrifice_mode else 0
      self.sprites[self.char_i[1-state]].visible = False
      self.sprites[self.char_i[state]].visible = True
      self.sprites[self.char_i[state]].opacity = int(max(min(255, self.char_dt * 150), 0))
      self.sprites_rel[self.char_i[state]] = (7, self.char_dt * 8 + 4)
      self.need_pos_update = True


    super().update(dt)