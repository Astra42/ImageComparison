import random as rm
import numpy as np


class Polygon:
    def __init__(self, xy, shape):
        self.xy = xy
        self.x = xy[0]
        self.y = xy[1]
        self.shape = shape
        self.w = shape[0]
        self.h = shape[1]
        self.square = self.w * self.h


class Polygon_finder:
    def __init__(self):
        self.figures = {"r": self.find_for_rectangle, "c":self.find_for_circle, "r_p": self.find_for_circle}

    def find_for_rectangle(self, polygons,caller,n, min_square=500*5):
        polygon_index = rm.choice(range(len(polygons)))
        polygon = polygons.pop(polygon_index)
        while polygon.square<min_square:
            l = len(polygons)
            if l==0:
                print("Все, места нет")
                return 0
            else:
                polygon_index = rm.choice(range(l))
                polygon = polygons.pop(polygon_index)     
        return polygon

    def find_for_circle(self, polygons, caller,n, min_square=500):
        polygon_index = rm.choice(range(len(polygons)))
        polygon = polygons.pop(polygon_index)
        min_r = np.floor((min_square / np.pi) ** (1 / 2)) if caller == "c" else np.floor((2 * min_square / n / np.sin(2 * np.pi / n)) ** (1/2))
        while polygon.w < 2 * min_r or polygon.h < 2 * min_r:
            l = len(polygons)
            if l == 0:
                print("Все, места нет")
                return 0
            else:
                polygon_index = rm.choice(range(l))
                polygon = polygons.pop(polygon_index)
        #print("полигон", polygon.shape)
        return polygon

    def init_search(self, polygons, figure, n):
        return self.figures[figure](polygons, figure, n)