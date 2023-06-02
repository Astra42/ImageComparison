import cv2
import numpy as np
from scipy import stats


def rotate_and_moove(img, alpha, x, y, dop=0):
    alpha = alpha * np.pi / 180
    h, w = img.shape
    w_padding = int(abs(h * np.sin(alpha)))
    h_padding = int(abs(w * np.sin(alpha)))
    x = w_padding if x < w_padding else x
    x = 0 if alpha > 0 else x
    y = h_padding if y < h_padding else y
    y = 0 if alpha < 0 else y
    afine_matrix = np.float32([[np.cos(alpha), np.sin(alpha), x], 
                                [-np.sin(alpha),  np.cos(alpha), y]])
    res = cv2.warpAffine(img, afine_matrix, (w + w_padding + dop * x, h + h_padding + dop * y), borderValue=255)
    return res


def preprocess(img_p, separator=220, resize_k=1, pad = 0):
    img = cv2.imread(img_p)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    bin = np.vectorize(lambda x: 0 if x<separator else 255)
    img = bin(img).astype('uint8')
    if resize_k!=1:
        h,w = img.shape
        img = cv2.resize(img,(int(resize_k*w), int(resize_k*h)))
    if pad>0:
        img = img[pad:-pad,pad:-pad]
    return img


def find_points(img):
    h,w = img.shape
    p1 = ()
    p2 = ()
    eye = 1
    black = 0
    for i, row in enumerate(img[::-1]):
        if black in row:
            ind = np.where(row == black)
            min_ind = ind[0][0]
            max_ind = ind[0][-1]
            p1 = (max_ind if min_ind > w / 2 else min_ind, h - i - 1) 
            eye = 1 if min_ind > w / 2 else -1
            break

    for i, column in enumerate(img.T[::eye]):
        if black in column:
            ind = np.where(column==black)[0][-1]
            x = i if eye>0 else w - 1 - i
            p2 = (x, ind)  
            break

    return [p1, p2]


def binary_masks(i1, i2, use_m_filt=True, kernel_size=3, treshold=5):
    img = i1 - i2
    if use_m_filt:
        img = cv2.medianBlur(img, kernel_size)
    similarity = np.vectorize(lambda x: True if x <= treshold else False)(img).astype('uint8')
    difference = np.vectorize(lambda x: True if x> treshold else False)(img).astype('uint8')
    return similarity, difference


def binary_masks_with_kernel(i1, i2, k=3):
    h,w = i1.shape
    res = np.zeros((h, w))
    for i in range(k, h - k):
        for j in range(k, w - k):
            res[i, j] = i2[i, j] in i1[i - k:i + k + 1, j - k:j + k + 1]

    similarity = cv2.medianBlur(res.astype('uint8'), 3)
    difference = np.vectorize(lambda x: False if x else True)(similarity).astype('uint8')
    return similarity, difference


def without_rot(img1, img2):
    h,w = img1.shape
    cord1 = np.array([[(j, i) for j in range(w)] for i in range(h)])
    h,w = img2.shape
    cord2 = np.array([[(j, i) for j in range(w)] for i in range(h)])

    black1 = cord1[img1 < 220]
    black2 = cord2[img2 < 220]

    max_w1 = np.float32(max(black1, key = lambda x: x[0]))[0]
    max_h1 = np.float32(max(black1, key = lambda x: x[1]))[1]
    max_w2 = np.float32(max(black2, key = lambda x: x[0]))[0]
    max_h2 = np.float32(max(black2, key = lambda x: x[1]))[1]

    dx = -max_w2 + max_w1
    dy = -max_h2 + max_h1
    return np.array([[1, 0, dx],
                    [0, 1, dy]]), (dx, dy)


def reverse_rot(img):
    corners = find_points(img)
    p1 = corners[0]
    p2 = corners[1]
    tg = (p1[1] - p2[1]) / (p1[0] - p2[0])
    alpha = np.arctan(tg)
    alpha = alpha * 180 / np.pi
    #print(alpha)
    rot_img = rotate_and_moove(img, alpha, 0, 0)
    return rot_img, alpha


def image_comparison(img1, img2, comp_func, comp_func_params,
                     separator = 220, use_d_and_e = True, kernels=[3,2]):
    k1, k2 = kernels
    r_i1, a1 = reverse_rot(img1)
    r_i2, a2 = reverse_rot(img2)

    bin = np.vectorize(lambda x: 0 if x > separator else 255)
    if use_d_and_e:
        r_i1 = bin(r_i1).astype('uint8')
        r_i2 = bin(r_i2).astype('uint8')

        kernel1 = np.ones((k1, k1), 'uint8')
        r_i1 = cv2.dilate(r_i1, kernel1, iterations=2)
        r_i2 = cv2.dilate(r_i2, kernel1, iterations=2)

        r_i1 = bin(r_i1).astype('uint8')
        r_i2 = bin(r_i2).astype('uint8')

    M, shift = without_rot(r_i1,r_i2)
    h, w = r_i1.shape
    conv_i2 = cv2.warpAffine(r_i2, M, (w,h),borderValue=255)

    s, d = comp_func(r_i1, conv_i2, *comp_func_params)
    if use_d_and_e:
        kernel2 = np.ones((k2, k2), 'uint8')
        s = cv2.erode(s, kernel2, iterations=1)
    
    return s, d, [a1, a2], shift


class Comparer:
    def __init__(self, path1, path2):
        self.path1 = path1
        self.path2 = path2
        self.separator = 220
        self.resize_k1 = 1
        self.resize_k2 = 1
        self.pad1 = 0
        self.pad2 = 0
        self.all_compr_funcs = {"non_k":binary_masks, "k":binary_masks_with_kernel}
        self.compr_funcs_default_params = {"non_k":(True, 3, 5), "k":(3)}
        self.func = "non_k"
        self.use_d_and_e = True
        self.d_and_e_kernels = [3,2]


    def init_compraision(self):
        img1 = preprocess(self.path1, self.separator, self.resize_k1, self.pad1)
        img2 = preprocess(self.path2, self.separator, self.resize_k2, self.pad2)

        s, d, alphas, shift = image_comparison(img1, img2, self.all_compr_funcs[self.func], self.compr_funcs_default_params[self.func],
                            self.separator, self.use_d_and_e, self.d_and_e_kernels)
        
        h, w = s.shape
        sim_metric = s.sum().sum()/h/w

        return s, d, sim_metric, alphas, shift