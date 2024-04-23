#   Reference/Supplementary Guide for these functions: 
#   https://raytracing.github.io/books/RayTracingInOneWeekend.html
#   https://github.com/shiva-kannan/RayTracingInOneWeekend-Python/blob/hittable_class/src/hittable.py

from vector3 import *
from abc import ABC, abstractmethod
import numpy as np
from interval import Interval

class Hittable(ABC):
    @abstractmethod
    def hit(self, r, ray_t, hit_record):
        pass

class Hit_record:
    def __init__(self, t=0.0, p=Vector3(0.0, 0.0, 0.0), normal=Vector3(0.0, 0.0, 0.0)):
        self.t = t
        self.p = p
        self.normal = normal
        self.front_face = False
        self.material = None

    def set_face_normal(self, r, outward_normal):
        self.front_face = np.dot(r.direction, outward_normal) < 0
        if self.front_face:
            self.normal = outward_normal
        else:
            self.normal = outward_normal * -1