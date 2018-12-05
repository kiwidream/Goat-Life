import pyglet
import sys
import random
from drawable import Drawable
from dungeon_template import DungeonTemplate
from chest import Chest
from enemy import Enemy
from mage import Mage
from pyglet.window import key

class DungeonTile(Drawable):

  TOP_LEFT = 0
  TOP_RIGHT = 1
  BOTTOM_RIGHT = 2
  BOTTOM_LEFT = 3
  FLOOR = 4
  OUTER_TOP_LEFT = 5
  OUTER_TOP_RIGHT = 6
  OUTER_BOTTOM_RIGHT = 7
  OUTER_BOTTOM_LEFT = 8
  TOP = 9
  BOTTOM = 10
  LEFT = 11
  RIGHT = 12
  EMPTY = 13
  CENTER_BOTTOM = 14
  CENTER = 15
  TOP_LEFT_FILL = 16
  TOP_RIGHT_FILL = 17
  BOTTOM_RIGHT_FILL = 18
  BOTTOM_LEFT_FILL = 19

  TYPE_EMPTY = 0
  TYPE_FLOOR = 1
  TYPE_WALL = 2
  TYPE_CHEST = 3
  TYPE_CHEST_STARTER = 4
  TYPE_EXIT = 5

  def __init__(self, game, tx, ty, group, type):
    super().__init__(game, tx, ty)

    self.hitboxes = set()
    self.type = type
    self.group = group
    self.target_state = self.game.world.DUNGEON
    self.group_floor = pyglet.graphics.OrderedGroup(group.order-1)
    self.width = self.game.TILE_WIDTH
    self.height = self.game.TILE_HEIGHT
    self.will_spawn_chest = False
    self.will_spawn_entity = False
    self.chest = None
    self.entities = []
    self.spawn_exit = False
    self.can_spawn_entity = True
    self.enemies = [Enemy, Mage]

    if type == self.TYPE_FLOOR:
      self.will_spawn_entity = random.random() < self.game.world.character.level * 0.1

    if type == self.TYPE_CHEST or type == self.TYPE_CHEST_STARTER:
      self.chest_type = 0 if type == self.TYPE_CHEST_STARTER else 1
      self.will_spawn_chest = random.random() < 0.8 or type == self.TYPE_CHEST_STARTER
      self.type = self.TYPE_FLOOR

    if type == self.TYPE_EXIT:
      self.spawn_exit = True
      self.type = self.TYPE_FLOOR

  def tile_at(self, dx, dy, type=2):
    tile = self.game.world.tile_at(self.tx+dx, self.ty+dy, self.game.world.DUNGEON)
    return (tile and tile.type == type) or (type == self.TYPE_EMPTY and not tile)

  def tile_sprite(self, type):
    return self.init_sprite('tile_stone_'+str(type)+'.png', self.group_floor if type == self.FLOOR else self.group)

  def draw(self):
    if self.chest:
      self.chest.draw()

    for entity in self.entities:
      entity.draw()

    super().draw()

  def update(self, dt):
    Drawable.handle_deletion(self.entities)

    if self.chest:
      self.chest.update(dt)

    offset = 0
    if self.spawn_exit:
      offset = self.game.dungeon_offset / self.game.TILE_WIDTH

    for entity in self.entities:
      entity.update(dt)

    super().update(dt)

    if self.spawn_exit and self.game.world.state_dt > 4 and self.game.world.progression == self.game.world.FREE_ROAM and abs(self.game.world.character.tx - offset - self.tx) < 0.6 and abs(self.game.world.character.ty - offset - self.ty - 0.5) < 0.6:

      if len(self.game.world.textbox.text) == 0 or self.game.keys[key.E]:
        self.game.world.textbox.text = ["Press E to exit the crevice."]
        self.game.world.textbox.faces = [None]

        if self.game.keys[key.E]:
          self.game.world.move_to = self.game.world.OVERWORLD

  def delete(self):
    if self.chest:
      self.chest.delete()

    for entity in self.entities:
      entity.delete()

    super().delete()

  def init_tile(self):
    dirs = {
      'N':  (0,1),
      'NW': (-1,1),
      'NE': (1,1),
      'W':  (-1,0),
      'E':  (1,0),
      'S':  (0,-1),
      'SE': (1,-1),
      'SW': (-1,-1)
    }

    floors = {key: self.tile_at(*dirs[key], self.TYPE_FLOOR) for key in dirs.keys()}
    walls = {key: self.tile_at(*dirs[key]) for key in dirs.keys()}
    surround_count = sum([int(walls[k]) for k in ['N','E','S','W']])
    offset = self.game.dungeon_offset / self.game.TILE_WIDTH

    if self.will_spawn_entity and self.can_spawn_entity:
      enemy_type = self.enemies[0] if random.random() >= self.game.world.character.level * 0.08 - 0.05 else self.enemies[1]
      self.entities.append(enemy_type(self.game, self.tx + offset, self.ty + offset, self.group))

    if self.will_spawn_chest:

      if (surround_count == 3 and not walls['E']) or (walls['N'] and walls['W'] and surround_count == 2 and walls['SW']):
        ori = Chest.LEFT
        cx, cy = Chest.OFFSET[ori]
        self.hitboxes.add((cx+2, cy, cx+8, cy+21))
      elif surround_count == 3 and not walls['W'] or (walls['N'] and walls['E'] and surround_count == 2 and walls['NE']):
        ori = Chest.RIGHT
        cx, cy = Chest.OFFSET[ori]
        self.hitboxes.add((cx, cy, cx+6, cy+21))
      elif surround_count == 3 and not walls['N']:
        ori = Chest.BOTTOM
        cx, cy = Chest.OFFSET[ori]
        self.hitboxes.add((cx, cy, cx+17, cy+7))
      elif walls['N'] or (floors['N'] and floors['S'] and floors['E'] and floors['W']):
        ori = Chest.TOP
        cx, cy = Chest.OFFSET[ori]
        self.hitboxes.add((cx, cy, cx+17, cy+10))
      elif walls['W']:
        ori = Chest.LEFT
        cx, cy = Chest.OFFSET[ori]
        self.hitboxes.add((cx+2, cy, cx+8, cy+21))
      elif walls['E']:
        ori = Chest.RIGHT
        cx, cy = Chest.OFFSET[ori]
        self.hitboxes.add((cx, cy, cx+6, cy+21))
      else:
        ori = Chest.BOTTOM
        cx, cy = Chest.OFFSET[ori]
        self.hitboxes.add((cx, cy, cx+17, cy+7))

      self.chest = Chest(self.game, self.tx + offset, self.ty + offset, self.group, ori, self.chest_type)

    if self.type == self.TYPE_WALL:
      empty = {key: self.tile_at(*dirs[key], self.TYPE_EMPTY) for key in dirs.keys()}

      corners = []

      if walls['E'] and walls['S']:
        if empty['SE']:
          self.hitboxes.add((self.width-12, 0, self.width, 17))
          corners.append(self.OUTER_TOP_LEFT)
        elif walls['SE']:
          self.hitboxes.add((0,0,self.width,self.height))
          corners.append(self.TOP_LEFT_FILL)
        else:
          self.hitboxes.add((0,0,12,self.height))
          self.hitboxes.add((0,self.height-17,self.width,self.height))
          corners.append(self.TOP_LEFT)
      elif walls['W'] and walls['S']:
        if empty['SW']:
          self.hitboxes.add((0, 0, 12, 17))
          corners.append(self.OUTER_TOP_RIGHT)
        elif walls['SW']:
          self.hitboxes.add((0,0,self.width,self.height))
          corners.append(self.TOP_RIGHT_FILL)
        else:
          self.hitboxes.add((self.width-12,0,self.width,self.height))
          self.hitboxes.add((0,self.height-17,self.width,self.height))
          corners.append(self.TOP_RIGHT)
      elif walls['W'] and walls['N']:
        if empty['NW']:
          self.hitboxes.add((0, self.height-16, 12, self.height))
          corners.append(self.OUTER_BOTTOM_RIGHT)
        elif walls['NW']:
          self.hitboxes.add((0,0,self.width,self.height))
          corners.append(self.BOTTOM_RIGHT_FILL)
        else:
          self.hitboxes.add((self.width-12,0,self.width,self.height))
          self.hitboxes.add((0,0,self.width,17))
          corners.append(self.BOTTOM_RIGHT)
      elif walls['E'] and walls['N']:
        if empty['NE']:
          self.hitboxes.add((self.width-12, self.height-16, self.width, self.height))
          corners.append(self.OUTER_BOTTOM_LEFT)
        elif walls['NE']:
          self.hitboxes.add((0,0,self.width,self.height))
          corners.append(self.BOTTOM_LEFT_FILL)
        else:
          self.hitboxes.add((0,0,12,self.height))
          self.hitboxes.add((0,0,self.width,17))
          corners.append(self.BOTTOM_LEFT)

      if surround_count == 1 and floors['S']:
        self.hitboxes.add((0,0,self.width,self.height))
        return self.tile_sprite(self.CENTER_BOTTOM)
      if surround_count <= 2 and floors['S'] and floors['N']:
        self.hitboxes.add((0,0,self.width,self.height))
        return self.tile_sprite(self.CENTER_BOTTOM)

      if len(corners) > 0:
        if surround_count >= 3:
          if not walls['S'] or (not walls['SE'] and not walls['SW']):
            self.hitboxes.add((0,0,self.width,self.height))
            return self.tile_sprite(self.CENTER_BOTTOM)
          else:
            self.hitboxes.add((0,0,self.width,self.height))
            return self.tile_sprite(self.CENTER)

        [self.tile_sprite(corner) for corner in corners]

      elif walls['N'] and walls['S']:
        if not floors['E']:
          self.hitboxes.add((self.width-12,0,self.width,self.height))
          self.tile_sprite(self.RIGHT)
        elif not floors['W']:
          self.hitboxes.add((0,0,12,self.height))
          self.tile_sprite(self.LEFT)
      elif walls['E'] and walls['W']:
        if not floors['N']:
          self.hitboxes.add((0, self.height-17, self.width, self.height))
          self.tile_sprite(self.TOP)
        elif not floors['S']:
          self.hitboxes.add((0, 0, self.width, 17))
          self.tile_sprite(self.BOTTOM)

    if self.type != self.TYPE_EMPTY:
      self.tile_sprite(self.FLOOR)

      if self.spawn_exit:
        self.tile_sprite("exit")