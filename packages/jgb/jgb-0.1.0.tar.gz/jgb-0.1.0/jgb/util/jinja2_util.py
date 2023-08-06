#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# tr!bf tribf@tribf.com


import jinja2

from . import file_util


def dump_template(output_file, tempo):
    output_file = file_util.resolve_filepath(output_file)
    file_util.ensure_dir(output_file.parent)

    with open(output_file, "w", encoding="UTF-8", newline="\n") as f:
        f.write(tempo)


def create_jinja2_file(output_file, jinja2_temp, cfg):
    with open(jinja2_temp, encoding="UTF-8") as temp:
        template = jinja2.Template(temp.read())
        tempo = template.render(cfg=cfg)
        dump_template(output_file, tempo)
