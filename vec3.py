import math
from common import random_double


class vec3:
  def __init__(self,x=0.0,y=0.0,z=0.0):
    self.x = x
    self.y = y
    self.z = z

  def __neg__(self):
    return vec3(-self.x,-self.y,-self.z)
  
  def __add__(self,val2):
    if type(val2) == int or type(val2) == float:
      return vec3(self.x + val2,self.y + val2, self.z + val2)
    else:
      return vec3(self.x + val2.x,self.y + val2.y, self.z + val2.z)

  def __iadd__(self,val2):
    if type(val2) == int or type(val2) == float:
      self.x += val2
      self.y += val2
      self.z += val2
    else:
      self.x += val2.x
      self.y += val2.y
      self.z += val2.z
    return self

  def __sub__(self,val2):
    if type(val2) == int or type(val2) == float:
      return vec3(self.x - val2,self.y - val2, self.z - val2)
    else:
      return vec3(self.x - val2.x,self.y - val2.y, self.z - val2.z)

  def __isub__(self,val2):
    if type(val2) == int or type(val2) == float:
      self.x -= val2
      self.y -= val2
      self.z -= val2
    else:
      self.x -= val2.x
      self.y -= val2.y
      self.z -= val2.z
    return self

  def __mul__(self,val2):
    if type(val2) == int or type(val2) == float:
      return vec3(self.x * val2,self.y * val2, self.z * val2)
    else:
      return vec3(self.x * val2.x,self.y * val2.y, self.z * val2.z)

  def __rmul__(self,val2):
    return vec3(self.x * val2,self.y * val2, self.z * val2)

  def __imul__(self,val2):
    if type(val2) == int or type(val2) == float:
      self.x *= val2
      self.y *= val2
      self.z *= val2
    else:
      self.x *= val2.x
      self.y *= val2.y
      self.z *= val2.z
    return self

  def __truediv__(self,val2):
    if type(val2) == int or type(val2) == float:
      return vec3(self.x / val2,self.y / val2, self.z / val2)
    else:
      return vec3(self.x / val2.x,self.y / val2.y, self.z / val2.z)

  def __idiv__(self,val2):
    if type(val2) == int or type(val2) == float:
      self.x /= val2
      self.y /= val2
      self.z /= val2
    else:
      self.x /= val2.x
      self.y /= val2.y
      self.z /= val2.z
    return self

  def __floordiv__(self,val2):
    if type(val2) == int or type(val2) == float:
      return vec3(self.x // val2,self.y // val2, self.z // val2)
    else:
      return vec3(self.x // val2.x,self.y // val2.y, self.z // val2.z)

  def __ifloordiv__(self,val2):
    if type(val2) == int or type(val2) == float:
      self.x //= val2
      self.y //= val2
      self.z //= val2
    else:
      self.x //= val2.x
      self.y //= val2.y
      self.z //= val2.z
    return self

  @property
  def length_squared(self):
    return self.x*self.x + self.y*self.y + self.z*self.z

  def near_zero(self):
    s = 1e-8
    return (math.fabs(self.x) < s) and (math.fabs(self.y) < s) and (math.fabs(self.z) < s)

  @property
  def length(self):
    return math.sqrt(self.length_squared)

class point3(vec3):
  pass

def random(min=None,max=None):
    if min and max:
      return vec3(random_double(min,max),random_double(min,max),random_double(min,max))
    return vec3(random_double(),random_double(),random_double())

def dot(vec3_a:vec3,vec3_b:vec3):
  return vec3_a.x * vec3_b.x + vec3_a.y * vec3_b.y + vec3_a.z * vec3_b.z

def cross(vec3_a:vec3,vec3_b:vec3):
  return vec3(vec3_a.y * vec3_b.z - vec3_a.z * vec3_b.y,
             vec3_a.z * vec3_b.x - vec3_a.x * vec3_b.z,
             vec3_a.x * vec3_b.y - vec3_a.y * vec3_b.x)

def unit_vector(vec3_a:vec3):
  return vec3_a / vec3_a.length

def random_in_unit_disk():
  while True:
    p = vec3(random_double(-1,1),random_double(-1,1),0)
    if p.length_squared < 1:
      return p

def random_in_unit_sphere():
  while True:
    p = random(-1,1)
    if p.length_squared < 1:
      return p

def random_unit_vector():
  return unit_vector(random_in_unit_sphere())

def random_on_hemisphere(normal:vec3):
  on_unit_sphere = random_unit_vector()
  if dot(on_unit_sphere,normal) > 0.0:
    return on_unit_sphere
  else:
    return -on_unit_sphere

def reflect(v:vec3,n:vec3):
  return v - 2*dot(v,n)*n

def refract(uv:vec3,n:vec3,etai_over_etat:float):
  cos_theta = min(dot(-uv,n),1.0)
  r_out_perp = etai_over_etat * (uv + cos_theta*n)
  r_out_parallel = -math.sqrt(math.fabs(1.0 - r_out_perp.length_squared)) * n
  return r_out_perp + r_out_parallel