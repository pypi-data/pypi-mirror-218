#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# tr!bf tribf@tribf.com

import xml.etree.ElementTree as ET

from . import file_util


def read_xml(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    return root


def write_xml(xml_path, root):
    xml_path = file_util.resolve_filepath(xml_path)
    file_util.ensure_dir(xml_path.parent)

    tree = ET.ElementTree(root)
    tree.write(xml_path, encoding="utf-8", xml_declaration=True)
    print(f"write xml file: {xml_path}")
