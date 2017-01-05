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
    # strip non alphanumeric characters from word
    curr_word = ''.join(i for i in curr_word if i.isalnum())
    word_phone_list = pronouncing.phones_for_word(curr_word)
    if not word_phone_list:
        return curr_word
    word_phones = word_phone_list[0]
    if pronouncing.syllable_count(word_phones) == 1:
        word_syllables = [curr_word]
    else:
        word_syllables = h_en.syllables(curr_word)
        if not word_syllables:
            return curr_word
    if pronouncing.syllable_count(word_phones) != len(word_syllables):
        return curr_word
    rep_words = [(i, words[i]) for i in words if words[i] in word_phones]
    if not rep_words:
        return curr_word
    rep_word = random.choice(rep_words)
    rep_word_vowel = re.search(r'(.*[0-9])', rep_word[1]).group()
    si = re.findall(r'\w+\d', word_phones).index(rep_word_vowel)
    new_syllable = rep_word[0]
    if re.search(r'[aeiouy]$', new_syllable):
        new_syllable += re.search(r'[^aeiouy]*$', word_syllables[si]).group()
    word_syllables[si] = new_syllable
    out = ''.join(word_syllables)

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
