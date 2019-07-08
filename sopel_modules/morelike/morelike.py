# coding=utf-8


from __future__ import (unicode_literals, absolute_import, division,
                        print_function)

from sopel import module

import pronouncing
import pyphen


def configure(config):
    pass


def setup(bot):
    pass


def clean_word(w):
    return ''.join(i for i in w if i.isalnum())


def get_pronounciation(w):
    phones = pronouncing.phones_for_word(w)
    if phones:
        return phones[0]
    else:
        return None


def get_syllables(w):
    h_en = pyphen.Pyphen(lang='en_US')
    word_syllables = h_en.inserted(w).split('-')
    return word_syllables


@module.commands('morelike')
def hello_world(bot, trigger):
    bot.say('Hello, world!')
