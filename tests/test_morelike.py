#!/usr/bin/env python
# coding=utf-8
from __future__ import (unicode_literals, absolute_import, division,
                        print_function)

import unittest

from sopel_modules.morelike import morelike

import pronouncing
import pyphen


def test_clean_word():
    assert morelike.clean_word('#hel_lo+') == 'hello'
