import pyglet
import sys
import random
from spell import Spell
from item import Item

class SpellScroll(Item):

  def __init__(self, game, spell_id):
    super().__init__(game, 1, Item.SPELL_SCROLL + spell_id)
    self.game = game
    self.scroll_type = Spell.TYPE[spell_id]
    self.spell_id = spell_id
    self.name = 'Spell Scroll'
    self.usable = True

  def sprite_name(self):
    return 'item_scroll_'+str(self.scroll_type)+'.png'

  def use(self):
    if len(self.game.world.inventory.spells) == 0:
      self.game.world.textbox.text = ["You now have a spell. Select the spell, and use LEFT CLICK to fire. RIGHT CLICK to deselect."]

    self.game.world.inventory.add_spell(Spell(self.game, self.spell_id))
