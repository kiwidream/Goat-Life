import pyglet
import sys
import random
from drawable import Drawable
from item import Item
from grass_seeds import GrassSeeds
from water_gem import WaterGem
from fire_gem import FireGem
from earth_gem import EarthGem
from spell import Spell

class Inventory(Drawable):

  WIDTH = 40

  def __init__(self, game, x, y, group):
    super().__init__(game, x, y, 0, True)
    self.group = group
    self.items = []
    self.batch = game.hud_batch
    self.bg_i = self.init_sprite('hud_bg.png', self.group)
    self.sel_bg_i = self.init_sprite('hud_bg.png', self.group)
    self.hov_bg_i = self.init_sprite('hud_bg.png', self.group)

    self.spell_bg_i = self.init_sprite('hud_bg.png', self.group)
    self.sel_spell_bg_i = self.init_sprite('hud_bg.png', self.group)

    self.sprites_rel[self.spell_bg_i] = (-260, 200)

    self.sprites_rel[self.sel_bg_i] = (200, 0)
    self.sprites_rel[self.hov_bg_i] = (200, 0)
    self.heart_i = self.init_sprite('heart.png', self.group)
    self.heart_label = None
    self.selected_i = None
    self.hovered_i = None
    self.selected_spell_i = None
    self.hovered_spell_i = None
    self.count_dt = 0
    self.spells = []
    self.obtained_spells = []
    self.goal_skull_half = False
    self.use_btn_i = self.init_sprite('btn_use.png', self.group)
    self.sprites_to_remove = []
    self.add_item(GrassSeeds(game, 25))

  def has_item(self, id, count):
    if count == 0:
      return True

    for item in self.items:
      if item.id == id and item.count >= count:
        return True

    return False

  def remove_item(self, id, dcount=1):
    removed_s_i = None
    found = False
    for i in range(len(self.items)):
      item = self.items[i]
      if item.id == id:
        found = True
        if item.count - dcount < 0:
          return False

        item.count -= dcount
        if item.count == 0:
          removed_s_i = item.sprite_i
          self.sprites_to_remove.append(removed_s_i)
          self.items.pop(i)

    if not found:
      return False

    if removed_s_i is not None:
      if self.selected_i and self.selected_i >= removed_s_i:
        self.selected_i -= 1

      if self.hovered_i and self.hovered_i >= removed_s_i:
        self.hovered_i -= 1


  def selected_item(self):
    if self.selected_i is None:
      return None

    return self.items[self.selected_i]

  def selected_spell(self):
    if self.selected_spell_i is None:
      return None

    return self.spells[self.selected_spell_i]

  def init_label(self, count):
    return pyglet.text.Label('x '+str(count), font_size=7, x=0, y=0, color=(255,255,255,255))

  def add_spell(self, spell):
    s_i = self.init_sprite(spell.sprite_name(), self.group)
    spell.sprite_i = s_i
    self.obtained_spells.append(spell.id)
    self.sprites[s_i].scale_x = 2
    self.sprites[s_i].scale_y = 2
    self.spells.append(spell)

  def add_item(self, item):
    for existing_item in self.items:
      if existing_item.name == item.name:
        existing_item.count += item.count
        existing_item.label = self.init_label(existing_item.count_anim)
        return

    s_i = self.init_sprite(item.sprite_name(), self.group)
    item.sprite_i = s_i
    item.count_anim = 0
    item.label = self.init_label(item.count_anim)
    self.items.append(item)

  def update(self, dt):
    while len(self.sprites_to_remove) > 0:
      r_i = self.sprites_to_remove.pop()
      for drawable in self.items + self.spells:
        if drawable.sprite_i >= r_i:
          drawable.sprite_i -= 1

      self.sprites[r_i].delete()
      self.sprites.pop(r_i)

    self.need_pos_update = True

    self.count_dt += dt

    if self.count_dt > 0.1:
      for item in self.items:
        if item.count > item.count_anim:
          item.count_anim += 1
        elif item.count < item.count_anim:
          item.count_anim -= 1
      self.count_dt = 0

    for i in range(len(self.items)):
      self.sprites_rel[self.items[i].sprite_i] = (10, i*20 + 10)
      if self.items[i].label:
        self.items[i].label.x = self.x + 20
        self.items[i].label.y = i*20 + 20
        self.items[i].label.text = 'x '+str(self.items[i].count_anim)

    for i in range(len(self.spells)):
      dx = self.sprites[self.spells[i].sprite_i].width // 2
      self.sprites_rel[self.spells[i].sprite_i] = (-260 + i*25 + 18 - dx, 206)

    self.sprites[self.spell_bg_i].color = (0,0,0)
    self.sprites[self.spell_bg_i].opacity = 200
    self.sprites[self.spell_bg_i].scale_x = len(self.spells) * 25 + 12
    self.sprites[self.spell_bg_i].scale_y = 30
    self.sprites[self.spell_bg_i].visible = len(self.spells) > 0

    self.sprites[self.bg_i].color = (0,0,0)
    self.sprites[self.bg_i].opacity = 200
    self.sprites[self.bg_i].scale_y = len(self.items) * 20 + 8
    self.sprites[self.bg_i].scale_x = 80

    if self.selected_spell_i is not None:
      self.sprites[self.sel_spell_bg_i].color = (255,255,255)
      self.sprites[self.sel_spell_bg_i].opacity = 200
      self.sprites[self.sel_spell_bg_i].scale_y = 6
      self.sprites[self.sel_spell_bg_i].scale_x = 25
      self.sprites_rel[self.sel_spell_bg_i] = (-260 + self.selected_spell_i*25 + 6, 225)
    else:
      self.sprites[self.sel_spell_bg_i].opacity = 0


    if self.selected_i is not None:
      self.sprites[self.sel_bg_i].color = (255,255,255)
      self.sprites[self.sel_bg_i].opacity = 200
      self.sprites[self.sel_bg_i].scale_y = 20
      self.sprites[self.sel_bg_i].scale_x = 6
      self.sprites_rel[self.sel_bg_i] = (self.WIDTH + 4, self.selected_i*20 + 4)
    else:
      self.sprites[self.sel_bg_i].opacity = 0

    self.sprites_rel[self.heart_i] = (0, 200)
    if self.heart_label:
      self.heart_label.x = self.x + 10
      self.heart_label.y = self.y + 200
      self.heart_label.text = 'x '+str(self.game.world.character.health)
    else:
      self.heart_label = self.init_label(self.game.world.character.health)

    if self.selected_item() is not None and self.selected_item().usable:
      self.sprites[self.use_btn_i].visible = True
      self.sprites_rel[self.use_btn_i] = (-24, self.selected_i*20 + 9)
    else:
      self.sprites[self.use_btn_i].visible = False

    if self.hovered_i is not None:
      self.sprites[self.hov_bg_i].color = (255,255,255)
      self.sprites[self.hov_bg_i].opacity = 50
      self.sprites[self.hov_bg_i].scale_y = 20
      self.sprites[self.hov_bg_i].scale_x = self.WIDTH + 20
      self.sprites_rel[self.hov_bg_i] = (0, self.hovered_i*20 + 4)
    else:
      self.sprites[self.hov_bg_i].opacity = 0

    super().update(dt)

  def on_right_click(self, x, y):
    self.selected_i = None
    self.selected_spell_i = None

  def on_click(self, x, y):
    if self.selected_item() is not None and self.selected_item().usable:
      selected_i = self.selected_i
      item = self.selected_item()
      if x > self.x - 24 and x < self.x - 3 and y > self.y + selected_i*20 + 9 and y < self.y + self.selected_i*20 + 18:
        item.use()
        self.remove_item(item.id)
        self.selected_i = None
        return True

    if x > self.x - 260 + 6 and y > self.y + 200:
      i = (x - self.x + 260 - 6) // 25
      if i < len(self.spells):
        self.selected_spell_i = int(i)
        return True

    if x > self.x and y - 4 > self.y and x < self.x + self.WIDTH:
      i = (y - self.y - 4) // 20
      if i < len(self.items):
        self.selected_i = int(i)
        return True

    return False

  def on_mouse_motion(self, x, y, dx, dy):
    if x > self.x and y - 4 > self.y and x < self.x + self.WIDTH:
      i = (y - self.y - 4) // 20
      if i < len(self.items):
        self.hovered_i = i
        return

    self.hovered_i = None

  def draw(self):
    for item in self.items:
      if item.label:
        item.label.draw()
    if self.heart_label:
      self.heart_label.draw()

    super().draw()