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
        self.camera = Camera(self, [0.5, 1, -4])
        self.projection = Projection(self)
        self.object = Object3D(self)
        self.object.translate([0.2, 0.4, 0.2])
        self.axes = Axes(self)
        self.axes.translate([0.7, 0.9, 0.7])
        self.worldAxes = Axes(self)
        self.worldAxes.movementFlag = False
        self.worldAxes.scale(2)
        self.worldAxes.translate([0.00001, 0.00001, 0.00001])
        #self.object.rotate_y(np.pi / 6)

    def draw(self):
        self.screen.fill(pg.Color('darkslategray'))
        self.worldAxes.draw()
        self.axes.draw()
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