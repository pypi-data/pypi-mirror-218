#!/usr/bin/env python
# -*- coding: utf-8 -*-
# tr!bf tribf@tribf.com

from pathlib import Path
from urllib import parse


def get_filename(url: str):
    return url[url.rfind("/") + 1 :]


def get_filename_from_url(url: str):
    return Path(parse.urlparse(url)).name
