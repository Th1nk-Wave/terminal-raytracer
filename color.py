import vec3
import graphics
import math

def linear_to_gamma(linear_component):
  return math.sqrt(linear_component)

class color(vec3.vec3):
  pass

def write_color(window:graphics.window,pixel_color:color):
  pass