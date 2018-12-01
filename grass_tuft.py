import pyglet
import sys
import random
from drawable import Drawable

class GrassTuft(Drawable):

  def __init__(self, game, tx, ty, group, blades=False):
    super().__init__(game, tx, ty)
    self.remaining_grass = 3
    grass_type = 'blades' if blades else 'tuft'

    for i in range(1, 4):
      self.init_sprite('grass_'+grass_type+'_'+str(i)+'.png', group)

  def update(self, dt):
    self.set_visible_sprite(self.remaining_grass - 1)