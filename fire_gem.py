import pyglet
import sys
import random
from item import Item

class FireGem(Item):

  def __init__(self, count):
    super().__init__(count, Item.FIRE_GEM)
    self.name = 'Fire Element'

  def sprite_name(self):
    return 'item_gem_1.png'