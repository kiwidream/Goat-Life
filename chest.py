import pyglet
import sys
import random
from drawable import Drawable
from pyglet.window import key
from water_gem import WaterGem
from fire_gem import FireGem
from earth_gem import EarthGem
from grass_seeds import GrassSeeds
from spell import Spell
from spell_scroll import SpellScroll
from goat_skull import GoatSkull

class Chest(Drawable):

  TOP = 0
  LEFT = 2
  RIGHT = 4
  BOTTOM = 6

  STARTER = 0
  RANDOM = 1

  OFFSET = {
    0: (7, 12),
    2: (2, 8),
    4: (26, 8),
    6: (8, 4)
  }

  def __init__(self, game, tx, ty, group, orientation=0, chest_type=1):
    super().__init__(game, tx, ty)
    self.contents = []
    self.open = False
    self.orientation = orientation

    self.all_sprites_rel = self.OFFSET[orientation]

    self.chest_type = chest_type

    for i in range(orientation, orientation+2):
      s_i = self.init_sprite('chest_'+str(i)+'.png', group)
      self.sprites[s_i].visible = False

  def open_chest(self):
    if self.open or not self.game.world.inventory:
      return

    self.open = True

    self.game.world.character.xp += self.game.CHEST_XP

    if self.chest_type == self.STARTER:
      self.contents.append(WaterGem(self.game, 15))
      self.contents.append(SpellScroll(self.game, Spell.BASIC_WATER))
    elif self.chest_type == self.RANDOM:
      gems = [WaterGem, EarthGem, FireGem]

      while len(self.contents) == 0:
        count = random.randint(0, self.game.world.character.level*6)
        if count > 0:
          self.contents.append(GrassSeeds(self.game, count))

        for i in range(len(gems)):
          gem = gems[i]
          count = random.randint(0, max(self.game.world.character.level*4-i*2,0))
          if count > 0:
            self.contents.append(gem(self.game, count))

        if random.random() < 0.15:
          keys = list(Spell.TYPE.keys())
          random.shuffle(keys)

          for s_id in keys:
            if s_id not in self.game.world.inventory.obtained_spells:
              self.contents.append(SpellScroll(self.game, s_id))
              break

        if random.random() < self.game.world.character.level * 0.022:
          self.contents.append(GoatSkull(self.game, self.game.world.inventory.goal_skull_half))
          self.game.world.inventory.goal_skull_half = True

    text = "Contents: "
    for item in self.contents:
      text += str(item.count)+"x "+item.name+", "
      self.game.world.inventory.add_item(item)

    text = text[:-2]
    self.game.world.textbox.text.append(text)

    self.contents = []

  def update(self, dt):
    ox, oy = self.all_sprites_rel
    ox /= self.game.TILE_WIDTH
    oy /= self.game.TILE_HEIGHT
    if abs(self.game.world.character.tx - self.tx - ox) < 0.5 and abs(self.game.world.character.ty - self.ty - oy) < 0.5:
      self.open_chest()

    self.set_visible_sprite(int(self.open))
    sprite = self.get_visible_sprite()
    sprite.group = self.game.world.group_for(self.ty-0.5)
    super().update(dt)