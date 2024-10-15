import math
import graphics
from color import color
from ray import ray
from vec3 import point3, vec3, unit_vector, dot, random
from hittable import hittable, hit_record
from hittable_list import hittable_list
from sphere import sphere
from interval import interval
from camera import camera
from materials import lambertian, material, metal, dielectric
from common import pi, random_double


#image
ASPECT_RATIO = 16.0 / 9.0

IMAGE_WIDTH = 80
IMAGE_HEIGHT = round(max(IMAGE_WIDTH/ASPECT_RATIO,1))
window = graphics.window("main",IMAGE_WIDTH,IMAGE_HEIGHT)

#world
world = hittable_list()

ground_material = lambertian(color(0.5,0.5,0.5))
world.add(sphere(point3(0,-1000,0),1000,ground_material))

for a in range(-2,2):
  for b in range(-2,2):
    choose_mat = random_double()
    center = point3()
    center.x = a + 0.9*random_double()
    center.y = 0.2
    center.z = b + 0.9*random_double()
    if (center - point3(4,0.2,0)).length > 0.9:
      if choose_mat < 0.8:
        #diffuse
        albedo = random() * random()
        col = color()
        col.x = albedo.x
        col.y = albedo.y
        col.z = albedo.z
        sphere_material = lambertian(col)
        world.add(sphere(center,0.2,sphere_material))
      elif choose_mat < 0.95:
        #metal
        albedo = random(0.5,1)
        fuzz = random_double(0,0.5)
        col = color()
        col.x = albedo.x
        col.y = albedo.y
        col.z = albedo.z
        sphere_material = metal(col,fuzz)
        world.add(sphere(center,0.2,sphere_material))
      else:
        #glass
        sphere_material = dielectric(1.5)
        world.add(sphere(center,0.2,sphere_material))


material1 = dielectric(1.5)
world.add(sphere(point3(0, 1, 0), 1.0, material1))

material2 = lambertian(color(0.4, 0.2, 0.1))
world.add(sphere(point3(-4, 1, 0), 1.0, material2))

material3 = metal(color(0.7, 0.6, 0.5), 0.0)
world.add(sphere(point3(4, 1, 0), 1.0, material3))


cam = camera(window,ASPECT_RATIO,IMAGE_WIDTH,100,50,point3(13,2,3),point3(0,0,0),vec3(0,1,0),20,0,10)
cam.render(world)

exit()