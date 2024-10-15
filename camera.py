import math
import graphics
from color import color, linear_to_gamma
from ray import ray
from vec3 import point3, random_in_unit_disk, vec3, unit_vector, dot, random_on_hemisphere, cross
from hittable import hittable, hit_record
from hittable_list import hittable_list
from sphere import sphere
from interval import interval
from common import random_double, degrees_to_radians


class camera:
  def __init__(self,output:graphics.window,aspect_ratio,image_width,samples_per_pixel,max_depth,lookfrom:point3,lookat:point3,vup:vec3,vfov,defocus_angle:float,focus_dist:float):
    self.defocus_angle = defocus_angle
    self.focus_dist = focus_dist
    self.defocus_disk_u = 0
    self.focus_disk_v = 0
    self.lookfrom = lookfrom
    self.lookat = lookat
    self.vup = vup
    self.u = vec3()
    self.v = vec3()
    self.w = vec3()
    self.vfov = vfov
    self.max_depth = max_depth
    self.samples_per_pixel = samples_per_pixel
    self.output = output
    self.aspect_ratio = aspect_ratio
    self.image_width = image_width
    self.image_height = 0
    self.center = point3(0,0,0)
    self.pixel00_loc = point3(0,0,0)
    self.pixel_delta_u = vec3(0,0,0)
    self.pixel_delta_v = vec3(0,0,0)

  def initialize(self):
    self.image_height = round(max(self.image_width/self.aspect_ratio,1))
    self.center = self.lookfrom

    #determin viewport dimentions
    theta = degrees_to_radians(self.vfov)
    h = math.tan(theta/2)
    viewport_height = 2 * h * self.focus_dist
    viewport_width = viewport_height * (self.image_width/self.image_height)

    #calculate the u,v,w unit basis vectors for the camera coordinate frame
    self.w = unit_vector(self.lookfrom - self.lookat)
    self.u = unit_vector(cross(self.vup,self.w))
    self.v = cross(self.w,self.u)

    #calculate the vectors across the horizontal and down the vertical viewport edges
    viewport_u = viewport_width * self.u
    viewport_v = viewport_height * -self.v

    #calculate the horizontal and vertical delta vectors from pixel to pixel
    self.pixel_delta_u = viewport_u / self.image_width
    self.pixel_delta_v = viewport_v / self.image_height

    #calculate location of upper left pixel
    viewport_upper_left = self.center - (self.focus_dist*self.w) - viewport_u/2 - viewport_v/2
    self.pixel00_loc = viewport_upper_left + 0.5 * (self.pixel_delta_u+self.pixel_delta_v)

    #calculate the camera defocus disk basis vectors
    defocus_radius = self.focus_dist * math.tan(degrees_to_radians(self.defocus_angle / 2))
    self.defocus_disk_u = self.u * defocus_radius
    self.defocus_disk_v = self.v * defocus_radius

  
  def pixel_sample_square(self):
    px = -0.5 + random_double()
    py = -0.5 + random_double()
    return (px*self.pixel_delta_u) + (py*self.pixel_delta_v)

  def defocus_disk_sample(self):
    #Returns a random point in the camera defocus disk.
    p = random_in_unit_disk()
    return self.center + (p.x * self.defocus_disk_u) + (p.y * self.defocus_disk_v)
  
  def get_ray(self,x,y):
    #Get a randomly-sampled camera ray for the pixel at location i,j, originating from
    #the camera defocus disk.
    pixel_center = self.pixel00_loc + (x * self.pixel_delta_u) + (y * self.pixel_delta_v)
    pixel_sample = pixel_center + self.pixel_sample_square()

    ray_origin = self.center if self.defocus_angle <= 0 else self.defocus_disk_sample()
    ray_direction = pixel_sample - ray_origin

    return ray(ray_origin,ray_direction)
  
  def render(self,world:hittable_list):
    self.initialize()
    for y in range(self.image_height):
      print("\033[0;0H scanlines remaining: {}    ".format(self.image_height-y))
      for x in range(self.image_width):
        pixel_color = color(0,0,0)
        for sample in range(self.samples_per_pixel):
          r = self.get_ray(x,y)
          pixel_color+=self.ray_color(r,self.max_depth,world)

        scale = 1.0/ self.samples_per_pixel
        

        r = pixel_color.x
        g = pixel_color.y
        b = pixel_color.z

        r*=scale
        g*=scale
        b*=scale

        r = linear_to_gamma(r)
        g = linear_to_gamma(g)
        b = linear_to_gamma(b)

        intensity = interval(0.000,0.999)
        
        r = math.floor(256 * intensity.clamp(r))
        g = math.floor(256 * intensity.clamp(g))
        b = math.floor(256 * intensity.clamp(b))
      
        self.output.plot(x,y,[r,g,b])

    self.output.update()
    self.output.render()


  def ray_color(self,r:ray,depth,world:hittable):
    rec = hit_record()
    if depth <= 0:
      return color(0,0,0)
    if world.hit(r,interval(0.001,999999999999999999999),rec):
      scattered = ray(point3(0,0,0),vec3(0,0,0))
      attenuation = color(1,0,0)
      
      if rec.mat.scatter(r,rec,attenuation,scattered):
        return attenuation*self.ray_color(scattered,depth-1,world)
      return color(0,0,0)

    unit_direction = unit_vector(r.direction)
    a = 0.5*(unit_direction.y + 1.0)
    return (1.0-a)*color(1.0, 1.0, 1.0) + a*color(0.5,0.7,1.0)