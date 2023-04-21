import random as rm
import numpy as np
import cv2
from math import ceil, floor
from .polygon import Polygon


class Regular_polygon:
    def __init__(self, polygon, n, min_square, color, thickness=1):
        min_r = np.floor((2 * min_square / n / np.sin(2 * np.pi / n)) ** 0.5)
        c = (rm.randint(min_r, polygon.w - min_r), rm.randint(min_r, polygon.h - min_r))
        self.center = (c[0] + polygon.x, c[1] + polygon.y)
        self.r = rm.randint(min_r, 
                            min(c[0], c[1], polygon.w - c[0], polygon.h - c[1]))
        
        alphas = np.arange(0, 2 * np.pi, 2 * np.pi / n) + 2 * np.pi * rm.random()
        self.points = [[self.center[0] + self.r * np.cos(a), self.center[1] + self.r * np.sin(a)] for a in alphas]

        self.color = color
        self.thickness = thickness

        min_x = ceil(min(self.points, key=lambda x: x[0])[0])
        max_x = floor(max(self.points, key=lambda x: x[0])[0])
        min_y = ceil(min(self.points, key=lambda x: x[1])[1])
        max_y = floor(max(self.points, key=lambda x: x[1])[1])

        self.outside_min_polygon = Polygon((min_x, min_y), (max_x-min_x, max_y-min_y))

    
        self.polygon_inside = Polygon((round(self.center[0] - 0.3535 * self.r), round(self.center[1] - 0.3535 * self.r)), 
                                    (round(0.7071 * self.r), round(0.7071 * self.r)))
        # не лучший полигон, пересечение с другими возможно, но так малО, что кажется касанием. Но он побольше
        # self.polygon_inside = Polygon((round(self.center[0] - 0.5 * self.r), round(self.center[1]-0.5 * self.r)), 
        #                             (round(self.r), round(self.r)))


def draw_regular_polygon(img, polygon, n, min_square, color):
    r_p = Regular_polygon(polygon, n, min_square, color)
    cv2.fillPoly(img, [np.array(r_p.points, 'int32')], color)
    return r_p
