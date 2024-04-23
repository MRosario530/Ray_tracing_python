#   Reference/Supplementary Guide for these functions: 
#   https://raytracing.github.io/books/RayTracingInOneWeekend.html

import numpy as np
from hittable import Hittable

class Sphere(Hittable):
    def __init__(self, center, radius, mat):
        self.center = center
        self.radius = radius
        self.mat = mat

    def hit (self, r, ray_t, rec):
        oc = r.origin - self.center
        a = r.direction.length_squared()
        half_b = np.dot(oc, r.direction)
        c = oc.length_squared() - self.radius*self.radius

        discriminant = half_b*half_b - a*c
        if (discriminant < 0): return False
        sqrtd = np.sqrt(discriminant)

        root = (-half_b - sqrtd) / a
        if not ray_t.surrounds(root):
            root = (-half_b + sqrtd) / a
            if not ray_t.surrounds(root):
                return False

        rec.t = root
        rec.p = r.pointOnRay(rec.t)
        outward_normal = (rec.p - self.center) / self.radius
        rec.set_face_normal(r, outward_normal)
        rec.material = self.mat

        return True