import pyglet
import sys
import random
from item import Item

class WaterGem(Item):

  def __init__(self, game, count):
    super().__init__(game, count, Item.WATER_GEM)
    self.name = 'Water Element'

  def sprite_name(self):
    return 'item_gem_0.png'