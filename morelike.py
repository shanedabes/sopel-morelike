#!/usr/bin/env python

import pronouncing
import hyphen
import re
import random


words = ['poo', 'crap', 'shit', 'gay', 'dumb', 'arse', 'fuck', 'piss', 'bum', 'tits']
words = {i: pronouncing.rhyming_part(pronouncing.phones_for_word(i)[0])
         for i in words}

h_en = hyphen.Hyphenator('en_GB')


def trans_word(curr_word):
    wp = pronouncing.phones_for_word(curr_word)[0]
    print(wp)
    ws = h_en.syllables(curr_word)
    print(ws)
    if not ws:
        return curr_word
    rw = [(i, words[i]) for i in words if words[i] in wp]
    print(rw)
    if not rw:
        return curr_word
    rwc = random.choice(rw)
    print(rwc)
    rwv = re.search(r'(.*[0-9])', rwc[1]).group()
    print(rwv)
    si = re.findall(r'\w+\d', wp).index(rwv)
    # ws[si] = rwc[0]
    ns = rwc[0]
    print(ns)
    print(ws[si])
    if re.search(r'[aeiouy]$', ns):
        ns += re.search(r'[^aeiou]*$', ws[si]).group()
    print(ns)
    ws[si] = ns
    print(ws)
    out = ''.join(ws)
    print(out)

    return out


if __name__ == '__main__':
    line = input('-> ').strip()

    new_line = ' '.join(trans_word(i) for i in line.split())

    print(new_line)
