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

    def Look(self):
        gluLookAt(*(self.position.to_tuple() + (self.position + self.forward).to_tuple() + self.up.to_tuple()))

    def Rotate(self, deltaX, deltaY):
        glLoadIdentity()
        self.forward = glm.rotate(self.forward, deltaY, self.up)
        self.right = glm.rotate(self.right, deltaY, self.up)
        self.forward = glm.rotate(self.forward, deltaX, self.right)
        self.Look()

    def MoveForward(self, speed):
        self.position += self.forward * speed
        self.Look()

    def MoveRight(self, speed):
        self.position += glm.cross(self.forward, self.up) * speed
        self.Look()


main_camera = Camera()


def GraphicSetup():
    pg.init()
    display = (600, 400)
    pg.display.set_mode(display, DOUBLEBUF | OPENGL)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    main_camera.Look()


def clearScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


def createWireCube(active, pivot, color):
    if active:
        cube_vertices = np.array(
            ((1, 1, 1), (1, 1, -1), (1, -1, -1), (1, -1, 1), (-1, 1, 1), (-1, -1, -1), (-1, -1, 1), (-1, 1, -1)))
        cube_edges = np.array(
            ((0, 1), (0, 3), (0, 4), (1, 2), (1, 7), (2, 5), (2, 3), (3, 6), (4, 6), (4, 7), (5, 6), (5, 7)))
        global VOXEL_SIZE

        for cubeEdge in cube_edges:
            for cubeVertex in cubeEdge:
                position = tuple(np.array(cube_vertices[cubeVertex]) * VOXEL_SIZE + pivot)
                glColor3f(*color)
                glVertex3fv(position)


def renderChunk(chunk):
    glBegin(GL_LINES)
    for voxel in chunk.voxels:
        createWireCube(True, np.array(voxel.parent.worldPosition) + np.array(voxel.localPosition), voxel.color)
    glEnd()
