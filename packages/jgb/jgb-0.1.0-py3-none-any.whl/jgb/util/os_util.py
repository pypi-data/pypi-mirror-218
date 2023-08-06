#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# tr!bf tribf@tribf.com

import platform


def get_default_ip():
    import netifaces

    gws = netifaces.gateways()
    addrs = netifaces.ifaddresses(gws["default"][netifaces.AF_INET][1])
    return addrs[netifaces.AF_INET][0]["addr"]


def is_linux():
    return platform.system() == "Linux"


def is_windows():
    return platform.system() == "Windows"
