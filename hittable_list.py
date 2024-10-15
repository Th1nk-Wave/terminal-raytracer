from hittable import hittable, hit_record
from ray import ray
from interval import interval

class hittable_list(hittable):
  def __init__(self):
    self.objects = []

  def clear(self):
    self.objects.clear()

  def add(self,object:hittable):
    self.objects.append(object)

  def hit(self, r:ray, ray_t:interval, rec:hit_record):
    temp_rec = hit_record()
    hit_anything = False
    closest_so_far = ray_t.max

    for object in self.objects:
      if object.hit(r,interval(ray_t.min,closest_so_far),temp_rec):
        hit_anything = True
        closest_so_far = temp_rec.t
        rec.front_face = temp_rec.front_face
        rec.normal = temp_rec.normal
        rec.p = temp_rec.p
        rec.t = temp_rec.t
        rec.mat = temp_rec.mat

    return hit_anything