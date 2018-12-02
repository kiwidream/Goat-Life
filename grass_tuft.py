import pyglet
import sys
import random
from drawable import Drawable

class GrassTuft(Drawable):

  def __init__(self, game, tx, ty, group, blades=False, anim=False):
    super().__init__(game, tx, ty)
    self.remaining_grass = 3
    self.grass_anim = 0 if anim else self.remaining_grass
    self.grass_anim_dt = random.random() * 5 + 5
    grass_type = 'blades' if blades else 'tuft'

    for i in range(1, 4):
      s_i = self.init_sprite('grass_'+grass_type+'_'+str(i)+'.png', group)
      self.sprites[s_i].visible = False

  def update(self, dt):

    if self.grass_anim < self.remaining_grass:
      self.grass_anim_dt += dt
      if self.grass_anim_dt >= 10:
        self.grass_anim += 1
        self.grass_anim_dt = 0
    else:
      self.grass_anim = self.remaining_grass

    self.set_visible_sprite(self.grass_anim - 1)