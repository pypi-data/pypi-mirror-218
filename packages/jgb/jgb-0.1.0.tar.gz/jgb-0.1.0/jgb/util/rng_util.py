#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# tr!bf tribf@tribf.com


def choice(rng, objs):
    idx = rng.integers(len(objs))
    return objs[idx]
