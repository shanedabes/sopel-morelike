#!/usr/bin/env python

import pronouncing
import hyphen
import re
import random
from sopel.module import commands
from sopel.config.types import StaticSection, ListAttribute
from sopel.db import SopelDB

h_en = hyphen.Hyphenator('en_US')


class MLSection(StaticSection):
    sub_words = ListAttribute('sub_words')
    ignored_words = ListAttribute('ignored_words')


def setup(bot):
    bot.config.define_section('morelike', MLSection)

    # create a dictionary with words and their rhyming phonemes
    def get_phones(x):
        return pronouncing.rhyming_part(pronouncing.phones_for_word(x)[0])
    bot.memory['sub_words'] = {i: get_phones(i)
                               for i in bot.config.morelike.sub_words}
    bot.memory['ignored_words'] = bot.config.morelike.ignored_words


def configure(config):
    config.define_section('morelike', MLSection, validate=False)
    config.morelike.configure_setting('sub_words', 'enter words to subsitute')
    config.morelike.configure_setting('ignored_words', 'enter words to ignore')


def trans_word(curr_word, sub_words=[], ignored_words=[]):
    # return if word is in ignored word lists
    if curr_word in ignored_words:
        return curr_word
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
    rep_words = [(i, sub_words[i]) for i in sub_words
                 if sub_words[i] in word_phones]
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
    # if an argument is passed to the command, use it as the line
    if trigger.group(2):
        line = trigger.group(2).strip()
    # if no argument has been passed, use the most recent message
    else:
        db = SopelDB(bot.config)
        query = db.execute(
            'SELECT * from nick_values '
            'WHERE key = "seen_timestamp" '
            'OR key = "seen_message"'
            'ORDER BY "nick_id", "key"').fetchall()
        messages = zip(*[iter(i[2] for i in query)]*2)
        line = max(messages, key=lambda x: x[1])[0].replace('"', '')

    sw, iw = bot.memory['sub_words'], bot.memory['ignored_words']
    new_line = ' '.join(trans_word(i, sw, iw) for i in line.split())

    bot.say('{}? More like {}'.format(line, new_line))
