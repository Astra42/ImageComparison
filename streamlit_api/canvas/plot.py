from .polygon import Polygon, Polygon_finder
from .circle import draw_circle
from .rectangle import draw_rectangle
from .regular_polygon import draw_regular_polygon
import random as rm


def random_color(a=0, b=240):
    return (rm.randint(a, b), rm.randint(a, b), rm.randint(a, b))


def random_point(img_shape):
    return (rm.randint(0, img_shape[0]), rm.randint(0, img_shape[1]))


class Plot:
    def __init__(self, img):
        self.img = img
        self.possible_polygons = [Polygon((0, 0), img.shape[:2])]
        self.figures_in_plot = []
        self.possible_figures_draw_methods = {"r": draw_rectangle, "c": draw_circle, "r_p": draw_regular_polygon}

    def draw_figure(self, figure_name, min_figure_square, regular=0):
        finder = Polygon_finder()
        polygon = finder.init_search(self.possible_polygons, figure_name, regular)

        if type(polygon) == type(1):
            return False

        #print(polygon.square)
        if not regular:
            figure = self.possible_figures_draw_methods[figure_name](self.img, polygon, min_figure_square, color=random_color())
            self.figures_in_plot.append(figure)
        else:
            figure = self.possible_figures_draw_methods[figure_name](self.img, polygon, regular, min_figure_square, color=random_color())
            self.figures_in_plot.append(figure)

        outside = figure.outside_min_polygon
        #print(outside.xy, outside.shape)
        first_p = Polygon((polygon.x, polygon.y), (outside.x - polygon.x + outside.w, outside.y - polygon.y))
        second_p = Polygon((polygon.x + first_p.w, polygon.y), (polygon.w - first_p.w, outside.y - polygon.y + outside.h))
        third_p = Polygon((outside.x, outside.y + outside.h), (polygon.w - outside.x + polygon.x, polygon.h - second_p.h))
        fourth_p = Polygon((polygon.x, polygon.y + first_p.h), (polygon.w - third_p.w, polygon.h - first_p.h))
        inside_p = figure.polygon_inside

        new_polygons = [first_p, second_p, third_p, fourth_p, inside_p]
        #new_polygons = filter(lambda x: x.square>=min_figure_square, new_polygons)
        for p in new_polygons:
            self.possible_polygons.append(p)
        return True