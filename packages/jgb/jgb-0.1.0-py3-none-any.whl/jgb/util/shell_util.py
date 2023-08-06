#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import shutil
import sys
from pathlib import Path
from typing import List

from . import file_util


class ShellOperator:
    def __init__(self, sh: Path, cli: List[str], **kwargs):
        self.sh = sh
        self.cli = cli
        self.outdir = sh.parents[0]
        self.meta = kwargs.get("meta", None)

        self.log_dir = self.outdir / "log"
        file_util.ensure_dir(self.log_dir)

        self.start = self.log_dir / "{}.start".format(self.sh.stem)
        self.done = self.log_dir / "{}.done".format(self.sh.stem)
        self.log = self.log_dir / "{}.log".format(self.sh.stem)

        cli_lines = [
            f"touch {self.start}",
            "",
            *self.cli,
            "",
            f"touch {self.done}",
        ]

        if not self.sh.exists():
            file_util.write_here_sh(self.sh, cli_lines)
            print("generate sh op: {}".format(self.sh))
        else:
            print("sh op exists: {}".format(self.sh))

    def run(self):
        if self.done.exists():
            print("task done: {}".format(self.done))
            return

        if self.start.exists():
            print("task running: {}".format(self.start))
            return

        os.system(f"sh {self.sh}")
