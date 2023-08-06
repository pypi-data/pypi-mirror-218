#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# tr!bf tribf@tribf.com

import os

import yaml


def save_ppocr_train_config(config):
    save_model_dir = config["Global"]["save_model_dir"]
    os.makedirs(save_model_dir, exist_ok=True)
    yml_file = os.path.join(save_model_dir, "config.yml")
    with open(yml_file, "w") as f:
        yaml.dump(dict(config), f, default_flow_style=False, sort_keys=False)
    print(f"dump yml file: {yml_file}")
