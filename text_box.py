import pyglet
import sys
import random
from drawable import Drawable

class TextBox(Drawable):

  UPPER_LEFT = 0
  BOTTOM_LEFT = 1
  TOP = 2
  BOTTOM = 3
  LEFT = 4
  MIDDLE = 5
  UPPER_RIGHT = 6
  BOTTOM_RIGHT = 7
  RIGHT = 8

  ALL = range(9)


  def __init__(self, game, x, y, group, width, height):
    super().__init__(game, x, y, 0, True)
    self.batch = game.hud_batch
    self.width = width
    self.height = height
    self.bounce_dt = 0
    self.text = ['Hello sir. It is I, the person.', 'You should sacrifice a goat. No, really. RIGHT NOW.']
    self.text_progress = 0
    self.corner_size = 8
    self.label = None
    self.document = None
    self.text_progress_changed = True
    self.text_dt = 0

    # Upper left
    self.init_sprite('textbox_0.png', group, 0, height - self.corner_size)

    # Bottom left
    self.init_sprite('textbox_1.png', group, 0, 0)

    # Top
    self.init_sprite('textbox_2.png', group, self.corner_size, height - self.corner_size)
    self.sprites[self.TOP].scale_x = width - self.corner_size * 3

    # Bottom
    self.init_sprite('textbox_3.png', group, self.corner_size, 0)
    self.sprites[self.BOTTOM].scale_x = width - self.corner_size * 3

    # Left
    self.init_sprite('textbox_4.png', group, 0, self.corner_size)
    self.sprites[self.LEFT].scale_y = height - self.corner_size * 2

    # Middle
    self.init_sprite('textbox_5.png', group, self.corner_size, self.corner_size)
    self.sprites[self.MIDDLE].scale_x = width - self.corner_size * 2
    self.sprites[self.MIDDLE].scale_y = height - self.corner_size * 2

    # Upper right
    self.init_sprite('textbox_0.png', group, width - self.corner_size, height - self.corner_size)
    self.sprites[self.UPPER_RIGHT].scale_x = -1

    # Bottom right
    self.init_sprite('textbox_1.png', group, width - self.corner_size, 0)
    self.sprites[self.BOTTOM_RIGHT].scale_x = -1

    # Right
    self.init_sprite('textbox_4.png', group, width - self.corner_size, self.corner_size)
    self.sprites[self.RIGHT].scale_x = -1
    self.sprites[self.RIGHT].scale_y = height - self.corner_size * 2

  def update(self, dt):
    self.need_pos_update = True
    self.bounce_dt += dt


    if len(self.text) > 0:
      self.text_dt += dt
      if self.text_dt >= 0.07:

        if self.text_progress >= len(self.text[0]):
          if self.text_dt >= 1:
            self.text.pop(0)
            self.text_progress = 0
        else:
          self.text_progress += 1
          if self.text[0][self.text_progress:self.text_progress+1] == ' ':
            self.text_progress += 1

          self.text_dt = 0

        self.text_progress_changed = True

    if len(self.text) > 0 and self.text_progress_changed:
      self.document = pyglet.text.decode_text(self.text[0][:self.text_progress])

    if self.document and self.text_progress_changed:
      self.label = pyglet.text.DocumentLabel(self.document, self.x + self.corner_size, self.y + self.height - self.corner_size * 2 + self.all_sprites_rel[1], self.width - self.corner_size * 3, self.height, 'left', 'baseline', True)
      self.label.set_style('font_size', 7)
      self.label.set_style('color', (0, 0, 0, 180))
      self.label.set_style('kerning', 1)
      self.text_progress_changed = False


    if self.bounce_dt >= 0.5:
      self.all_sprites_rel = (0, 1 - self.all_sprites_rel[1])
      self.bounce_dt = 0
      self.text_progress_changed = True

    super().update(dt)

  def draw(self):
    if self.label:
      self.label.draw()

    super().draw()