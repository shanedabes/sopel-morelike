#!/usr/bin/env python

import pronouncing
import hyphen
import re
import random
from sopel.module import commands


words = ['poo', 'crap', 'shit', 'gay', 'dumb', 'arse', 'fuck', 'piss', 'bum',
         'tits', 'fart', 'dick', 'cock', 'knob', 'ass']
words = {i: pronouncing.rhyming_part(pronouncing.phones_for_word(i)[0])
         for i in words}

h_en = hyphen.Hyphenator('en_GB')


def trans_word(curr_word):
    if ' ' in curr_word:
        return curr_word
    wp = pronouncing.phones_for_word(curr_word)[0]
    if pronouncing.syllable_count(wp) == 1:
        ws = [curr_word]
    else:
        ws = h_en.syllables(curr_word)
        if not ws:
            return curr_word
    if pronouncing.syllable_count(wp) != len(ws):
        return curr_word
    rw = [(i, words[i]) for i in words if words[i] in wp]
    if not rw:
        return curr_word
    rwc = random.choice(rw)
    rwv = re.search(r'(.*[0-9])', rwc[1]).group()
    si = re.findall(r'\w+\d', wp).index(rwv)
    ns = rwc[0]
    if re.search(r'[aeiouy]$', ns):
        ns += re.search(r'[^aeiouy]*$', ws[si]).group()
    ws[si] = ns
    out = ''.join(ws)

    return out


@commands('morelike')
def morelike(bot, trigger):
    line = trigger.group(2).strip()
    new_line = ' '.join(trans_word(i) for i in line.split())
    bot.say('{}? More like {}'.format(line, new_line))


if __name__ == '__main__':
    line = input('-> ').strip()

    new_line = ' '.join(trans_word(i) for i in line.split())

    print(new_line)
