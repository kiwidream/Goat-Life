import pyglet
import sys
import random
from item import Item

class GrassSeeds(Item):

  def __init__(self, count):
    super().__init__(count, Item.GRASS_SEEDS)
    self.name = 'Grass Seeds'

  def sprite_name(self):
    return 'item_seeds.png'