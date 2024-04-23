#   Reference/Supplementary Guide for these functions: 
#   https://raytracing.github.io/books/RayTracingInOneWeekend.html

from hittable import Hittable, Hit_record
from interval import Interval

class Hittable_list(Hittable):
    def __init__(self, hittable_objects):
        self.hittable_objects = hittable_objects

    def hit(self, r, ray_t, rec):
        temp_hit_rec = Hit_record()
        hit_anything = False
        closest_so_far = ray_t.max
        for object in self.hittable_objects:
            if object.hit(r, Interval(ray_t.min, closest_so_far), temp_hit_rec):
                hit_anything = True
                closest_so_far = temp_hit_rec.t
                rec.t = temp_hit_rec.t
                rec.p = temp_hit_rec.p
                rec.normal = temp_hit_rec.normal
                rec.material = temp_hit_rec.material
        return hit_anything