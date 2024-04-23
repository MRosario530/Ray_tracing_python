from vector3 import *
from abc import ABC, abstractmethod
import numpy as np
from interval import Interval
from ray import Ray

class Material(ABC):
    @abstractmethod
    def scatter(self, r_in, rec, attenuation, scattered):
        pass

class Lambertian(Material):
    def __init__(self, albedo):
        self.albedo = albedo

    def scatter(self, r_in, rec):
        scatter_direction = rec.normal + Vector3.random_unit_vector()
        if (scatter_direction.near_zero()):
            scatter_direction = rec.normal
        scattered = Ray(rec.p, scatter_direction)
        attenuation = self.albedo
        return True, attenuation, scattered

class Metal(Material):
    def __init__(self, albedo):
        self.albedo = albedo

    def scatter(self, r_in, rec):
        reflected = Vector3.reflect(Vector3.unit_vector(r_in.direction), rec.normal)
        scattered = Ray(rec.p, reflected)
        attenuation = self.albedo
        return True, attenuation, scattered
    
# class Dielectric(Material): Shelved due to issues with loading refractions.
#     def __init__(self, index_of_refraction):
#         self.index_of_refraction = index_of_refraction

#     def scatter(self, r_in, rec):
#         attenuation = Vector3(1.0,1.0,1.0)
#         if rec.front_face:
#             refraction_ratio = (1.0/self.index_of_refraction)
#         else:
#             refraction_ratio = self.index_of_refraction

#         unit_direction = Vector3.unit_vector(r_in.direction)
#         refracted = Vector3.refract(unit_direction, rec.normal, refraction_ratio)

#         scattered = Ray(rec.p, refracted)

#         return True, attenuation, scattered 