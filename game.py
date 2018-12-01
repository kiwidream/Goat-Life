import pyglet
pyglet.options['debug_gl'] = False
from pyglet.gl import *
from pyglet.graphics import Batch
from pyglet.image.atlas import TextureBin
from pyglet.window import mouse
from camera import Camera
from world import World
import sys
import cProfile
import math
from pyglet.window import key

#glEnable(GL_DEPTH_TEST)
#glEnable(GL_BLEND)
#glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
#glEnable(GL_ALPHA_TEST)
#glAlphaFunc(GL_GREATER, .1)
glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

class Game:
  bin = TextureBin()
  bin_loaded = {}

  batch = Batch()
  hud_batch = Batch()

  TILE_HEIGHT = 32
  TILE_WIDTH = 32

  def __init__(self):
    self.window = pyglet.window.Window()
    self.camera = Camera(self)
    self.keys = key.KeyStateHandler()
    self.window.push_handlers(self.keys)
    self.world = World(self)
    self.cursor = self.window.CURSOR_DEFAULT
    self.set_cursor = None



game = Game()
fps_display = pyglet.clock.ClockDisplay()

def main():
  pyglet.app.run()

def update(dt):
  game.camera.update(dt)
  game.world.update(dt)
  if game.set_cursor != game.cursor:
    game.window.set_mouse_cursor(game.window.get_system_mouse_cursor(game.cursor))
    game.set_cursor = game.cursor

pyglet.clock.schedule_interval(update, 1.0/60.0)
pyglet.clock.set_fps_limit(60)

def transform_mouse_coords(x, y):
  x -= game.camera.width // 2
  y -= game.camera.height // 2
  x /= game.camera.zoom
  y /= game.camera.zoom
  x += game.camera.x
  y += game.camera.y
  return x, y

@game.window.event
def on_mouse_motion(x, y, dx, dy):
  x, y = transform_mouse_coords(x, y)
  game.world.on_mouse_motion(x, y, dx, dy)

@game.window.event
def on_mouse_press(x, y, button, modifiers):
  x, y = transform_mouse_coords(x, y)
  if button == mouse.LEFT:
    game.world.on_click(x, y)


@game.window.event
def on_draw():
  game.window.clear()
  game.camera.apply()
  game.world.draw()
  game.batch.draw()
  game.camera.apply_hud()
  game.hud_batch.draw()
  game.world.draw(True)
  fps_display.draw()

if __name__ == '__main__':
  cProfile.run('main()')