#!/usr/bin/env python
# -*- coding: utf-8 -*-
# tr!bf tribf@tribf.com

import os
from enum import Enum
from pathlib import Path

import yaml
from attrdict import AttrDict

from . import file_util, log_util, os_util


class AppRunType(Enum):
    DEV = ("dev",)
    TEST = "test"
    PROD = "prod"


def get_app_run_type():
    run_type = os.environ.get("APP_RUN_TYPE", "dev").lower()
    if run_type is None:
        return AppRunType.DEV
    elif run_type == "dev":
        return AppRunType.DEV
    elif run_type == "test":
        return AppRunType.TEST
    elif run_type == "prod":
        return AppRunType.PROD
    else:
        return AppRunType.DEV


def load_settings(filepath):
    with open(filepath) as f:
        settings = AttrDict(yaml.load(f, Loader=yaml.FullLoader))
        return settings


def resolve_app_home(filepath, chdir=True):
    app_home = os.environ.get("APP_HOME")
    if app_home is None:
        app_home = Path(filepath).resolve().parents[1]
    else:
        app_home = Path(app_home)

    if chdir:
        os.chdir(app_home)
    return app_home


def resolve_app_home_prod(app_name, chdir=True):
    name = app_name.replace(" ", "_")

    if os_util.is_windows():
        app_home = Path(os.environ.get("APPDATA")) / f"Roaming/.{name}"
    elif os_util.is_linux():
        app_home = Path(os.environ.get("HOME")) / f".{name}"
    else:
        app_home = Path(os.environ.get("HOME")) / f".{name}"

    if chdir and app_home.exists():
        os.chdir(app_home)

    return app_home


class BaseAppConfig:
    def __init__(self, app_home, cfg_root_name):
        cfg_file = app_home / "conf/config-dev.yml"
        if not cfg_file.exists():
            cfg_file = app_home / "conf/config.yml"

        print("load config from {}".format(cfg_file))
        self._settings = load_settings(cfg_file)

        self.cfg = AttrDict(self._settings[cfg_root_name])
        self.app_home = app_home

        file_util.ensure_dir(app_home / "logs")

        logging_cfg_file = app_home / self._settings.log_cfg

        print("setup logging from {}".format(logging_cfg_file))
        log_util.setup_logging(logging_cfg_file)

    def get_param(self, dot_str, default):
        keys = dot_str.split(".")
        node = self.cfg
        for k in keys:
            if k in node:
                node = node[k]
            else:
                return default
        return node
