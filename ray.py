import vec3

class ray:
  def __init__(self,origin:vec3.point3,direction:vec3.vec3):
    self.origin = origin
    self.direction = direction

  def at(self,t):
    return self.origin + t*self.direction