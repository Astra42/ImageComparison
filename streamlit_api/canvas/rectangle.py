import cv2
import numpy as np
import random as rm
from .polygon import Polygon

class Rectangle:
    def __init__(self, polygon, min_square, color, thickness=cv2.FILLED, padding=0.05):
        max_x =np.floor(polygon.w - min_square/polygon.h)
        x = rm.randint(0, max_x)
        max_y = np.floor(polygon.h - min_square / (polygon.w - x))
        y = rm.randint(0, max_y)
        p = (x,y)
        min_w = np.ceil(min_square / (polygon.h - y))
        w = rm.randint(min_w, polygon.w - p[0])
        min_h = np.ceil(min_square / w)
        h = rm.randint(min_h, polygon.h - p[1])
        self.shape = (w, h)
        self.start_point = (p[0] + polygon.x, p[1] + polygon.y)
        self.end_point = (self.shape[0] + self.start_point[0], self.shape[1] + self.start_point[1])
        self.color = color
        self.thickness=thickness

        self.outside_min_polygon = Polygon(self.start_point, self.shape)
        self.polygon_inside = Polygon((round(self.start_point[0] + self.shape[0] * padding), round(self.start_point[1] + self.shape[1] * padding)),
                                    (round(self.shape[0] * (1 - 2 * padding)), round(self.shape[1] * (1 - 2 * padding))))


def draw_rectangle(img, polygon, min_square, color):
    r = Rectangle(polygon, min_square, color)
    cv2.rectangle(img, r.start_point, r.end_point, r.color, r.thickness)
    return r
