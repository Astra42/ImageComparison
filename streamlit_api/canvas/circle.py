import numpy as np
import random as rm
import cv2
from .polygon import Polygon


class Circle:
    def __init__(self, polygon, min_square, color, thickness=cv2.FILLED):
        min_r = np.floor((min_square / np.pi) ** (1/2))
        c = (rm.randint(min_r, polygon.w - min_r), rm.randint(min_r, polygon.h - min_r))
        self.center = (c[0] + polygon.x, c[1] + polygon.y)
        self.r = rm.randint(min_r, 
                            min(c[0], c[1], polygon.w - c[0], polygon.h - c[1]))
    
        self.color = color
        self.thickness = thickness

        self.outside_min_polygon = Polygon((self.center[0] - self.r, self.center[1] - self.r), (2 * self.r, 2 * self.r))
        self.polygon_inside = Polygon((round(self.center[0] - 0.7071 * self.r), round(self.center[1] - 0.7071 * self.r)), 
                                    (round(1.4142 * self.r), round(1.4142 * self.r)))


def draw_circle(img, polygon, min_square, color):
    c = Circle(polygon, min_square, color)
    cv2.circle(img, c.center, c.r, c.color, c.thickness)
    return c
