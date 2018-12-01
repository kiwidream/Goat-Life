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

  def reset(self):
    glLoadIdentity()
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

  def apply(self):
    self.reset()
    glTranslatef(-int(self.x*self.zoom)+self.width//2, -int(self.y*self.zoom)+self.height//2, 0)
    glScaled(self.zoom, self.zoom, 1)

  def apply_hud(self):
    self.reset()
    glScaled(self.hud_zoom, self.hud_zoom, 1)

  def update(self, dt):
    #print(self.width, self.height, self.x, self.y)
    #sys.stdout.flush()
    dx = self.vx * dt
    dy = self.vy * dt
    if self.x + dx >= self.width // 2 / self.zoom and self.x + dx < self.game.world.WIDTH * self.game.TILE_WIDTH - self.width // 2 / self.zoom:
      self.x += dx

    if self.y + dy >= self.height // 2 / self.zoom and self.y + dy < self.game.world.HEIGHT * self.game.TILE_HEIGHT - self.height // 2 / self.zoom:
      self.y += dy
    self.vx *= 0.92
    self.vy *= 0.92

    if self.game.keys[key.W]:
      self.vy = self.vy + (self.speed / self.zoom - self.vy) * 0.6
    elif self.game.keys[key.S]:
      self.vy = self.vy + (-self.speed / self.zoom - self.vy) * 0.6

    if self.game.keys[key.D]:
      self.vx = self.vx + (self.speed / self.zoom - self.vx) * 0.6
    elif self.game.keys[key.A]:
      self.vx = self.vx + (-self.speed / self.zoom - self.vx) * 0.6


    if self.game.keys[key.UP]:
      self.zoom *= 1.1
    elif self.game.keys[key.DOWN]:
      self.zoom *= 0.9