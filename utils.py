#########################################
#   File containing helper functions    #
#########################################

from vector3 import *
import pygame as pg
from OpenGL.GL import *
from objLoaderV4 import ObjLoader
from hittable_list import Hittable_list
from sphere import Sphere
from material import Lambertian, Metal

############################################################################
#   Helper function from previous assignments to help create a cube map    #
#   which would be used to render the actual picture once it was done      #
#   being drawn                                                            #
############################################################################
#   Side note for us to change later, this is the function from devkota
#   So we may not need to reference it, but just in case
def load_cubemap_texture(filenames):
    #   Generate a texture ID
    texture_id = glGenTextures(1)

    #   Bind the texture as a cubemap
    glBindTexture(GL_TEXTURE_CUBE_MAP, texture_id)

    #   Define texture parameters
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_NEAREST)
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    #   Define the faces of the cubemap
    faces = [GL_TEXTURE_CUBE_MAP_POSITIVE_X, GL_TEXTURE_CUBE_MAP_NEGATIVE_X,
             GL_TEXTURE_CUBE_MAP_POSITIVE_Y, GL_TEXTURE_CUBE_MAP_NEGATIVE_Y,
             GL_TEXTURE_CUBE_MAP_POSITIVE_Z, GL_TEXTURE_CUBE_MAP_NEGATIVE_Z]

    #   Load and bind images to the corresponding faces
    for i in range(6):
        img_data, img_w, img_h = load_image(filenames[i], format="RGB", flip=False)
        glTexImage2D(faces[i], 0, GL_RGB, img_w, img_h, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)

    #   Generate mipmaps
    glGenerateMipmap(GL_TEXTURE_CUBE_MAP)

    #   Unbind the texture
    glBindTexture(GL_TEXTURE_CUBE_MAP, 0)

    return texture_id

#############################################################################
#   A helper function that would create each of the objects in the scene    #
#############################################################################
#   Somewhat original
def load_spheres():
    #   Initializing variables
    object_list = random_spheres(2)

    #   Returns the list as a form of a list of Hittable objects
    return Hittable_list(object_list)

def random_spheres(num_rand_spheres):
    spheres = []
    material_ground = Lambertian(Vector3(0.5, 0.5, 0.5))
    material_center = Lambertian(Vector3(0.7, 0.3, 0.3))
    material_left = Metal(Vector3(0.8, 0.8, 0.8))
    material_right = Metal(Vector3(0.8, 0.6, 0.2))

    spheres.append(Sphere(Vector3(0, -1000, 0), 1000, material_ground))
        
    for a in range(-num_rand_spheres, num_rand_spheres, 1):
        for b in range(-num_rand_spheres, num_rand_spheres, 1):
            random_mat_value = random.uniform(0, 1)
            center = Vector3(a+0.9*random.uniform(0, 1), 0.2, b+0.9*random.uniform(0, 1))
            if (center - Vector3(4.0, 0.2, 0)).length() > 0.9:
                if random_mat_value < 0.8:  # Diffuse materials
                    spheres.append(Sphere(center, 0.2, Lambertian(Vector3(random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)))))
                else:  # Metal materials
                    spheres.append(Sphere(center, 0.2, Metal(Vector3(0.5*(1 + random.uniform(0, 1)), 0.5*(1 + random.uniform(0, 1)),0.5*(1 + random.uniform(0, 1))))))

    spheres.append(Sphere(Vector3(0.0, 1.0, 0.0), 1.0, material_right))
    spheres.append(Sphere(Vector3(4.0, 1.0, 0.0), 1.0, material_left))
    spheres.append(Sphere(Vector3(-4.0, 1.0, 0.0), 1.0, material_center))
    return spheres



###############################################################################
#   A utility function from previous assignments that would load the image    #
#   and return data about that image to be used when creating the cubemap     #
###############################################################################
#   Another function from Devkota
def load_image(filename, format="RGB", flip=False):
    img = pg.image.load(filename)
    img_data = pg.image.tobytes(img, format, flip)
    w, h = img.get_size()
    return img_data, w, h
