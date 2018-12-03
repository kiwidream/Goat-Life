import pyglet
import sys
import random
from item import Item

class GrassSeeds(Item):

  def __init__(self, game, count):
    super().__init__(game, count, Item.GRASS_SEEDS)
    self.name = 'Grass Seeds'

  def sprite_name(self):
    return 'item_seeds.png'