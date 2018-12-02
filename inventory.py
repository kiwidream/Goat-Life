import pyglet
import sys
import random
from drawable import Drawable
from item import Item
from grass_seeds import GrassSeeds
from water_gem import WaterGem
from fire_gem import FireGem
from earth_gem import EarthGem

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
    self.sprites_rel[self.sel_bg_i] = (200, 0)
    self.sprites_rel[self.hov_bg_i] = (200, 0)
    self.selected_i = None
    self.hovered_i = None
    self.count_dt = 0

    self.add_item(GrassSeeds(25))
    #self.add_item(WaterGem(50))
    #self.add_item(FireGem(50))
    #self.add_item(EarthGem(50))

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
          self.items.pop(i)

    if not found:
      return False

    if removed_s_i is not None:
      if self.selected_i > removed_s_i:
        self.selected_i -= 1

      if self.hovered_i > removed_s_i:
        self.hovered_i -= 1


  def selected_item(self):
    if self.selected_i is None:
      return None

    return self.items[self.selected_i]

  def init_label(self, item):
    return pyglet.text.Label('x '+str(item.count_anim), font_size=7, x=0, y=0, color=(255,255,255,255))

  def add_item(self, item):
    for existing_item in self.items:
      if existing_item.name == item.name:
        existing_item.count += item.count
        existing_item.label = self.init_label(existing_item)
        return

    s_i = self.init_sprite(item.sprite_name(), self.group)
    item.sprite_i = s_i
    item.count_anim = 0
    item.label = self.init_label(item)
    self.items.append(item)

  def update(self, dt):
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

    self.sprites[self.bg_i].color = (0,0,0)
    self.sprites[self.bg_i].opacity = 200
    self.sprites[self.bg_i].scale_y = len(self.items) * 20 + 8
    self.sprites[self.bg_i].scale_x = 80

    if self.selected_i is not None:
      self.sprites[self.sel_bg_i].color = (255,255,255)
      self.sprites[self.sel_bg_i].opacity = 200
      self.sprites[self.sel_bg_i].scale_y = 20
      self.sprites[self.sel_bg_i].scale_x = 6
      self.sprites_rel[self.sel_bg_i] = (self.WIDTH + 4, self.selected_i*20 + 4)
    else:
      self.sprites[self.sel_bg_i].opacity = 0

    if self.hovered_i is not None:
      self.sprites[self.hov_bg_i].color = (255,255,255)
      self.sprites[self.hov_bg_i].opacity = 50
      self.sprites[self.hov_bg_i].scale_y = 20
      self.sprites[self.hov_bg_i].scale_x = self.WIDTH + 20
      self.sprites_rel[self.hov_bg_i] = (0, self.hovered_i*20 + 4)
    else:
      self.sprites[self.hov_bg_i].opacity = 0

    super().update(dt)

  def on_click(self, x, y):
    if x > self.x and y - 4 > self.y and x < self.x + self.WIDTH:
      i = (y - self.y - 4) // 20
      if i < len(self.items):
        self.selected_i = int(i)
        return

    self.selected_i = None

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

    super().draw()