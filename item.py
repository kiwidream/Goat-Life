import pyglet
import sys
import random

class Item:

  DEFAULT = 0
  GRASS_SEEDS = 1
  FIRE_GEM = 2
  WATER_GEM = 3
  EARTH_GEM = 4
  GOAT_SKULL = 5
  SPELL_SCROLL = 6
  # Reserved ID space spells

  def __init__(self, game, count=1, id=0):
    self.game = game
    self.id = id
    self.count = count
    self.name = 'Default Item'
    self.usable = False

  def sprite_name(self):
    return 'face_1.png'