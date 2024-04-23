from vector3 import *
from PIL import Image
import pygame as pg
from OpenGL.GL import *
import numpy as np
import shaderLoaderV3
import pyrr
import camera
from utils import load_cubemap_texture

if __name__ == '__main__':
    #   Initialize pygame
    pg.init()

    #   Set up OpenGL context version
    pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
    pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)

    #   Create a window for graphics using OpenGL
    #   Originally having the aspect ratio be something other than one would cause a problem with the cubemap
    aspect_ratio = 1
    image_width = 600
    image_height = image_width
    vfov = 45
    lookfrom = Vector3(11, 4, 5)
    lookat = Vector3(0, 0, 0)
    vup = Vector3(0, 1, 0)

    pg.display.set_mode((image_width, image_height), pg.OPENGL | pg.DOUBLEBUF)

    #   Creating the .ppm then converting it into a .png
    cam = camera.Camera(aspect_ratio, image_width, image_height, vfov, lookfrom, lookat, vup)
    cam.load_world(image_width, image_height)
    im = Image.open("images/raybg.ppm")
    im.save("images/raybg.png")

    glClearColor(0.3, 0.4, 0.5, 1.0)
    glEnable(GL_DEPTH_TEST)
    
    shaderProgram_skybox = shaderLoaderV3.ShaderProgram("shaders/skybox/vert_skybox.glsl", "shaders/skybox/frag_skybox.glsl")

    quad_vertices = (
                # Position
                -1, -1,
                1, -1,
                1,  1,
                1,  1,
                -1,  1,
                -1, -1
    )
    vertices = np.array(quad_vertices, dtype=np.float32)

    size_position = 2       # x, y, z
    stride = size_position * 4
    offset_position = 0
    quad_n_vertices = len(vertices) // size_position  # number of vertices

    # Create VA0 and VBO
    vao_quad = glGenVertexArrays(1)
    glBindVertexArray(vao_quad)            # Bind the VAO. That is, make it the active one.
    vbo_quad = glGenBuffers(1)                  # Generate one buffer and store its ID.
    glBindBuffer(GL_ARRAY_BUFFER, vbo_quad)     # Bind the buffer. That is, make it the active one.
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)   # Upload the data to the GPU.

    # Define the vertex attribute configurations
    # we can either query the locations of the attributes in the shader like we did in our previous assignments
    # or explicitly tell the shader that the attribute "position" corresponds to location 0.
    # It is recommended to explicitly set the locations of the attributes in the shader than querying them.
    # Position attribute
    position_loc = 0
    glBindAttribLocation(shaderProgram_skybox.shader, position_loc, "position")
    glVertexAttribPointer(position_loc, size_position, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(offset_position))
    glEnableVertexAttribArray(position_loc)

    shaderProgram_skybox["cubeMapTex"] = 0   # Okay this might be confusing. Here 0 indicates texture unit 0. Note that "cubeMapTex" is a sampler variable in the fragment shader. It is not an integer.

    #   Basically will be using the cubemap as a way to render the scene
    cubemap_images = ["images/raybg.png", "images/raybg.png",
                   "images/raybg.png", "images/raybg.png",
                   "images/raybg.png", "images/raybg.png"]

    cubemap_id = load_cubemap_texture(cubemap_images)

    #   Camera properties
    eye = (0,0,0)
    target = (0, 0, 1)
    up = (0, 1, 0)

    fov = 45
    near = 0.1
    far = 10

    # Run a loop to keep the program running
    draw = True
    while draw:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                draw = False

        # Clear color buffer and depth buffer before drawing each frame
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        view_mat = pyrr.matrix44.create_look_at(eye, target, up)
        projection_mat = pyrr.matrix44.create_perspective_projection_matrix(fov,
                                                                            aspect_ratio, near,  far)

        # remove the translation component from the view matrix because we want the skybox to be static
        view_mat_without_translation = view_mat.copy()
        view_mat_without_translation[3][:3] = [0,0,0]

        # compute the inverse of the view (one without translation)- projection matrix
        inverseViewProjection_mat = pyrr.matrix44.inverse(pyrr.matrix44.multiply(view_mat_without_translation,projection_mat))

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_CUBE_MAP, cubemap_id)

        # ******************* Draw the skybox ************************
        glDepthFunc(GL_LEQUAL)    # Change depth function so depth test passes when values are equal to depth buffer's content
        glUseProgram(shaderProgram_skybox.shader)  # being explicit even though the line below will call this function
        shaderProgram_skybox["invViewProjectionMatrix"] = inverseViewProjection_mat
        glBindVertexArray(vao_quad)
        glDrawArrays(GL_TRIANGLES,
                    0,
                    quad_n_vertices)  # Draw the triangle
        glDepthFunc(GL_LESS)      # Set depth function back to default
        # *************************************************************


        # Refresh the display to show what's been drawn
        pg.display.flip()


    glDeleteVertexArrays(1, vao_quad)
    glDeleteBuffers(1, vbo_quad)
    glDeleteProgram(shaderProgram_skybox.shader)

    pg.quit()   # Close the graphics window
    quit()      # Exit the program