#   Reference/Supplementary Guide for these functions: 
#   https://raytracing.github.io/books/RayTracingInOneWeekend.html

import os
from vector3 import *
from ray import Ray
from OpenGL.GL import *
from hittable import Hit_record
from utils import load_spheres
from interval import Interval
import numpy as np
import random

class Camera:
    def __init__(self, aspect_ratio, image_width, image_height, vfov, lookfrom, lookat, vup):
        self.aspect_ratio = aspect_ratio
        self.image_width = image_width
        self.image_height = image_height
        self.vfov = vfov
        self.lookfrom = lookfrom
        self.lookat = lookat
        self.vup = vup
        self.pixel_delta_u = None
        self.pixel_delta_v = None
        self.pixel00_loc = None
        self.u = None
        self.v = None
        self.w = None

    #################################################################################
    #   This function creates then draws the scene based off of the camera          #
    #   where it will send out rays to get the color of each pixel from the scene   #
    #################################################################################
    #   From the book which also means the github
    def load_world(self, image_width, image_height):

        samples_per_pixel = 3  # Note - Anti aliasing heavily slows down program due to lack of optimization + slowness of python
        max_depth = 3

        world = load_spheres()

        
        # Calculations to determine viewport dimensions.
        focal_length = (self.lookfrom - self.lookat).length()  
        theta = np.deg2rad(self.vfov)
        h = np.tan(theta/2)
        viewport_height = 2 * h * focal_length
        viewport_width = viewport_height * (image_width/image_height)
        camera_center = self.lookfrom

        # Calculating the basis vectors for the camera frame.
        self.w = Vector3.unit_vector(self.lookfrom - self.lookat)
        self.u = Vector3.unit_vector(Vector3.cross(self.vup, self.w))
        self.v = Vector3.cross(self.w, self.u) * -1

        # Calculating the horizontal and vertical viewport edges.
        viewport_u = self.u * viewport_width
        viewport_v = self.v * -1 * viewport_height
        
        # Calculating the delta vectors for going from pixel to pixel.
        self.pixel_delta_u = viewport_u / image_width
        self.pixel_delta_v = viewport_v / image_height

        # Calculate the location of the top left pixel.
        viewport_upper_left = camera_center - (self.w * focal_length) - (viewport_u / 2) - (viewport_v / 2)
        self.pixel00_loc = viewport_upper_left + (self.pixel_delta_u + self.pixel_delta_v) * 0.5 


        path = os.path.join(os.path.dirname(__file__), "images", "raybg.ppm")
        ppm_file = open(path, 'w')
        rows = image_width
        columns = int(image_height)


        title = "P3\n{r} {c}\n255\n".format(r=rows, c=columns)
        ppm_file.write(title)
        for j in range(columns-1, -1, -1):
            print(f'{j} columns remain')
            for i in range(0, rows, 1):
                pixel_color = Vector3(0,0,0)
                for k in range(0, samples_per_pixel, 1):
                    rayr = self.get_ray(i, j, camera_center)
                    pixel_color = pixel_color + self.ray_color(rayr, world, max_depth)
                col = pixel_color / samples_per_pixel
                ir = int(255.99*np.sqrt(col.x))     # Square roots to convert the linear RGB values towards gamma.
                ig = int(255.99*np.sqrt(col.y))
                ib = int(255.99*np.sqrt(col.z))
                value = "{ir} {ig} {ib}\n".format(ir=ir, ig=ig, ib=ib)
                ppm_file.write(value)
        ppm_file.close()

    def pixel_sample_square(self):
        px = -0.5 + random.uniform(0.0, 1.0)
        py = -0.5 + random.uniform(0.0, 1.0)
        return (self.pixel_delta_u * px) + (self.pixel_delta_v * py)

    def get_ray(self, i, j, camera_center):
        pixel_center = self.pixel00_loc + (self.pixel_delta_u * i) + (self.pixel_delta_v * j)
        pixel_sample = pixel_center + self.pixel_sample_square()
        ray_origin = camera_center
        ray_direction = pixel_sample - camera_center
        return Ray(ray_origin, ray_direction)
    
    ###################################################################
    #   This function returns a color depending on if the ray hits    #
    #   something (spheres) or continues off into the sky             #
    ###################################################################
    #   From the book which also means the github
    def ray_color(self, r, world, depth):
        #   Changing the distance shifts the colors to a darker/browner palette.
        rec = Hit_record()
        if (depth <= 0):
            return Vector3(0, 0, 0)

        if (world.hit(r, Interval(0.001, 99999), rec)):
            result, attenuation, scattered = rec.material.scatter(r, rec)
            if result:
                return np.multiply(self.ray_color(scattered, world, depth - 1), attenuation)
            return Vector3(0, 0, 0)
        
        unit_direction = Vector3.unit_vector(r.direction)
        
        #   Graphics trick of scaling it to 0.0 < y < 1.0
        a = 0.5*(unit_direction.y + 1.0)
        
        #   Lerping between (255, 255, 255) which is white to a light shade blue (128, 255*0.7, 255)
        return Vector3(1.0, 1.0, 1.0)*(1.0-a) + Vector3(0.5, 0.7, 1.0)*a