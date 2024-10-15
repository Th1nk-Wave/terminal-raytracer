from hittable import hittable, hit_record
from vec3 import point3, vec3, dot
from ray import ray
import math
from interval import interval
from materials import material


class sphere(hittable):
  def __init__(self,center:point3,radius:float,mat:material):
    self.mat = mat
    self.center = center
    self.radius = radius
  def hit(self,r:ray,ray_t:interval,rec:hit_record):
    oc = r.origin - self.center
    a = r.direction.length_squared
    half_b = dot(oc, r.direction)
    c = oc.length_squared - self.radius*self.radius

    discriminant = half_b*half_b - a*c
    if discriminant < 0:
      return False
    sqrtd = math.sqrt(discriminant)

    root = (-half_b - sqrtd) / a
    if root <= ray_t.min or ray_t.max <= root:
      root = (-half_b + sqrtd) / a
      if root <= ray_t.min or ray_t.max <= root:
        return False

    rec.t = root
    rec.p = r.at(rec.t)
    outward_normal = (rec.p - self.center) / self.radius
    rec.set_face_normal(r,outward_normal)
    rec.mat = self.mat

    return True
    
    