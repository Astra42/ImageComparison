import cv2
import numpy as np
import random as rm
import math
import os.path


class Point:
    def __init__(self, x,y):
        self.x, self.y = x, y
    def addForEach(self, x, y):
        self.x+=x
        self.y+=y

    def get(self):
        return self.x, self.y

    def __str__(self):
        return f"x{self.x} y{self.y}"
  

class MainFrame:
    def __init__(self, corners, shift=10):
        #shift - небольшой сдвиг чтобы чертеж не накладывался на шаблон
        self.corners = corners
        self.shape = (np.abs(corners[3].x - corners[1].x) - shift, np.abs(corners[3].y - corners[1].y) - shift) #width height
        armin = [corner.x+corner.y for corner in self.corners]
        self.leftcorner = self.corners[armin.index(min(armin))]
        self.leftcorner.addForEach(shift // 2, shift // 2)

    def __str__(self):
        return [str(c) for c in self.corners]
    

def findAllBorderNew(img):
    midy, midx = img.shape[0]//2, img.shape[1]//2
    operations = [lambda p: Point(p.x,p.y-1), lambda p:Point(p.x+1, p.y), lambda p:Point(p.x,p.y+1), lambda p:Point(p.x-1, p.y)]
    corners = [[Point(midx, midy) for _ in range(4)] for i in range(4)]
    runners = [Point(midx, midy) for _ in range(4)]
    for i in range(4):
        for j in range(6):
            while(img[runners[i].y, runners[i].x][0] > 250):
                runners[i] = operations[(i+j)%4](runners[i])
            if j > 1:
                corners[i][j-2] = Point(runners[i].x, runners[i].y)
            opposite_oper = (i+j+2)%4
            for _ in range(3):
                runners[i] = operations[opposite_oper](runners[i])

    s = [np.abs(r[3].x - r[1].x) * np.abs(r[3].y - r[1].y)  for r in corners]
    maxS = np.max(s)

    corners = corners[s.index(maxS)]

    mf = MainFrame(corners)
    return mf


def overlay_transparent(background, overlay, x, y):

    background_width = background.shape[1]
    background_height = background.shape[0]

    if x >= background_width or y >= background_height:
        return background

    h, w = overlay.shape[0], overlay.shape[1]

    if x + w > background_width:
        w = background_width - x
        overlay = overlay[:, :w]

    if y + h > background_height:
        h = background_height - y
        overlay = overlay[:h]

    if overlay.shape[2] < 4:
        overlay = np.concatenate(
            [
                overlay,
                np.ones((overlay.shape[0], overlay.shape[1], 1), dtype = overlay.dtype) * 255
            ],
            axis = 2,
        )

    overlay_image = overlay[..., :3]
    mask = overlay[..., 3:] / 255.0
    background[y:y+h, x:x+w] = (1.0 - mask) * background[y:y+h, x:x+w] + mask * overlay_image
    return background


def getTemplate(scale_percent=50):
    temp_dir = 'content/TemplatesJPG'  #папка шаблонов
    temp_names = os.listdir(temp_dir)
    template = cv2.imread(f"{temp_dir}/{rm.choice(temp_names)}")
    width = int(template.shape[1] * scale_percent / 100)
    height = int(template.shape[0] * scale_percent / 100)
    dim = (width, height)

    template = cv2.resize(template, dim)
    print(f'img shape:{template.shape}')

    mf = findAllBorderNew(template)
    return template, mf


#Base
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
class Polygon:
    def __init__(self, xy, shape):
        self.xy = xy
        self.x = xy[0]
        self.y = xy[1]
        self.shape = shape
        self.w = shape[0]
        self.h = shape[1]
        self.square = self.w*self.h


class Polygon_finder:
  def __init__(self):
    self.figures = {"r": self.find_for_rectangle, "f":self.find_for_rectangle}

  def find_for_rectangle(self, polygons,caller, min_square):
    if len(polygons)==0:
      print("Нет полигонов")
      return 0
    polygon_index = rm.choice(range(len(polygons)))
    polygon = polygons.pop(polygon_index)
    while polygon.w<min_square**(1/2) or polygon.h<min_square**(1/2):
      l = len(polygons)
      if l==0:
        print("Нет полигонов с необходимым мин размером")
        return 0
      else:
        polygon_index = rm.choice(range(l))
        polygon = polygons.pop(polygon_index)

    return polygon

  def init_search(self, polygons, figure, min_square):
    return self.figures[figure](polygons, figure, min_square)



def random_color(a=0, b=240):
  return (rm.randint(a, b), rm.randint(a, b), rm.randint(a, b))

def random_point(img_shape):
  return (rm.randint(0,img_shape[0]), rm.randint(0,img_shape[1]))

def floor(x):
  return math.floor(x)

def ceil(x):
  return math.ceil(x)


#Saver
#----------------------------------------------------------------------------------------------------------------------------------------------------------
def save_images(images, folder_name="media"):
  f_name = f"/{folder_name}/count_of_same_sample.txt"
  if not os.path.exists(f_name):
    open(f_name, 'w').write("0")

  count_of_same_images = int(open(f_name, 'r').read(1))

  for i in range(len(images)):
    cv2.imwrite(f"/{folder_name}/sample{count_of_same_images}_{i}.jpg", images[i])

  open(f_name, 'w').write(str(count_of_same_images+1))


#Figures
#---------------------------------------------------------------------------------------------------------------------------------------------------
class Rectangle:
  def __init__(self, polygon, min_square, padding=0.05):
    #print(type(polygon), type(min_square))
    max_x =np.floor(polygon.w - min_square/polygon.h)
    x = rm.randint(0, max_x)
    max_y = np.floor(polygon.h - min_square/(polygon.w-x))
    y = rm.randint(0, max_y)
    p = (x,y)
    min_w = np.ceil(min_square/(polygon.h - y))
    w = rm.randint(min_w, polygon.w-p[0])
    min_h = np.ceil(min_square/w)
    h = rm.randint(min_h, polygon.h-p[1])
    self.shape = (w,h)
    #print(self.shape[0]*self.shape[1])
    self.start_point = (p[0]+polygon.x, p[1]+polygon.y)
    self.end_point = (self.shape[0] + self.start_point[0], self.shape[1] + self.start_point[1])

    self.outside_min_polygon = Polygon(self.start_point, self.shape)
    self.polygon_inside = Polygon((round(self.start_point[0] + self.shape[0]*padding), round(self.start_point[1] + self.shape[1]*padding)),
                                  (round(self.shape[0]*(1-2*padding)), round(self.shape[1]*(1-2*padding))))
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #self.polygon_inside нужно давать через твой поиск внутренней формы, а не так, как здесь написано
    #структура - Polygon(верхняя левая точка х, верхняя левая точка y, (ширина, высота))


def draw_rectangle(img, polygon, min_square, putting_img):
    #здесь последний уровень вложенности, где можно обратиться к putting_img и найти ее внутренности

    r = Rectangle(polygon, min_square)
    #можешь изменить polygon_inside так: r.polygon_inside= ...
    x,y = r.start_point
    w,h = r.shape
    wi,hi = putting_img.shape[0:2]
    k = min(w/wi, h/hi)
    resized_img = cv2.resize(putting_img, (int(hi*k), int(wi*k)))
    img = overlay_transparent(img, resized_img, y, x)
    # img[x:x+w, y:y+h,:]=resized_img
    # print("log resized_img.shape and .img.shape", resized_img.shape,img.shape, y+h, x+w)
    return r


class Plot:
    def __init__(self, img):
        self.img = img
        self.possible_polygons = [Polygon((0,0), img.shape[:2])]
        self.figures_in_plot = []
        self.possible_figures_draw_methods = {"r": draw_rectangle}
        self.possible_polygons_inside_forms = []

    def draw_figure(self, figure_name, min_figure_square, input_img):
        finder = Polygon_finder()
        used_pol = self.possible_polygons if figure_name=="f" else self.possible_polygons_inside_forms
        polygon = finder.init_search(used_pol, figure_name, min_figure_square)

        if type(polygon)==type(1):
            return False

        #print(polygon.square)
        figure = self.possible_figures_draw_methods["r"](self.img, polygon, min_figure_square, input_img)
        self.figures_in_plot.append(figure)

        outside = figure.outside_min_polygon
        #print(outside.xy, outside.shape)
        first_p = Polygon((polygon.x, polygon.y), (outside.x-polygon.x + outside.w, outside.y-polygon.y))
        second_p = Polygon((polygon.x + first_p.w, polygon.y), (polygon.w-first_p.w, outside.y-polygon.y+outside.h))
        third_p = Polygon((outside.x, outside.y+outside.h), (polygon.w-outside.x+polygon.x, polygon.h-second_p.h))
        fourth_p = Polygon((polygon.x, polygon.y+first_p.h), (polygon.w-third_p.w, polygon.h-first_p.h))
        inside_p = figure.polygon_inside
        if figure_name=="f":
            self.possible_polygons_inside_forms.append(inside_p)

        new_polygons = [first_p, second_p, third_p, fourth_p]
        #new_polygons = filter(lambda x: x.square>=min_figure_square, new_polygons)
        for p in new_polygons:
            if figure_name=="f":
                self.possible_polygons.append(p)
            else:
                self.possible_polygons_inside_forms.append(p)

        return True


def make_random_images(count, percent, form_count=4, dict_of_k={"r":0.01, "f":0.1}):
    template, mf = getTemplate()
    img_shape = (mf.shape[1], mf.shape[0], 3)
    img_s = img_shape[0]*img_shape[1]
    dict_of_min_squares = {}
    for k in dict_of_k:
        dict_of_min_squares[k]=round(img_s * dict_of_k[k])

    img = np.ones(img_shape)+254
    plot = Plot(img)

    res = []
    all_results = []
    c = 0
    form_dir = 'content/forms'  #папка форм
    form_names = os.listdir(form_dir)
    for _ in range(form_count):
        form = rm.choice(form_names)
        f = cv2.imread(f"{form_dir}/{form}", -1)
        plot.draw_figure('f', dict_of_min_squares['f'], f)

    figures_dir = 'content/data'   #папка фигур
    figures_names = os.listdir(figures_dir)
    for _ in range(count):
        figure = rm.choice(figures_names)
        fig = cv2.imread(f"{figures_dir}/{figure}", -1)
        can_continue = plot.draw_figure("r", dict_of_min_squares["r"], fig)
        all_results.append(plot.img.copy())

        if can_continue:
            c += 1

        if c / count >= percent and len(res)==0:
            res.append(plot.img.copy())

        if not can_continue:
            if len(res)==0:
                ind = math.floor(len(all_results)*percent)
                res.append(all_results[ind])
                all_results.clear()
            print(f"Удалось построить {c} фигур для 1го изображения")
            res.append(plot.img)
            break
    #размещаем на шаблонах
    # for r in range(len(res)):
    #     res[r] = overlay_transparent(template, res[r], mf.leftcorner.x, mf.leftcorner.y)

    # for r in res:
    #    r = overlay_transparent(template, r, mf.leftcorner.x, mf.leftcorner.y)

    for idx, elem in enumerate(res):
       template_ = template.copy()
       res[idx] = overlay_transparent(template_, elem, mf.leftcorner.x, mf.leftcorner.y)

    # res[0] = overlay_transparent(template, res[0], mf.leftcorner.x, mf.leftcorner.y)

    return res
