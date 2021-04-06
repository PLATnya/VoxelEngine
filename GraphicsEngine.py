from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

import glm

import numpy as np
import pygame as pg

VOXEL_SIZE = 1

class Camera:
    def __init__(self):
        self.position = glm.vec3(0,0,0)
        self.forward = glm.vec3(0,0,1)
        self.up = glm.vec3(0,1,0)

    def Look(self):
        gluLookAt(*(self.position.to_tuple() + self.forward.to_tuple()+self.up.to_tuple()))

    def Rotate(self,deltaX,deltaY):
        glLoadIdentity()
        self.forward = glm.rotateY(self.forward,deltaY)
        self.forward = glm.rotateX(self.forward, deltaX)
        self.Look()
        print('\n....................................................\n')

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

def createWireCube(active, pivot):
    if active:
        cube_vertices = np.array(
            ((1, 1, 1), (1, 1, -1), (1, -1, -1), (1, -1, 1), (-1, 1, 1), (-1, -1, -1), (-1, -1, 1), (-1, 1, -1)))
        cube_edges = np.array(
            ((0, 1), (0, 3), (0, 4), (1, 2), (1, 7), (2, 5), (2, 3), (3, 6), (4, 6), (4, 7), (5, 6), (5, 7)))
        global VOXEL_SIZE

        for cubeEdge in cube_edges:
            for cubeVertex in cubeEdge:
                position = tuple(np.array(cube_vertices[cubeVertex]) * VOXEL_SIZE + pivot)
                glColor3f(0.0,1.0,0.0)
                glVertex3fv(position)


def renderChunk(chunk):
    glBegin(GL_LINES)
    for voxel in chunk.voxels:
        createWireCube(True, np.array(voxel.parent.worldPosition) + np.array(voxel.localPosition))
    glEnd()
