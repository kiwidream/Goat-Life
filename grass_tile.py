import pyglet
import sys
import random
from drawable import Drawable
from tile import Tile
from grass_tuft import GrassTuft

class GrassTile(Tile):

  def __init__(self, game, tx, ty, group):
    super().__init__(game, tx, ty, group, 'grass')

    self.grass_tufts = []
    for i in range(random.randint(0, 6)):
      blades = (random.randint(0,1) == 0)
      tx_offset, ty_offset = tuple(self.random_offset(blades) for _ in range(2))
      group = self.game.world.group_for(ty+ty_offset)
      self.grass_tufts.append(GrassTuft(game, tx+tx_offset, ty+ty_offset, group, blades))

  def random_offset(self, blades=False):
    if blades:
      return random.random() * 0.6
    return random.random() * 0.85 + 0.05

  def update(self, dt):
    Drawable.handle_deletion(self.grass_tufts)

    for tuft in self.grass_tufts:
      tuft.update(dt)