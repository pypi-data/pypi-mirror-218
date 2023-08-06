#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# tr!bf tribf@tribf.com

import base64
import math

import cv2
import numpy as np
from numpy import newaxis
from PIL import Image

from ..vision import file_util, os_util


def imread(img_file, use_gray=False):
    img_file = file_util.resolve_filepath(img_file)

    if img_file.suffix in {".tif", ".tiff"} and os_util.is_windows():
        import tifffile as tiff

        img = tiff.imread(str(img_file))
    else:
        img = cv2.imread(str(img_file), cv2.IMREAD_UNCHANGED)

    if use_gray:
        h, w, c = cv2_hwc(img)
        if c != 1:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img


def imwrite(output_file, img):
    output_file = file_util.resolve_filepath(output_file)
    file_util.ensure_dir(output_file.parent)
    cv2.imwrite(str(output_file), img)
    print(f"write image file: {output_file}")


def imwrite_rgb(output_file, img):
    bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    imwrite(output_file, bgr)


def resize(img, h, w):
    img = cv2.resize(img, (w, h))
    return img


def get_shape_pil(f):
    img = Image.open(f)
    width, height = img.size[0], img.size[1]
    return width, height


def keepratio_wh(w, h, w1):
    r = w1 / w
    return int(w1), int(h * r)


def cv2_to_base64(image):
    data = cv2.imencode(".jpg", image)[1]
    return base64.b64encode(data.tobytes()).decode("utf8")


def base64_to_cv2(b64str):
    data = base64.b64decode(b64str.encode("utf8"))
    data = np.fromstring(data, np.uint8)
    data = cv2.imdecode(data, cv2.IMREAD_COLOR)
    return data


def min_area_rect(points):
    # minAreaRect 返回的width与height不是按照长短来定义的
    if isinstance(points, list):
        points = np.array(points, dtype=np.float32)
    (cx, cy), (w, h), deg = cv2.minAreaRect(points)
    return (cx, cy), (w, h), deg


def min_area_rect_points(points):
    rect = min_area_rect(points)
    return cv2.boxPoints(rect)


def bounding_rect(points):
    if isinstance(points, list):
        points = np.array(points, dtype=np.float32)
    return cv2.boundingRect(points)


def find_root_contours(img):
    cnts, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    root_contour_idx = np.where(hierarchy[0][:, 3] == -1)[0]
    root_contours = [cnts[i] for i in root_contour_idx]
    return root_contours


def max_area_contour(contours):
    if len(contours) == 1:
        return contours[0]

    contours.sort(key=lambda cnt: cv2.contourArea(cnt), reverse=True)
    return contours[0]


def sort_contours_by_area(contours):
    areas = [cv2.contourArea(c) for c in contours]
    idx = np.argsort(areas)
    return [contours[i] for i in idx], [areas[i] for i in idx]


def filter_contours_by_area(contours, min_area):
    areas = [cv2.contourArea(c) for c in contours]
    contours, areas = zip(*[(c, a) for c, a in zip(contours, areas) if min_area <= a])
    return contours, areas


def cv2_moment_center(arr):
    moments = cv2.moments(arr)
    cx = moments["m10"] / moments["m00"]
    cy = moments["m01"] / moments["m00"]
    return cx, cy


def color_remap(im_gray):
    im_color = cv2.applyColorMap(im_gray, cv2.COLORMAP_JET)
    return im_color


def get_color_map_list(num_classes):
    color_map = num_classes * [0, 0, 0]
    for i in range(0, num_classes):
        j = 0
        lab = i
        while lab:
            color_map[i * 3] |= ((lab >> 0) & 1) << (7 - j)
            color_map[i * 3 + 1] |= ((lab >> 1) & 1) << (7 - j)
            color_map[i * 3 + 2] |= ((lab >> 2) & 1) << (7 - j)
            j += 1
            lab >>= 3
    color_map = [color_map[i : i + 3] for i in range(0, len(color_map), 3)]
    # return color_map
    return np.array(color_map).astype("uint8")


def gray2pseudo(gray_image, color_map=None):
    if color_map is None:
        color_map = get_color_map_list(256)

    c1 = cv2.LUT(gray_image, color_map[:, 0])
    c2 = cv2.LUT(gray_image, color_map[:, 1])
    c3 = cv2.LUT(gray_image, color_map[:, 2])
    pseudo_img = np.dstack((c1, c2, c3))
    return pseudo_img


def mask2color(lbl, color_map):
    lbl_pil = Image.fromarray(lbl.astype(np.uint8), mode="P")
    lbl_pil.putpalette(color_map)
    img = np.array(lbl_pil)
    return img


def connectedComponentsWithStats(img):
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(img, connectivity=8, ltype=cv2.CV_32S)
    return num_labels, labels, stats, centroids


def block_otsu(image, row_blocks, col_blocks):
    rows, cols = image.shape
    rows_c, cols_c = math.ceil(rows / row_blocks), math.ceil(cols / col_blocks)
    otsu = np.empty_like(image)

    for r in range(row_blocks):
        r_start = r * rows_c
        for c in range(col_blocks):
            c_start = c * cols_c
            block = image[r_start : r_start + rows_c, c_start : c_start + cols_c]
            _, block = cv2.threshold(block, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            otsu[r_start : r_start + rows_c, c_start : c_start + cols_c] = block
    return otsu


def adj_bbox(rect, width, height):
    x1, y1, x2, y2 = bbox2xyxy(rect)
    changed = False
    if x1 < 0:
        x1 = 0
        changed = True
    if y1 < 0:
        y1 = 0
        changed = True
    if x2 > width:
        x2 = width
        changed = True
    if y2 > height:
        y2 = height
        changed = True

    if changed:
        rect = xyxy2bbox((x1, y1, x2, y2))
    return changed, rect


def bbox2xyxy(rect):
    x, y, w, h = rect
    return x, y, x + w, y + h


def xyxy2bbox(xyxy):
    x, y, x2, y2 = xyxy
    return x, y, x2 - x, y2 - y


def resize_bbox(rect, rx, ry):
    x, y, w, h = rect
    return round(x * rx), round(y * ry), round(w * rx), round(h * ry)


def center_resize_bbox(rect, rx, ry):
    x, y, w, h = rect
    w1 = w * rx
    h1 = h * ry
    x += (w - w1) / 2
    y += (h - h1) / 2
    return round(x), round(y), round(w1), round(h1)


def merge_bbox_list(bbox_list):
    ...


def crop_rect(image, rect):
    x, y, w, h = rect
    return image[y : y + h, x : x + w]


def past_rect_roi(image, roi, rect):
    x, y, w, h = rect
    image[y : y + h, x : x + w] = roi


def pca_angle(x, y):
    data_pts = np.stack([x, y], axis=1).astype(np.float64)

    mean = np.empty(0)
    mean, eigenvectors, eigenvalues = cv2.PCACompute2(data_pts, mean)
    center = (mean[0, 0], mean[0, 1])
    angle = math.atan2(eigenvectors[0, 1], eigenvectors[0, 0])  # orientation in radians
    return center, angle


def extract_points(image, contours):
    mask = np.zeros_like(image)
    cv2.drawContours(mask, contours, -1, 255, -1)

    yx = np.where(mask > 0)
    x = yx[1]
    y = yx[0]
    # y, x = np.where(mask > 0)
    z = image[y, x]

    return np.hstack((x[:, newaxis], y[:, newaxis], z[:, newaxis]))


def cv2_hwc(img):
    if img.ndim == 2:
        channels = 1  # single (grayscale)
    if img.ndim == 3:
        channels = img.shape[-1]
    h, w = img.shape[:2]
    return h, w, channels


def cv2_dilation_mask_with_offset(mask, offset):
    kernel = np.zeros((offset * 2, offset * 2), np.uint8)
    cv2.circle(kernel, (offset, offset), offset, 255, -1)
    dilated = cv2.dilate(mask, kernel, iterations=1)
    return dilated


def cv2_erode_mask_with_offset(mask, offset):
    kernel = np.zeros((offset * 2, offset * 2), np.uint8)
    cv2.circle(kernel, (offset, offset), offset, 255, -1)
    dilated = cv2.erode(mask, kernel, iterations=1)
    return dilated


def order_points_clockwise(pts):
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    tmp = np.delete(pts, (np.argmin(s), np.argmax(s)), axis=0)
    diff = np.diff(np.array(tmp), axis=1)
    rect[1] = tmp[np.argmin(diff)]
    rect[3] = tmp[np.argmax(diff)]
    return rect


def box_pad(box, pad: int, img_shape=None) -> np.array:
    box = np.array(box, dtype=np.int32)
    box[0][0], box[0][1] = box[0][0] - pad, box[0][1] - pad
    box[1][0], box[1][1] = box[1][0] + pad, box[1][1] - pad
    box[2][0], box[2][1] = box[2][0] + pad, box[2][1] + pad
    box[3][0], box[3][1] = box[3][0] - pad, box[3][1] + pad
    if img_shape:
        h, w = img_shape[:2]
        box[:, 0] = np.clip(box[:, 0], 0, w)
        box[:, 1] = np.clip(box[:, 1], 0, h)
    return box


def normalize_image(img):
    img = img - np.min(img)
    img = img / np.max(img)
    result = np.float32(img)
    return result


def adjust_gamma(img, gamma=1.0):
    # build a lookup table mapping the pixel values [0, 255] to their adjusted gamma values
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
    # apply gamma correction using the lookup table
    return cv2.LUT(img, table)


def slow_gamma_correction(img, c=1, g=2.2):
    out = img.copy()
    out /= 255.0
    out = (1 / c * out) ** (1 / g)
    out *= 255
    out = out.astype(np.uint8)
    return out


def ppocr_rec_img_reverse_transform(img):
    img = ((img * 0.5 + 0.5) * 255).astype(np.uint8).transpose((1, 2, 0))
    return img


def get_rotate_crop_image(img, points):
    """
    img_height, img_width = img.shape[0:2]
    left = int(np.min(points[:, 0]))
    right = int(np.max(points[:, 0]))
    top = int(np.min(points[:, 1]))
    bottom = int(np.max(points[:, 1]))
    img_crop = img[top:bottom, left:right, :].copy()
    points[:, 0] = points[:, 0] - left
    points[:, 1] = points[:, 1] - top
    """
    assert len(points) == 4, "shape of points must be 4*2"
    img_crop_width = int(max(np.linalg.norm(points[0] - points[1]), np.linalg.norm(points[2] - points[3])))
    img_crop_height = int(max(np.linalg.norm(points[0] - points[3]), np.linalg.norm(points[1] - points[2])))
    pts_std = np.float32(
        [
            [0, 0],
            [img_crop_width, 0],
            [img_crop_width, img_crop_height],
            [0, img_crop_height],
        ]
    )
    M = cv2.getPerspectiveTransform(points, pts_std)
    dst_img = cv2.warpPerspective(
        img,
        M,
        (img_crop_width, img_crop_height),
        borderMode=cv2.BORDER_REPLICATE,
        flags=cv2.INTER_CUBIC,
    )
    dst_img_height, dst_img_width = dst_img.shape[0:2]
    if dst_img_height * 1.0 / dst_img_width >= 1.5:
        dst_img = np.rot90(dst_img)
    return dst_img


def rotate_bound(image, angle):
    # grab the dimensions of the image and then determine the
    # center
    (h, w) = image.shape[:2]
    (cX, cY) = (w / 2, h / 2)

    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))

    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY

    # perform the actual rotation and return the image
    return cv2.warpAffine(image, M, (nW, nH))
