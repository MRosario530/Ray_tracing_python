#   Reference/Supplementary Guide for these functions: 
#   https://raytracing.github.io/books/RayTracingInOneWeekend.html

class Ray:
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction

    def pointOnRay(self, time):
        return self.origin + (self.direction * time)