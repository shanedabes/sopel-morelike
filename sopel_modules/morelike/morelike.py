# coding=utf-8


from __future__ import (unicode_literals, absolute_import, division,
                        print_function)

from sopel import module


def configure(config):
    pass


def setup(bot):
    pass


def clean_word(w):
    return ''.join(i for i in w if i.isalnum())


@module.commands('morelike')
def hello_world(bot, trigger):
    bot.say('Hello, world!')
