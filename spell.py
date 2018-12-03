import pyglet
import sys
import random
from character import Character
from item import Item

class Spell:

  BASIC_WATER = 2

  TYPE_WATER = 0
  TYPE_FIRE = 1
  TYPE_EARTH = 2

  TYPE = {
    0: 1,
    1: 0,
    2: 0,
    3: 1,
    4: 1,
    5: 2,
    6: 2,
    7: 2
  }
  DAMAGE = {
    0: 1,
    1: 2,
    2: 1,
    3: 2,
    4: 3,
    5: 2,
    6: 1,
    7: 1
  }
  COST = {
    0: (0, 1, 0),
    1: (2, 0, 0),
    2: (1, 0, 0),
    3: (0, 2, 0),
    4: (5, 2, 0),
    5: (0, 2, 3),
    6: (0, 0, 2),
    7: (0, 0, 1)
  }

  def __init__(self, game, id=0, count=1):
    self.id = id
    self.count = count
    self.game = game
    self.speed = 1.25
    self.name = 'Default Item'

  def fire(self, tx, ty, entity):
    if self.game.world.state == self.game.world.OVERWORLD:
      return

    if isinstance(entity, Character):
      wg, fg, eg = self.COST[self.id]
      inventory = self.game.world.inventory
      if inventory.has_item(Item.WATER_GEM, wg) and inventory.has_item(Item.FIRE_GEM, fg) and inventory.has_item(Item.EARTH_GEM, eg):
        inventory.remove_item(Item.WATER_GEM, wg)
        inventory.remove_item(Item.FIRE_GEM, fg)
        inventory.remove_item(Item.EARTH_GEM, eg)
      else:
        return False

    entity.spawn_spell(tx, ty, self)

  def sprite_name(self):
    return 'particle_spell_'+str(self.id)+'.png'