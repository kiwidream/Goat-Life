import pyglet
from drawable import Drawable
from pyglet.window import key
from pyglet.gl import *
import sys

class Camera(Drawable):

  zoom = 2
  hud_zoom = 2
  speed = 6

  def __init__(self, game):
    self.game = game
    self.speed = 125
    self.width = self.game.window.width
    self.height = self.game.window.height
    self.x = self.width // 4
    self.y = self.height // 4
    self.vx = 0
    self.vy = 0
    self.last_cull = None
    self.target = None

  def reset(self):
    self.zoom = 2 if self.game.world.state == self.game.world.OVERWORLD else 3
    glLoadIdentity()
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

  def apply(self):
    self.reset()
    cx, cy = self.x, self.y
    if self.game.world.state == self.game.world.DUNGEON:
      cx += self.game.dungeon_offset
      cy += self.game.dungeon_offset
    glTranslatef(-int(cx*self.zoom)+self.width//2, -int(cy*self.zoom)+self.height//2, 0)
    glScaled(self.zoom, self.zoom, 1)

  def apply_hud(self):
    self.reset()
    glScaled(self.hud_zoom, self.hud_zoom, 1)

  def move_to_target(self):
    self.x = self.target.x
    self.y = self.target.y

  def update(self, dt):
    dx = 0
    dy = 0

    cx, cy = self.x, self.y

    if self.game.world.state == self.game.world.DUNGEON:
      cx += self.game.dungeon_offset
      cy += self.game.dungeon_offset

    if self.target:
      dx = (self.target.x - cx) * dt
      dy = (self.target.y - cy) * dt

    cx, cy = self.x, self.y

    if cx + dx >= self.width // 2 / self.zoom and cx + dx < self.game.world.WIDTH[self.game.world.state] * self.game.TILE_WIDTH - self.width // 2 / self.zoom:
      self.x += dx

    if cy + dy >= self.height // 2 / self.zoom and cy + dy < self.game.world.HEIGHT[self.game.world.state] * self.game.TILE_HEIGHT - self.height // 2 / self.zoom:
      self.y += dy



    self.vx *= 0.92
    self.vy *= 0.92



    #if self.game.keys[key.W]:
    #  self.vy = self.vy + (self.speed / self.zoom - self.vy) * 0.6
    #elif self.game.keys[key.S]:
    #  self.vy = self.vy + (-self.speed / self.zoom - self.vy) * 0.6

    #if self.game.keys[key.D]:
    #  self.vx = self.vx + (self.speed / self.zoom - self.vx) * 0.6
    #elif self.game.keys[key.A]:
    #  self.vx = self.vx + (-self.speed / self.zoom - self.vx) * 0.6


    if self.game.keys[key.UP]:
      self.zoom *= 1.1
    elif self.game.keys[key.DOWN]:
      self.zoom *= 0.9

    if self.game.world.state == self.game.world.DUNGEON:
      cx += self.game.dungeon_offset
      cy += self.game.dungeon_offset

