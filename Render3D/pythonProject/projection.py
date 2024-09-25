import numpy as np

class Projection:
    def __init__(self, render):
        NEAR = render.camera.near_plane
        FAR = render.camera.far_plane
        RIGHT = np.tan(render.camera.h_fov / 2)
        LEFT = -RIGHT
        TOP = np.tan(render.camera.v_fov / 2)
        BOTTOM = -TOP

        m00 = 2/(RIGHT - LEFT)
        m11 = 2/(TOP - BOTTOM)
        m22 = (FAR + NEAR)/(FAR - NEAR)
        m32 = 2*FAR*NEAR/(FAR - NEAR)

        self.projectionMatrix = np.array([
            [m00, 0, 0, 0],
            [0, m11, 0, 0],
            [0, 0, m22, 1],
            [0, 0, m32, 0]
        ])

        HW, HH = render.H_WIDTH, render.H_HEIGHT
        self.toScreenMatrix = np.array([
            [HW, 0, 0, 0],
            [0, -HH, 0, 0],
            [0, 0, 0, 1],
            [HW, HH, 0, 1]
        ])