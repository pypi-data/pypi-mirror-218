#!/usr/bin/env python3
# -*- coding:utf-8 -*-


import yaml

from . import file_util


def load(filepath):
    with open(filepath) as f:
        d = yaml.load(f, Loader=yaml.FullLoader)
        return d


def dump(yml_file, data):
    yml_file = file_util.resolve_filepath(yml_file)
    with open(yml_file, "w") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)
