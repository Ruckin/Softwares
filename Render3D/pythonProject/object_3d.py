import pygame as pg
from pygame.gfxdraw import textured_polygon
from matrix_function import *
from numba import njit

@njit(fastmath=True)
def any_func(arr, a, b):
    return np.any((arr == a) | (arr == b))

class Object3D:
    def __init__(self, render, vertices='', faces=''):
        self.render = render
        self.vertices = np.array(vertices)
        self.faces = faces
        self.font = pg.font.SysFont('Arial', 30, bold=True)
        self.colorFaces = [(pg.Color('orange'), face) for face in self.faces]
        self.movementFlag = self.drawVertexes = True, False
        self.Label = ''

    def draw(self):
        self.screenProjection()
        self.movement()

    def movement(self):
        if self.movementFlag:
            self.rotate_y(pg.time.get_ticks() % 0.005)

    def screenProjection(self):
        vertices = self.vertices @ self.render.camera.camera_matrix()
        vertices = vertices @ self.render.projection.projectionMatrix
        vertices /= vertices[:, -1].reshape(-1, 1)
        vertices[(vertices > 2) | (vertices < -2)] = 0
        vertices = vertices @ self.render.projection.toScreenMatrix
        vertices = vertices[:, :2]

        for index, colorFaces in enumerate(self.colorFaces):
            color, face = colorFaces
            polygon = vertices[face]
            if not any_func(polygon, self.render.H_WIDTH, self.render.H_HEIGHT):
                pg.draw.polygon(self.render.screen, color, polygon, 1)
                if self.Label:
                    text = self.font.render(self.Label[index], True, pg.Color('white'))
                    self.render.screen.blit(text, polygon[-1])

        if self.drawVertexes:
            for verti in vertices:
                if not any_func(polygon, self.render.H_WIDTH, self.render.H_HEIGHT):
                    pg.draw.circle(self.render.screen, pg.Color('white'), verti, 2)

    def translate(self, pos):
        self.vertices = self.vertices @ translate(pos)

    def scale(self, s):
        self.vertices = self.vertices @ scale(s)

    def rotate_x(self, angle):
        self.vertices = self.vertices @ rot_x(angle)

    def rotate_y(self, angle):
        self.vertices = self.vertices @ rot_y(angle)

    def rotate_z(self, angle):
        self.vertices = self.vertices @ rot_z(angle)

class Axes(Object3D):
    def __init__(self, render):
        super().__init__(render)
        self.vertices = np.array([
            (0, 0, 0, 1),
            (1, 0, 0, 1),
            (0, 1, 0, 1),
            (0, 0, 1, 1)
        ])

        self.faces = np.array([
            (0, 1),
            (0, 2),
            (0, 3)
        ])

        self.colors = [pg.Color('red'), pg.Color('green'), pg.Color('blue')]
        self.colorFaces = [(color, face) for color, face in zip(self.colors, self.faces)]
        self.drawVertices = False
        self.Label = 'XYZ'
