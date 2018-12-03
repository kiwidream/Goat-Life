import pyglet
import sys
import random
from item import Item

class EarthGem(Item):

  def __init__(self, game, count):
    super().__init__(game, count, Item.EARTH_GEM)
    self.name = 'Earth Element'

  def sprite_name(self):
    return 'item_gem_2.png'