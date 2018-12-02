import pyglet
import sys
import random

class Item:

  DEFAULT = 0
  GRASS_SEEDS = 1
  FIRE_GEM = 2
  WATER_GEM = 3
  EARTH_GEM = 4

  def __init__(self, count=1, id=0):
    self.id = id
    self.count = count
    self.name = 'Default Item'

  def sprite_name(self):
    return 'face_1.png'