#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# tr!bf tribf@tribf.com

import json

from . import file_util


def dumps(d):
    s = json.dumps(d, ensure_ascii=False)
    return s


def load(file):
    with open(file, encoding="utf8") as f:
        return json.load(f)


def dump(output_file, d):
    output_file = file_util.resolve_filepath(output_file)
    file_util.ensure_dir(output_file.parent)

    with open(output_file, "w") as f:
        json.dump(d, f)

    print(f"write json file: {output_file}")


def dump_pretty(output_file, obj):
    output_file = file_util.resolve_filepath(output_file)
    file_util.ensure_dir(output_file.parent)

    with open(output_file, "w") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
