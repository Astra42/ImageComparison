import cv2
from skimage.metrics import structural_similarity as ssim
import numpy as np
from PIL import Image, ImageChops


class Images_comparison:
    def __init__(self, pathA, pathB):
        self.pathA=pathA #пути к картинкам
        self.pathB=pathB
        self.masks = 0

    # метрика SSIM  
    def find_SSIM(self):
        imageA = cv2.imread(self.pathA)
        imageB = cv2.imread(self.pathB)
        ch = 2 if len(imageA.shape) == 3 else None
        (score, diff) = ssim(imageA, imageB, full=True, channel_axis=ch)
        return score

    # возвращает две маски, сходств и различий, по умолчанию используется медианный
    # фильтр с kernel_size=3, чтобы убрать шум, можете отключить его
    # treshold - порог, ниже которого пиксели принимаются за схожие на основании их
    # разности. Применим в случае, когда не нужно учитывать яркость
    def binary_masks(self, use_m_filt=True, kernel_size=3, treshold=5):
        img1 = Image.open(self.pathA)
        img2 = Image.open(self.pathB)
        diff = np.array(ImageChops.difference(img1, img2))
        img = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        if use_m_filt:
        # median_filter(img,kernel_size)
            img = cv2.medianBlur(img, kernel_size)
        similarity = np.vectorize(lambda x: True if x <= treshold else False)(img)
        difference = np.vectorize(lambda x: True if x > treshold else False)(img)
        self.masks = (similarity, difference)
        return similarity, difference

    # возвращает процент вхождений True в маску сходств
    # если маска раньше не нходилась, он найдет ее с дефолтными параметрами
    def bin_mask_fullness(self):
        if type(self.masks) == type(0):
            self.binary_masks()
        h, w = self.masks[0].shape
        count_of_true = self.masks[0].sum().sum()
        return count_of_true / (h * w)