from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

import glm

import numpy as np
import pygame as pg

VOXEL_SIZE = 1


class Camera:
    def __init__(self):
        self.position = glm.vec3(0, 0, 0)
        self.forward = glm.vec3(0, 0, 1)
        self.right = glm.vec3(1, 0, 0)
        self.up = glm.vec3(0, 1, 0)
        self.yaw = -90.0
        self.pitch = 0

    def look(self):
        gluLookAt(*(self.position.to_tuple() + (self.position + self.forward).to_tuple() + self.up.to_tuple()))

    def rotate(self, delta_x, delta_y):
        glLoadIdentity()
        self.forward = glm.rotate(self.forward, delta_y, self.up)
        self.right = glm.rotate(self.right, delta_y, self.up)
        self.forward = glm.rotate(self.forward, delta_x, self.right)
        self.look()

    def move_forward(self, speed):
        self.position += self.forward * speed
        self.look()

    def move_right(self, speed):
        self.position += glm.cross(self.forward, self.up) * speed
        self.look()


main_camera = Camera()


def graphic_setup():
    pg.init()
    display = (600, 400)
    pg.display.set_mode((0, 0), DOUBLEBUF | OPENGL, FULLSCREEN)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, (display[0] / display[1]), 0.1, 200.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    main_camera.look()


def clear_screen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


def create_wire_cube(active, pivot, color):
    if active:
        cube_vertices = np.array(
            ((1, 1, 1), (1, 1, -1), (1, -1, -1), (1, -1, 1), (-1, 1, 1), (-1, -1, -1), (-1, -1, 1), (-1, 1, -1)))
        cube_edges = np.array(
            ((0, 1), (0, 3), (0, 4), (1, 2), (1, 7), (2, 5), (2, 3), (3, 6), (4, 6), (4, 7), (5, 6), (5, 7)))
        global VOXEL_SIZE

        for cubeEdge in cube_edges:
            for cubeVertex in cubeEdge:
                position = tuple(np.array(cube_vertices[cubeVertex]) * VOXEL_SIZE + np.array([pivot[0], pivot[1], 0]))
                glColor3f(*color)
                glVertex3fv(position)


def render_chunk(chunk):
    glBegin(GL_LINES)
    for voxel in chunk.voxels:
        create_wire_cube(voxel.isActive, np.array(voxel.globalPosition), voxel.color)
    glEnd()
