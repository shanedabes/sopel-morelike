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
    # return if more than one word is passed
    if ' ' in curr_word:
        return curr_word
    # strip non alphanumeric characters from word
    curr_word = ''.join(i for i in curr_word if i.isalnum())
    # get the phonemes for the current word
    word_phone_list = pronouncing.phones_for_word(curr_word)
    # if no phonemes were found return the current word
    if not word_phone_list:
        return curr_word
    # pick the first pronunciation, it's usually accurate
    word_phones = word_phone_list[0]
    # if the number of syllables is 1, no need to use hyphen to split
    if pronouncing.syllable_count(word_phones) == 1:
        word_syllables = [curr_word]
    else:
        # use hyphen to split the word into syllables
        word_syllables = h_en.syllables(curr_word)
        # if the word couldn't be split, return the original word
        if not word_syllables:
            return curr_word
    # if hyphen's syllable count doesn't match pronouncing's, return the word
    if pronouncing.syllable_count(word_phones) != len(word_syllables):
        return curr_word
    # use any of our words that exist in the phoneme for the current word
    rep_words = [(i, words[i]) for i in words if words[i] in word_phones]
    # if no words match, return the current word
    if not rep_words:
        return curr_word
    # pick one of our matched words to be our new syllable
    new_syl, new_syl_pronounciation = random.choice(rep_words)
    # use regex to just find the vowel within our word's phoneme
    new_syl_vowel = re.search(r'(.*\d)', new_syl_pronounciation).group()
    # use regex to find the vowel of our phoneme within our current word
    syllable_index = re.findall(r'\w+\d', word_phones).index(new_syl_vowel)
    # if our new syllable ends with a vowel, keep the end of the original
    if re.search(r'[aeiouy]$', new_syl):
        new_syl += re.search(r'[^aeiouy]*$',
                                  word_syllables[syllable_index]).group()
    # using the found index, replace the old syllable with the new one
    word_syllables[syllable_index] = new_syl

    # recombine and return
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
