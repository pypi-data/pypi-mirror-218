#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# tr!bf tribf@tribf.com


from functools import cached_property
from pathlib import Path
from xml.dom.minidom import parseString
from xml.etree.ElementTree import Element, SubElement, parse, tostring

import numpy as np

from . import cv_util, file_util, xml_util


def get_labels_txt(d):
    return d / "labels.txt"


def get_val_list_txt(d):
    return d / "val_list.txt"


def get_train_list_txt(d):
    return d / "train_list.txt"


def get_img_dir(d):
    img_dir = file_util.resolve_filepath(d) / "JPEGImages"
    return img_dir


def get_ann_dir(d):
    ann_dir = file_util.resolve_filepath(d) / "Annotations"
    return ann_dir


def resolve_xml_path(img_path: Path):
    ann_dir = get_ann_dir(img_path.parents[1])
    xml_path = ann_dir / f"{img_path.stem}.xml"
    return xml_path


def resolve_img_path(xml_path: Path):
    img_dir = get_img_dir(xml_path.parents[1])
    img_path = img_dir / f"{xml_path.stem}.jpg"
    return img_path


def read_voc_list_txt(txt):
    lines = []
    if not txt.exists():
        return lines

    for line in file_util.read_text_lines(txt):
        img_path, xml_path = map(Path, line.split())
        if not img_path.exists():
            img_path = get_img_dir(txt.parent) / img_path.name
            xml_path = resolve_xml_path(img_path)
        lines.append(f"{img_path} {xml_path}")
    return lines


def merge_dataset(outdir, *dataset_list):
    dst_label_txt = get_labels_txt(outdir)
    train_lines = []
    val_lines = []

    for d in dataset_list:
        train_lines.extend(read_voc_list_txt(get_train_list_txt(d)))
        val_lines.extend(read_voc_list_txt(get_val_list_txt(d)))

        label_txt = get_labels_txt(d)
        if label_txt.exists() and not dst_label_txt.exists():
            file_util.copy(label_txt, dst_label_txt)

    if train_lines:
        file_util.write_text_lines(get_train_list_txt(outdir), train_lines)

    if val_lines:
        file_util.write_text_lines(get_val_list_txt(outdir), val_lines)


def change_xml(root, new_size=None):
    annos = [anno for anno in root.iter()]
    ratio_x, ratio_y = 1, 1
    for ann in annos:
        if new_size is not None:
            w, h = new_size
            if "width" in ann.tag:
                ratio_x = w / int(ann.text)
                ann.text = str(w)
            if "height" in ann.tag:
                ratio_y = h / int(ann.text)
                ann.text = str(h)

        if "object" in ann.tag:
            for ele in list(ann):
                if new_size is not None and "bndbox" in ele.tag:
                    for coor in list(ele):
                        if "xmin" in coor.tag or "xmax" in coor.tag:
                            coor.text = str(int(int(coor.text) * ratio_x))
                        elif "ymin" in coor.tag or "ymax" in coor.tag:
                            coor.text = str(int(int(coor.text) * ratio_y))


def get_annotations(root):
    annos = [anno for anno in root.iter()]
    for ann in annos:
        ...


class Image:
    def __init__(self, img_path: Path, xml_path: Path):
        self.img_path = img_path
        self.xml_path = xml_path

    @cached_property
    def img(self):
        img = cv_util.imread(self.img_path)
        return img

    @cached_property
    def xml_root(self):
        return xml_util.read_xml(self.xml_path)

    def load(self):
        ...

    def resize(self, w, h):
        self.img = cv_util.resize(self.img, h, w)
        change_xml(self.xml_root, new_size=(w, h))

    def dump(self, outdir):
        img_path = get_img_dir(outdir) / self.img_path.name
        xml_path = get_ann_dir(outdir) / self.xml_path.name

        cv_util.imwrite(img_path, self.img)
        xml_util.write_xml(xml_path, self.xml_root)


def load_ann_xml(xml_path):
    from supervision.dataset.formats.pascal_voc import load_pascal_voc_annotations

    return load_pascal_voc_annotations(xml_path)


def save_ann_xml(xml_path: Path, classes, filename, xyxy_list, labels, image_shape):
    import supervision as sv
    from supervision.dataset.formats.pascal_voc import detections_to_pascal_voc

    detections = sv.Detections(np.array(xyxy_list), class_id=np.array(labels))
    xml_str = detections_to_pascal_voc(detections, classes, filename, image_shape)
    file_util.write_text_lines(xml_path, [xml_str])


def obj2xml(xyxy, name):
    root = Element("object")

    object_name = SubElement(root, "name")
    object_name.text = name

    bndbox = SubElement(root, "bndbox")
    xmin = SubElement(bndbox, "xmin")
    xmin.text = str(int(xyxy[0]))
    ymin = SubElement(bndbox, "ymin")
    ymin.text = str(int(xyxy[1]))
    xmax = SubElement(bndbox, "xmax")
    xmax.text = str(int(xyxy[2]))
    ymax = SubElement(bndbox, "ymax")
    ymax.text = str(int(xyxy[3]))
    return root


class VocAnn:
    def __init__(self, filename, xyxy_list, cnames, shape):
        self.filename = filename
        self.xyxy_list = xyxy_list
        self.cnames = cnames
        self.height, self.width, self.depth = shape

    def dumps_xml(self):
        annotation = Element("annotation")

        # Add folder element
        folder = SubElement(annotation, "folder")
        folder.text = "VOC"

        # Add filename element
        file_name = SubElement(annotation, "filename")
        file_name.text = self.filename

        # Add source element
        source = SubElement(annotation, "source")
        database = SubElement(source, "database")
        database.text = "tribf"

        # Add size element
        size = SubElement(annotation, "size")
        w = SubElement(size, "width")
        w.text = str(self.width)
        h = SubElement(size, "height")
        h.text = str(self.height)
        d = SubElement(size, "depth")
        d.text = str(self.depth)

        # Add segmented element
        segmented = SubElement(annotation, "segmented")
        segmented.text = "0"

        # Add object elements
        for xyxy, label in zip(self.xyxy_list, self.cnames):
            next_object = obj2xml(xyxy=xyxy, name=label)
            annotation.append(next_object)

        # Generate XML string
        xml_string = parseString(tostring(annotation)).toprettyxml(indent="  ")
        return xml_string

    def dump_xml(self, xml_path):
        xml_str = self.dumps_xml()
        file_util.write_text_lines(xml_path, [xml_str])


def show_voc_image(img_path):
    import supervision as sv
    from supervision.dataset.formats.pascal_voc import load_pascal_voc_annotations

    from ..visualization import vis_util

    img_path = file_util.resolve_filepath(img_path)
    xml_path = resolve_xml_path(img_path)
    _, detections, class_names = load_pascal_voc_annotations(xml_path)
    image = cv_util.imread(img_path)
    box_annotator = sv.BoxAnnotator()
    annotated_frame = box_annotator.annotate(scene=image, detections=detections, labels=class_names)
    vis_util.plt_imshow(annotated_frame)


def show_voc(voc_dir):
    for img_path in file_util.list_all_imgs(get_img_dir(voc_dir)):
        show_voc_image(img_path)
