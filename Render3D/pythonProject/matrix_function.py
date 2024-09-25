import numpy as np

def translate(pos):
    tx, ty, tz = pos
    
    return np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [tx, ty, tz, 1],
    ])

def rot_x(a):
    return np.array([
        [1, 0, 0, 0],
        [0, np.cos(a), np.sin(a), 0],
        [0, -np.sin(a), np.cos(a), 0],
        [0, 0, 0, 1],
    ])

def rot_y(a):
    return np.array([
        [np.cos(a), 0, np.sin(a), 0],
        [0, 1, 0, 0],
        [-np.sin(a), 0, np.cos(a), 0],
        [0, 0, 0, 1],
    ])

def rot_z(a):
    return np.array([
        [np.cos(a), np.sin(a), 0, 0],
        [-np.sin(a), np.cos(a), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ])


def scale(s):
    return np.array([
        [s, 0, 0, 0],
        [0, s, 0, 0],
        [0, 0, s, 0],
        [0, 0, 0, 1],
    ])
