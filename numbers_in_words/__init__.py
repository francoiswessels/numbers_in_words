""" Help on package numbers_in_words:

NAME
    numbers_in_words

DESCRIPTION
    A small module that helps with the output of the value of an integer in words.
    The package makes two functions available to achieve this, namely 'number_in_words'
    and 'number_in_words_from_phrase'.

    The two functions allow for the optional use of an LRU cached, at the expense
    of a little bit of additional memory consumption.

    The range of numbers that can be expressed is any negative or positive number where the whole
    number component does not exceed 999,999,999,999,999,999,999,999,999,999,999,999,999,999
    (14 groups of three 9's). The decimal component is limited only by your machine's memory.

CONTENTS
    number_in_words (function)
    number_in_words_from_phrase (function)
    _conditional_cache (module)
    _string_processing (module)

AUTHOR:
    Francois Wessels
    https://github.com/francoiswessels/numbers_in_words
"""


from ._numbers_in_words_modules.string_processing import number_in_words, number_in_words_from_phrase
