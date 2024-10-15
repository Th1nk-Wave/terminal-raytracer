from ray import ray
from vec3 import vec3, point3, dot
from interval import interval

class hit_record:
  def __init__(self):
    from materials import material
    self.p = point3(0,0,0)
    self.normal = vec3(0,0,0)
    self.mat = material()
    self.t = float(0)
    self.front_face = bool(False)

  def set_face_normal(self,r:ray,outward_normal:vec3):
    self.front_face = dot(r.direction,outward_normal) < 0
    self.normal = outward_normal if self.front_face else -outward_normal

class hittable:
  def __init__(self):
    pass

  def hit(self, r:ray, ray_t:interval, rec:hit_record):
    pass