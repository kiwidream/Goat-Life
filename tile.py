import pyglet
import sys
import random
from drawable import Drawable

class Tile(Drawable):

  def __init__(self, game, tx, ty, group, type):
    super().__init__(game, tx, ty)
    self.init_sprite('tile_'+type+'.png', group)