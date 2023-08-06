#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# tr!bf tribf@tribf.com

import pickle

from . import file_util


def dump(pkl_file, obj):
    pkl_file = file_util.resolve_filepath(pkl_file)
    file_util.ensure_dir(pkl_file.parent)

    with open(pkl_file, "wb") as f:
        pickle.dump(obj, f)

    print(f"write pickle file: {pkl_file}")


def load(f):
    with open(f, "rb") as f:
        return pickle.load(f)
