import pyglet
import sys
import random

class Drawable:

  def __init__(self, game, tx=0, ty=0, z=0, hud_element=False):
    self.game = game
    self.tx, self.ty = tx, ty
    self.z = 0
    self.hud_element = hud_element

    if not self.hud_element:
      self.x, self.y = self.screen_coords()
    else:
      self.x, self.y = tx, ty

    self.origX, self.origY = 0, 0
    self.group = None
    self.sprites = []
    self.sprites_rel = []
    self.all_sprites_rel = (0,0)
    self.visible_sprite = None
    self.need_pos_update = True
    self.needs_deletion = False
    self.hovered = False
    self.hud_element = hud_element
    self.batch = self.game.batch

  def mouse_in_bounds(self, x, y):
    sprite = self.get_visible_sprite()
    sx,sy = self.x - self.sprites_rel[self.visible_sprite][0] if self.visible_sprite else 0, self.y
    in_bounds = x >= sx and x <= sx + sprite.width and y >= sy and y <= sy + sprite.height
    return in_bounds

  def screen_coords(self):
    return self.tx * self.game.TILE_WIDTH, self.ty * self.game.TILE_HEIGHT

  def set_visible_sprite(self, i):
    if self.visible_sprite == i:
      return

    for j in range(len(self.sprites)):
      self.sprites[j].visible = (j == i)

    self.visible_sprite = i

  def get_visible_sprite(self):
    if self.visible_sprite is None and len(self.sprites) > 0:
      return self.sprites[0]

    return self.sprites[self.visible_sprite]

  @staticmethod
  def handle_deletion(drawables):
    to_delete = []
    for i in range(len(drawables)):
      if drawables[i].needs_deletion:
        to_delete.append(i)

    offset = 0
    for i in to_delete:
      drawables[i + offset].delete()
      drawables.pop(i + offset)
      offset -= 1

  def init_sprite(self, filename, group, rel_x=0, rel_y=0):
    if filename not in self.game.bin_loaded.keys():
      image = pyglet.image.load('sprites/'+filename)
      texture = self.game.bin.add(image)
      self.game.bin_loaded[filename] = texture
    else:
      texture = self.game.bin_loaded[filename]

    i = len(self.sprites)

    self.sprites_rel.append((rel_x, rel_y))

    s_x, s_y = self.sprite_coords(i)
    self.sprites.append(pyglet.sprite.Sprite(texture, s_x, s_y, batch=self.batch, group=group))

    return i

  def update_position(self):
    self.need_pos_update = True

  def sprite_coords(self, i=None):
    if i is None or i >= len(self.sprites_rel):
      return (0, 0)
    sx = self.x + self.sprites_rel[i][0] + self.all_sprites_rel[0]
    sy = self.y + self.sprites_rel[i][1] + self.all_sprites_rel[1] + self.z
    return sx, sy


  def delete(self):
    for sprite in self.sprites:
      sprite.delete()

  def update(self, dt):
    pass

  def draw(self):

    if self.need_pos_update:

      if not self.hud_element:
        self.x, self.y = self.screen_coords()

      for i in range(len(self.sprites)):
        self.sprites[i].position = self.sprite_coords(i)

      self.need_pos_update = False