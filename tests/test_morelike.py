#!/usr/bin/env python
# coding=utf-8
from __future__ import (unicode_literals, absolute_import, division,
                        print_function)

import unittest
import pytest

from sopel_modules.morelike import morelike

import pronouncing
import pyphen


def test_clean_word():
    assert morelike.clean_word('#hel_lo+') == 'hello'


def test_get_pronounciation():
    expected = 'HH AH0 L OW1'

    assert morelike.get_pronounciation('hello') == expected


def test_get_no_pronounciation():
    assert morelike.get_pronounciation('aksjga') is None


def test_get_syllables():
    expected = ['to', 'mor', 'row']

    assert morelike.get_syllables('tomorrow') == expected
