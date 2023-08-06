#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# tr!bf tribf@tribf.com

from collections import Counter

import cv2
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import ticker

from ..util import cv_util, file_util

# plt.rcParams["font.sans-serif"].insert(0, "SimHei")
# plt.rcParams["font.sans-serif"].append("SimHei")
plt.rcParams["font.sans-serif"] = ["SimHei", "WenQuanYi Micro Hei"]
plt.rcParams["axes.unicode_minus"] = False


def plt_hist(png, x, title, xlabel, ylabel, **kwargs):
    fig = plt.figure()
    plt.hist(x)

    if kwargs.get("x_percentage", True):
        plt.gca().xaxis.set_major_formatter(ticker.PercentFormatter(xmax=1, decimals=2))

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid()

    plt.savefig(png, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"save png file: {png}")


def plt_bar_of_counts(png, char_list, dict_file, title, xlabel, ylabel):
    lines = file_util.read_text_lines(dict_file)

    char_counts = Counter(char_list)
    data = []
    for c in lines:
        if c not in char_counts:
            continue
        data.append((c, char_counts[c]))

    fig = plt.figure()
    plt.bar([e[0] for e in data], [e[1] for e in data], width=0.8, bottom=0, align="center")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(png, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"save png file: {png}")


def plt_bar_with_count(png, x, counts, title, xlabel, ylabel):
    fig = plt.figure()
    plt.bar(x, counts, width=0.5, bottom=0, align="edge")
    # plt.bar([i*3 for i in range(len(df_cnt))], df_cnt['counts'], width=0.5, bottom=0, align='edge')
    # plt.xticks([i*3 for i in range(len(df_cnt))], df_cnt['rec'])

    plt.xticks(fontsize=8, rotation=70)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(png, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"save png file: {png}")


def plt_grid_imgs(png, img_list, rows, columns):
    fig = plt.figure()

    for i, img in enumerate(img_list):
        fig.add_subplot(rows, columns, i + 1)
        plt.imshow(img)

    plt.setp(plt.gcf().get_axes(), xticks=[], yticks=[])

    plt.subplots_adjust(top=0.5, bottom=0.01, hspace=0.1, wspace=0.1)
    plt.savefig(png, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"save png file: {png}")


class ImagesViewer:
    def __init__(self):
        self.closed = False

    def wait_for_button_press(self):
        while plt.waitforbuttonpress(0.2) is None:
            if self.closed:
                return False
        return True

    def show_img_under_dir(self, base_dir):
        self.closed = False
        base_dir = file_util.resolve_filepath(base_dir)

        fig = plt.figure()
        for f in base_dir.iterdir():
            if not file_util.check_image_file(f.name):
                continue

            img = cv_util.imread(f)

            plt.imshow(img)
            plt.draw()
            if not self.wait_for_button_press():
                break


def show_img_under_dir(d):
    viewer = ImagesViewer()
    viewer.show_img_under_dir(d)


def draw_overlay(img, mask, use_rgb: bool = False, colormap: int = cv2.COLORMAP_JET):
    w, h = img.shape[:2]
    img = cv2.resize(img, (h, w))
    img = np.float32(img) / 255

    heatmap = cv2.applyColorMap(np.uint8(255 * mask), colormap)
    if use_rgb:
        heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)
    heatmap = np.float32(heatmap) / 255

    if np.max(img) > 1:
        raise Exception("The input image should np.float32 in the range [0, 1]")

    cam_img = heatmap + img
    cam_img = cam_img / np.max(cam_img)
    return np.uint8(255 * cam_img)


def plt_imshow(img, title="default"):
    if img.ndim == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.title(title)
    plt.imshow(img)
    plt.show()


def plt_nn_cam_image(png, img_ori, img_cam):
    plt.imshow(img_cam)
    plt.axis("off")
    plt.savefig(png, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"save png file: {png}")

    # 与原图融合
    cam_image = draw_overlay(img_ori, img_cam, use_rgb=True)

    plt.imshow(cam_image)
    plt.axis("off")
    png2 = png.parent / f"{png.stem}-overlay.png"
    plt.savefig(png2, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"save png file: {png2}")


def plt_nn_ctc_probs(png, img, chars):
    labels = ["{} {}".format(i, "".join(c).replace("blank", "∅")) for i, c in enumerate(chars)]

    x = np.linspace(0, img.shape[1], len(labels), endpoint=False)
    x += x[1]

    plt.imshow(img)
    plt.gca().xaxis.tick_top()
    plt.xticks(x, labels=labels)
    plt.xticks(fontsize=6, rotation=70)
    plt.savefig(png, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"save png file: {png}")


def plt_hbar(png, x, y, xlabel, ylabel, **kwargs):
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    bars = plt.barh(x, y)
    ax.bar_label(bars)

    # plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    plt.savefig(png, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"save png file: {png}")


def plt_pcolormesh(X, Y, Z):
    plt.pcolormesh(X, Y, Z, shading="auto")
    # plt.plot(x, y, "ok", label="input point")
    plt.legend()
    plt.colorbar()
    plt.axis("equal")
    plt.show()


def plt_scatter(points: np.ndarray, title="scatter plot", label="colorbar", show=True):
    plt.scatter(points[:, 0], points[:, 1], c=points[:, 2], s=20, cmap="jet", edgecolor="none")
    plt.gca().set_aspect("equal", adjustable="box")
    plt.gca().invert_yaxis()
    plt.colorbar(label=label)
    plt.title(title)
    if show:
        plt.show()


def plt_line(p0, p1, show=True):
    x = [p0[0], p1[0]]
    y = [p0[1], p1[1]]
    plt.plot(x, y, "-")
    if show:
        plt.show()


def plt_marker(x, y, size=10, m="0", show=True):
    plt.scatter(x, y, s=size, c="red", marker=m)
    if show:
        plt.show()


def plt_show_bgr(bgr, show=True):
    rgb = bgr[..., ::-1].copy()
    plt.imshow(rgb)
    plt.gca().set_aspect("equal", adjustable="box")
    if show:
        plt.show()


def sns_scatterplot(png, df, x, y, **kwargs):
    import seaborn as sns

    file_util.ensure_dir(png.parent)

    sns.scatterplot(data=df, x=x, y=y, **kwargs.get("sns_kwargs", {}))
    plt.grid()
    plt.savefig(png, bbox_inches="tight", dpi=300)
    print(f"save png file: {png}")
