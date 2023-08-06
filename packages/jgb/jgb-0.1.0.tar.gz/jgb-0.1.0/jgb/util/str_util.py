#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# wangyamin wangyamin@image-x.com.cn


def ratio_str(a, b):
    r = a / b
    return r, f"{r}({a}/{b})"


def percentage_str(a, b):
    r = a / b
    return r, f"{r:.2%}({a}/{b})"
