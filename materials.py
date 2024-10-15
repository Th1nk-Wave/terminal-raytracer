from common import random_double
from ray import ray
from color import color
from hittable import hit_record
from vec3 import random_unit_vector, reflect, unit_vector, dot, refract, vec3
import math


class material:
  def __init__(self,material=None):
    pass
  def scatter(self,r_in:ray,rec:hit_record,attenuation:color, scattered:ray):
    pass

class lambertian(material):
  def __init__(self,a:color):
    self.a = a

  def scatter(self,r_in:ray,rec:hit_record,attenuation:color, scattered:ray):
    scatter_direction = rec.normal + random_unit_vector()

    if scatter_direction.near_zero():
      scatter_direction = rec.normal
    
    scattered.origin = rec.p
    scattered.direction = scatter_direction
    attenuation.x = self.a.x
    attenuation.y = self.a.y
    attenuation.z = self.a.z
    return True

class metal(material):
  def __init__(self,a:color,fuzz:float):
    self.fuzz = min(fuzz,1)
    self.a = a

  def scatter(self,r_in:ray,rec:hit_record,attenuation:color, scattered:ray):
    reflected = reflect(unit_vector(r_in.direction),rec.normal)

    scattered.origin = rec.p
    scattered.direction = reflected + self.fuzz*random_unit_vector()
    attenuation.x = self.a.x
    attenuation.y = self.a.y
    attenuation.z = self.a.z
    return dot(scattered.direction,rec.normal) > 0

class dielectric(material):
  def __init__(self,index_of_refraction:float):
    self.index_of_refraction = index_of_refraction

  def scatter(self,r_in:ray,rec:hit_record,attenuation:color, scattered:ray):
    attenuation.x = 1
    attenuation.y = 1
    attenuation.z = 1

    refraction_ratio = 1.0/self.index_of_refraction if rec.front_face else self.index_of_refraction
    unit_direction = unit_vector(r_in.direction)
    cos_theta = min(dot(-unit_direction,rec.normal),1.0)
    sin_theta = math.sqrt(1.0 - cos_theta*cos_theta)

    cannot_refract = refraction_ratio * sin_theta > 1.0
    direction = vec3()

    if cannot_refract or self.reflectance(cos_theta,refraction_ratio) > random_double():
      direction = reflect(unit_direction,rec.normal)
    else:
      direction = refract(unit_direction,rec.normal,refraction_ratio)

    scattered.origin = rec.p
    scattered.direction = direction
    return True

  def reflectance(self,cosine:float,ref_idx:float):
    r0 = (1-ref_idx) / (1+ref_idx)
    r0 = r0*r0
    return r0 + (1-r0)*((1-cosine)**5)