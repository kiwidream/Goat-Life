import pyglet
import sys
import random
from spell import Spell
from item import Item

class GoatSkull(Item):

  def __init__(self, game, right_half=False):
    super().__init__(game, 1, Item.GOAT_SKULL)
    self.right_half = right_half
    if right_half:
      game.world.skulls_collected = True
    self.name = 'Goat Skull ('+('Right' if right_half else 'Left')+' Half)'

  def sprite_name(self):
    return 'goat_skull.png'