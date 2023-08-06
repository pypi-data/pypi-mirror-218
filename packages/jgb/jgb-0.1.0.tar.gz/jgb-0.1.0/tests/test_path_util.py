#!/usr/bin/env python
# -*- coding: utf-8 -*-
# tr!bf tribf@tribf.com
from unittest import TestCase


class TestPathUtil(TestCase):

    def setUp(self) -> None:
        from tpcu import app_util
        self.app_home = app_util.resolve_app_home(__file__, False)

    def test_resolve(self):
        from tpcu import path_util
        from pathlib import Path

        self.assertEqual(self.app_home / 'hhh', path_util.resolve(self.app_home, './hhh'))
        self.assertEqual(Path("/home/tribf"), path_util.resolve(self.app_home, '/home/tribf'))

        user = "tribf"
        dst = Path("/home/{}".format(user))
        self.assertEqual(dst, path_util.resolve(self.app_home, '/home/{{user}}', {"user": user}))

        self.assertEqual(dst, path_util.resolve(self.app_home, '{{HOME}}'))

