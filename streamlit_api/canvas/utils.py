import numpy as np
import random as rm
from .plot import Plot


def make_image(img_shape, comand, dict_of_k={"r":0.01, "c":0.002, "r_p":0.002}):
    img_s = img_shape[0] * img_shape[1]
    dict_of_min_squares = {}
    for k in dict_of_k:
        dict_of_min_squares[k] = round(img_s * dict_of_k[k])

    comands = [v.split(":") for v in comand.split()]
    img = np.ones(img_shape)
    plot = Plot(img)

    count = 0
    for comand in comands:
        flag = False
        n = 0 if len(comand) == 2 else int(comand[2])
        for _ in range(int(comand[1])):
            figure = comand[0]
            can_continue = plot.draw_figure(figure, dict_of_min_squares[figure], n)

            if can_continue:
                count += 1
            else:
                print(f"Удалось построить {count} фигур")
                flag == True
                break
            
        if flag:
            break

    return plot


def make_random_images(img_shape, count, percent, dict_of_k={"r":0.01, "c":0.002, "r_p":0.002}):
    img_s = img_shape[0] * img_shape[1]
    dict_of_min_squares = {}
    for k in dict_of_k:
        dict_of_min_squares[k] = round(img_s * dict_of_k[k])

    figures = ["r", "c", "r_p"]
    img = np.ones(img_shape)
    plot = Plot(img)

    res = []
    c = 0
    for i in range(count):
        figure = rm.choice(figures)
        n = 0 if figure != "r_p" else rm.randint(3, 10)

        can_continue = plot.draw_figure(figure, dict_of_min_squares[figure], n)

        if can_continue:
            c += 1

        if c / count >= percent and len(res) == 0:
            res.append(plot.img.copy())
        
        if not can_continue:
            print(f"Удалось построить {c} фигур для 1го изображения")
            res.append(plot.img)
            break

    res.append(plot.img)
    return res
