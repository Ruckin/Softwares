from fileinput import filename

import pygame as pg
from camera import *
from object_3d import *
from projection import *

class softwareRender:
    def __init__(self):
        pg.init()
        self.RES = self.WIDTH, self.HEIGHT = 800, 600
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        self.FPS = 60
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.create_object_3D()

    def create_object_3D (self):
        self.camera = Camera(self, [-5, 6, -55])
        self.projection = Projection(self)
        self.object = self.getObject('resources/t_34_obj.obj')

    def getObject(self, filename):
        vertex, face = [], []
        with open(filename) as f:
            for line in f:
                if line.startswith('v '):
                    vertex.append([float(i) for i in line.split()[1:]] + [1])
                elif line.startswith('f'):
                    faces = line.split()[1:]
                    face.append([int(face_.split('/')[0]) - 1 for face_ in faces])
        return Object3D(self, vertex, face)

    def draw(self):
        self.screen.fill(pg.Color('darkslategray'))
        self.object.draw()

    def run(self):
        while True:
            self.draw()
            self.camera.Control()
            [exit() for i in pg.event.get() if i.type == pg.QUIT]
            pg.display.set_caption(str(self.clock.get_fps()))
            pg.display.flip()
            self.clock.tick(self.FPS)

if __name__ == '__main__':
    app = softwareRender()
    app.run()