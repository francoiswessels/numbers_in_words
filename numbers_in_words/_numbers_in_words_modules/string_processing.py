"""Help on package _string_processing:

NAME
    _string_processing

DESCRIPTION
    A private module belonging to numbers_in_words package.

AUTHOR:
    Francois Wessels
    https://github.com/francoiswessels/numbers_in_words
"""

from math import ceil
from functools import lru_cache
from typing import Union, Tuple, cast
from enum import Enum

from . import conditional_cache as cc
from . import number_parts as np
from . import value_maps as maps

conditional_block_cache = cc.ConditionalLRUCache()
conditional_number_cache = cc.ConditionalLRUCache()


def number_in_words_from_phrase(phrase: str, cached_blocks=True, cached_numbers=False) -> str:
    """Finds a number-like substring in a phrase and returns the value in words.

    Arguments:
        phrase -- a collection of words, separated by spaces

    Keyword arguments:
        cached_blocks  -- default True, indicates whether number BLOCKS (substrings) will be cached when
                            procesing a string. This will decrease runtime, but increase memory consumption.
        cached_numbers -- default False, indicates whether entire number strings will be cached when
                            procesing a string. This will decrease runtime, but increase memory consumption.

    Returns:
        str -- the value of a number in words or, 'number invalid' if no suitable
                number was found.
    """

    conditional_block_cache.enabled = cached_blocks
    conditional_number_cache.enabled = cached_numbers

    number_parts = _get_number_parts_from_phrase(phrase)

    if not number_parts.is_valid:
        return "number invalid"

    number_str = _number_in_words_from_parts(number_parts)

    return number_str


@conditional_number_cache
def number_in_words(number: str, cached_blocks=True, cached_numbers=False) -> str:
    """Returns the value of an integer-like string in words.

    Arguments:
        phrase -- a string, representing an integer number

    Keyword arguments:
        cached_blocks  -- default True, indicates whether number BLOCKS (substrings) will be cached when
                            procesing a string. This will decrease runtime, but increase memory consumption.
        cached_numbers -- default False, indicates whether entire number strings will be cached when
                            procesing a string. This will decrease runtime, but increase memory consumption.

    Returns:
        str -- the value of a number in words or, 'number invalid' if no suitable
                number was found."""

    conditional_block_cache.enabled = cached_blocks
    conditional_number_cache.enabled = cached_numbers

    parts = _get_number_parts_from_word(number)

    return _number_in_words_from_parts(parts)


def _number_in_words_from_parts(number_parts: np.NumberParts):
    number_str: str = cast(str, number_parts.integer)
    num_of_blocks = ceil(len(number_str)/3)  # A block is three digits, always
    number_str = number_str.zfill(num_of_blocks*3)

    integer_result = ""
    for i in range(num_of_blocks):
        block_result, block_glue = _get_block_result(number_str[i*3:(i+1)*3])

        if block_result:
            if i == (num_of_blocks - 1):
                if i == 0:  # There was only one block
                    integer_result += block_result
                else:  # The last block, but not the only block
                    integer_result += f"{block_glue}{block_result}"
            elif i == 0:  # The first block, but not the only block
                integer_result += f"{block_result} {maps.block_num_to_thousands_map[num_of_blocks - i - 1]}"
            else:  # Neither the first, nor the last block
                integer_result += f"{block_glue}{block_result} {maps.block_num_to_thousands_map[num_of_blocks - i - 1]}"

    if not integer_result:
        return "zero"

    negative = "negative " if number_parts.negative else ""

    if number_parts.decimals:
        decimals = " ".join([maps.num_to_words_map[d] for d in number_parts.decimals])
        decimals = f" point {decimals}"
        return f"{negative}{integer_result}{decimals}"

    return f"{negative}{integer_result}"


def _get_number_parts_from_phrase(phrase: str) -> np.NumberParts:
    # Only clean up numbers that have a chance of being a number
    maybe_digits = [_get_number_parts_from_word(word) for word in phrase.split(" ") if _is_number_like(word)]

    # If only one number-like string was found and we can actually interpret it as a number,
    # then we have found what we are looking for.
    if len(maybe_digits) == 1 and maybe_digits[0].is_valid:
        return maybe_digits[0]

    return np.NumberParts()


def _is_number_like(word: str) -> bool:
    # If the first char in the string is a number, we deem it number-like
    return word[0].isdigit() or (word[0] == "-" and word[1].isdigit())


@conditional_number_cache
def _get_number_parts_from_word(word: str, separator: str = ",", decimal_point: str = ".") -> np.NumberParts:
    decimals, suffix = "", ""

    while not word[-1].isdigit():  # strip off any suffix
        suffix = f"{word[-1]}{suffix}"
        word = word[:-1]

    last_separator_index, decimal_index = -1, -1
    for i in range(len(word), 0, -1):  # from right to left
        if word[i-1] == decimal_point:
            if decimal_index > -1:  # there can be only one decimal point
                return np.NumberParts()
            decimal_index = i-1
            if last_separator_index > -1:  # if the decimal point is left of a separator, something is wrong
                return np.NumberParts()
        elif word[i-1] == separator:
            if last_separator_index > -1:  # if we had already found a separator character
                if not (last_separator_index - i == 4):  # spacing has to be exactly 3, plus a separator character
                    return np.NumberParts()
                else:
                    last_separator_index = i
            elif decimal_index > -1:  # if we had already found a decimal character
                last_separator_index = i
                if not (decimal_index - last_separator_index == 3):  # spacing has to be exactly 3
                    return np.NumberParts()
            else:
                last_separator_index = i

    if not word[0] == "-":  # there is no negative indicator
        if (last_separator_index - i > 3):
            return np.NumberParts()
        if (decimal_index > -1):
            decimals = word[decimal_index+1:]
            integer = word[:decimal_index].replace(",", "")
        else:
            integer = word.replace(",", "")
        return np.NumberParts(integer, decimals, suffix)

    if (last_separator_index - i > 4):  # we have a negative indicator that makes it 3 + 1
        return np.NumberParts()

    if (decimal_index > -1):
        decimals = word[decimal_index+1:]
        integer = word[1:decimal_index].replace(",", "")
    else:
        integer = word[1:].replace(",", "")
    
    return np.NumberParts(integer, decimals, suffix, True)


@conditional_block_cache
def _get_block_result(block: str) -> Tuple[str, str]:
    num_100 = block[0]
    num_10 = block[1]
    num_1 = block[2]

    words_100, words_10, words_1 = "", "", ""
    glue_100_to_10, glue_10_to_1, block_glue = "", "", ", "

    if not num_100 == "0":  # This block has a 100 value
        words_100 = f"{maps.num_to_words_map[num_100]} hundred"
        if not (num_10 == "0" and num_1 == "0"):  # ... and this block has either a 10 or a 1 value
            glue_100_to_10 = " and "
    elif not (num_10 == "0" and num_1 == "0"):  # This block has NO 100 value and has either a 10 or a 1 value
        block_glue = " and "

    if not (num_10 == "0" or num_1 == "0"):  # There is a 10 and a 1 that need to be joined.
        glue_10_to_1 = "-"

    if num_10 == "1":  # Number is in the teens
        words_teen = maps.num_to_words_map[f"{num_10}{num_1}"]
        block_result = f"{words_100}{glue_100_to_10}{words_teen}"
    else:  # Number is NOT in the teens
        words_10 = "" if num_10 == "0" else maps.num_to_words_map[f"{num_10}0"]
        words_1 = "" if num_1 == "0" else maps.num_to_words_map[num_1]
        block_result = f"{words_100}{glue_100_to_10}{words_10}{glue_10_to_1}{words_1}"

    return block_result, block_glue
