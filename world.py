import pyglet
import sys
import random
from drawable import Drawable
from grass_tile import GrassTile
from goat import Goat
from text_box import TextBox

class World(Drawable):

  HEIGHT = 12
  WIDTH = 12

  def __init__(self, game):
    self.game = game
    self.tiles = []
    self.entities = []
    self.has_init = False
    self.groups = [pyglet.graphics.OrderedGroup(self.HEIGHT * 32 - i) for i in range(self.HEIGHT*32)]
    self.sacrifice_mode = True
    self.hud_group = pyglet.graphics.OrderedGroup(self.HEIGHT * 32 + 1)
    self.textbox = TextBox(game, 10, 10, self.hud_group, 200, 60)
    self.last_hover = None
    self.hover_dt = 0

  def group_for(self, ty):
    return self.groups[int(ty // 0.03215)]

  def tile_at(self, tx, ty):
    if tx < 0 or tx >= self.WIDTH or ty < 0 or ty >= self.HEIGHT:
      return False

    return self.tiles[ty*self.WIDTH + tx]

  def update(self, dt):
    if not self.has_init:
      for i in range(random.randint(10, 30)):
        tx = (random.random() * self.WIDTH - 1) + 1
        ty = (random.random() * self.HEIGHT - 1) + 1
        self.entities.append(Goat(self.game, tx, ty, self.group_for(ty)))

      for ty in range(self.HEIGHT):
        for tx in range(self.WIDTH):
          self.tiles.append(GrassTile(self.game, tx, ty, self.group_for(ty+1)))
      self.has_init = True

    if self.last_hover:
      self.hover_dt += dt

    if self.last_hover and self.hover_dt >= 0.05 and self.sacrifice_mode:
      mouse_hover = False

      for entity in self.entities:
        entity.hovered = entity.mouse_in_bounds(*self.last_hover)
        mouse_hover = entity.hovered
        if mouse_hover:
          break

      self.hover_dt = 0
      self.last_hover = None
      self.game.cursor = self.game.window.CURSOR_HAND if mouse_hover else self.game.window.CURSOR_DEFAULT

    for drawable in self.tiles + self.entities + [self.textbox]:
      drawable.update(dt)

  def on_click(self, x, y):
    if not self.sacrifice_mode:
      return

    for entity in self.entities:
      if entity.hovered and isinstance(entity, Goat):
        entity.spawn_flames()
        #self.sacrifice_mode = False

  def on_mouse_motion(self, x, y, dx, dy):
    self.last_hover = (x, y)

  def draw(self, hud=False):
    for drawable in self.tiles + self.entities + [self.textbox]:
      if drawable.hud_element == hud:
        drawable.draw()