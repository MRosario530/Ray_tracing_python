#   Reference/Supplementary Guide for these functions: 
#   https://raytracing.github.io/books/RayTracingInOneWeekend.html

import math
import random
import numpy as np

class Vector3(list):
    def __init__(self, e0, e1, e2):
        self.x = e0
        self.y = e1
        self.z = e2
        self.append(float(e0))
        self.append(float(e1))
        self.append(float(e2))


    def __add__(self, other):
        return Vector3(self[0] + other[0], self[1] + other[1], self[2] + other[2])

    def __sub__(self, other):
        return Vector3(self[0] - other[0], self[1] - other[1], self[2] - other[2])

    def __mul__(self, other):
        return Vector3(self[0] * other, self[1] * other, self[2] * other)

    def __truediv__(self, other):
        return Vector3(self[0] / other, self[1] / other, self[2] / other)
    
    def length_squared(self):
        return (self.x * self.x) + (self.y * self.y) + (self.z * self.z)
    
    def length(self):
        return math.sqrt(self.length_squared())
    
    def near_zero(self):
        s = 1e-8
        return (abs(self.x) < s) and (abs(self.y) < s) and (abs(self.z) < s)

    def convert_unit_vector(self):
        self[0] = self[0]/self.length()
        self[1] = self[1]/self.length()
        self[2] = self[2]/self.length()
    
    def dot(u, v):
        return u[0]*v[0] + u[1]*v[1] + u[2]*v[2]

    def cross(u, v):
        return Vector3(u[1]*v[2] - u[2]*v[1], u[2]*v[0] - u[0]*v[2], u[0]*v[1] - u[1]*v[0])

    def unit_vector(v):
        return Vector3(v[0] / v.length(), v[1] / v.length(), v[2] / v.length())
    
    def random():
        return Vector3(random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1))
    
    def random(min, max):
        return Vector3(random.uniform(min, max), random.uniform(min, max), random.uniform(min, max))
    
    def random_in_unit_sphere():
        while True:
            p = Vector3.random(-1, 1)
            if p.length_squared() < 1:
                return p
            
    def random_unit_vector():
        return Vector3.unit_vector(Vector3.random_in_unit_sphere())
    
    def random_on_hemisphere(normal):
        on_unit_sphere = Vector3.random_unit_vector()
        if (Vector3.dot(on_unit_sphere, normal) > 0.0):
            return on_unit_sphere
        else:
            return on_unit_sphere * -1
        
    def reflect(v, n):
        return v - np.multiply(Vector3.dot(v, n), n) * 2
    
    def refract(uv, n, etai_over_etat): # Function to calculate refractions (primarily for dielectric materials).
        cos_theta = min(Vector3.dot(uv * -1, n), 1.0)
        r_out_perp =  (uv + (n * cos_theta)) * etai_over_etat
        r_out_parallel = -np.sqrt(abs(1.0 - r_out_perp.length_squared())) * n
        return r_out_perp + r_out_parallel  # Application of Snell's law.