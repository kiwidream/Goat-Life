import pyglet
import sys
import random
from drawable import Drawable
from entity import Entity
from tile import Tile
from grass_tuft import GrassTuft
from pyglet.window import key

class DungeonEntry(Entity):

  def __init__(self, game, tx, ty, group):
    super().__init__(game, tx, ty, group)
    self.progress = 0
    self.progress_dt = 0
    self.char_dt = 0
    self.group = group
    self.do_bounce = False
    self.do_coll = False
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
    sprite = self.get_visible_sprite()
    sprite.group = self.game.world.group_for(self.ty + 0.1)

    if self.progress == 3 and self.game.world.state_dt > 4 and self.remove_character and self.char_dt <= 0 and self.game.world.progression == self.game.world.FREE_ROAM:
      if abs(self.game.world.character.tx - self.tx) < 0.6 and abs(self.game.world.character.ty - self.ty - 0.75) < 0.6:
        if len(self.game.world.textbox.text) == 0 or self.game.keys[key.E] or self.game.keys[key.Q]:
          self.game.world.textbox.text = ["Press E to enter the crevice. Press Q to sacrifice another goat."]
          self.game.world.textbox.faces = [None]
          if self.game.keys[key.E]:
            self.game.world.move_to = self.game.world.DUNGEON
          if self.game.keys[key.Q]:
            self.game.world.sacrifice_mode = True

    if self.progress >= 2:
      if self.remove_character and self.char_dt > 0:
        self.char_dt -= dt
      elif self.char_dt < 2:
        self.char_dt += dt

      state = 1 if self.game.world.sacrifice_mode else 0
      self.sprites[self.char_i[1-state]].visible = False
      self.sprites[self.char_i[state]].visible = True
      self.sprites[self.char_i[state]].group = self.game.world.group_for(self.ty + (self.char_dt * 8 + 4) / self.game.TILE_HEIGHT)
      self.sprites[self.char_i[state]].opacity = int(max(min(255, self.char_dt * 150), 0))
      self.sprites_rel[self.char_i[state]] = (7, self.char_dt * 8 + 4)
      self.need_pos_update = True


    super().update(dt)