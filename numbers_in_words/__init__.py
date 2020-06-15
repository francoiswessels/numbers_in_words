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

ASSUMPTIONS

    - Numbers can have both whole number and decimal components.
    - Negative numbers are indicated by a "-" prefix.
    - No other prefixes are recognised and will be interpreted to mean that what follows is not a
        number.
    - Suffixes ("km", "kg", "ikko", etc.) can exist and are treated as arbitrary i.e. we don't get
        involved with the meaning of "ikko".
    - Decimal points are "."
    - Thousands separators are "," and are optional. However, if they are present in a string they
        must be used concistently through the string.
    - Only phrases with one number in them will be successfully procesed. If it appears that there
        is more than one number, an invalid response is returned.

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
