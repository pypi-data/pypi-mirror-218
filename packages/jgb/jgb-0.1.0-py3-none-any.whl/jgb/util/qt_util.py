#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# tr!bf tribf@tribf.com

from PyQt5 import uic


def ui2py(ui_file, py_file):
    with open(ui_file, encoding="UTF-8") as ui_file:
        with open(py_file, "w", encoding="UTF-8", newline="\n") as py_ui_file:
            uic.compileUi(ui_file, py_ui_file)
