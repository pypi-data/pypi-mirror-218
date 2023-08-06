#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# tr!bf tribf@tribf.com

import os
import io
import re
import setuptools
from setuptools import setup

import jgb


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type("")
    with io.open(filename, mode="r", encoding="utf-8") as fd:
        return re.sub(text_type(r":[a-z]+:`~?(.*?)`"), text_type(r"``\1``"), fd.read())


setup(
    name="jgb",
    version=jgb.__version__,
    url="https://github.com/tribf/py_jgb",
    license="MIT",
    author=jgb.__author__,
    author_email=jgb.__email__,
    description="金箍棒",
    long_description=read("readme.md"),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=[],
    extras_require={
        "dev": [
            "flake8",
            "black==22.3.0",
            "isort",
            "twine",
            "pytest",
            "wheel",
            "notebook",
            "mkdocs-material",
            "mkdocstrings[python]",
        ],
    },
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: MacOS",
    ],
    python_requires=">=3.7",
)
