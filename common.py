import random

pi = 3.1415926535897932385
infinity = 999999999999999999999

def degrees_to_radians(degrees:float):
  return degrees * pi / 180.0

def random_double(min=None,max=None):
  if min and max:
    return min + (max-min)*(random.random()-0.0000000001)
  return (random.random()-0.0000000001)