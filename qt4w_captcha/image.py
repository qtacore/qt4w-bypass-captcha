# -*- coding: utf-8 -*-

from PIL import Image


def binarize(image):
    """二值化"""
    image = image.convert("L")
    threshold = 100

    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)

    # 图片二值化
    image = image.point(table, "1")
    white_points = 0
    w, h = image.size
    data = image.load()
    for i in range(h):
        for j in range(w):
            if data[j, i] == 1:
                white_points += 1
    if white_points > w * h /2:
        # 反转
        for i in range(h):
            for j in range(w):
                data[j, i] ^= 1
     
    return image


def locate_shadow_area(image):
    """定位阴影区域"""
    w, h = image.size
    data = image.load()
    min_pixel_count = 10
    for i in range(1, h - min_pixel_count):
        for j in range(1, w - min_pixel_count):
            for k in range(min_pixel_count):
                if data[j + k, i - 1] == data[j + k, i]:
                    break
            else:
                # 判断垂直方向是否有连续竖线
                for k in range(min_pixel_count):
                    if data[j - 1, i + k] == data[j, i + k]:
                        break
                else:
                    return j, i
    return -1, -1


def remove_discrete_points(image):
    """移除离散点"""
    w, h = image.size
    data = image.load()
    for i in range(1, h - 1):
        for j in range(1, w - 1):
            if data[j, i] == 0:
                continue
            if (
                data[j - 1, i] == 0
                and data[j + 1, i] == 0
                and data[j, i - 1] == 0
                and data[j, i + 1] == 0
            ):
                data[j, i] = 0
    return image
