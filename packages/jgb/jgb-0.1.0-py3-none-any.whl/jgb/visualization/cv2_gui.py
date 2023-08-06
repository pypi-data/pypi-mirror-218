#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# tr!bf tribf@tribf.com

import cv2
import numpy as np


def cv2_show_image(img, window_name="default"):
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.imshow(window_name, img)
    k = cv2.waitKey(0)
    return k


def cv2_check_char(ret, char):
    return ord(char) == ret


def cv2_show_colormap(img, title="default"):
    colormap = cv2.applyColorMap(img, cv2.COLORMAP_JET)
    cv2_show_image(colormap, title)


def cv2_draw_contour(img, contour):
    if isinstance(contour, list):
        contour = np.array(contour, dtype=np.int32)

    if contour.dtype != np.int32:
        contour = contour.astype(np.int32)
    cv2.drawContours(img, [contour], 0, (255, 255, 255), 1)
    return img


def cv2_draw_contours(img, contours, color=(255, 255, 255), thickness=1):
    cv2.drawContours(img, contours, -1, color, thickness)
    return img


def cv2_draw_ellipse(img, ellipse):
    cv2.ellipse(img, ellipse, (255, 255, 255), 1)
    return img


def cv2_draw_rect(img, rect, thickness=1):
    cv2.rectangle(img, rect, (255, 255, 255), thickness)
    return img


def cv2_draw_marker(img, x, y):
    cv2.drawMarker(img, (int(x), int(y)), 0, markerSize=10, thickness=1)
    return img


def cv2_draw_obb(img, rect):
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(img, [box], 0, (255, 255, 255), 1)
    return img
