from math import ceil as _ceil
from functools import lru_cache as _lru_cache
import typing as _tp


def number_in_words_from_phrase(phrase: str, cached=False) -> str:
    number_str = _get_number_substring(phrase)
    if number_str is None:
        return "number invalid"

    return number_in_words(number_str, cached=cached)


def number_in_words(number_str: str, cached=False) -> str:
    _conditional_cache.enabled = cached

    if not number_str.isdigit():
        raise ValueError(f"The string is not a valid number: {number_str}")

    num_of_blocks = _ceil(len(number_str)/3)  # A block is three digits, always
    number_str = number_str.zfill(num_of_blocks*3)

    result = ""
    for i in range(num_of_blocks):
        block_result, block_glue = _get_block_result(number_str[i*3:(i+1)*3])

        if block_result:
            if i == (num_of_blocks - 1):
                if i == 0:  # There was only one block
                    return block_result
                else:  # The last block, but not the only block
                    result += f"{block_glue}{block_result}"
            elif i == 0:  # The first block, but not the only block
                result += f"{block_result} {_block_num_to_thousands_map[num_of_blocks - i - 1]}"
            else:  # Neither the first, nor the last block
                result += f"{block_glue}{block_result} {_block_num_to_thousands_map[num_of_blocks - i - 1]}"

    return result


def _get_number_substring(phrase: str) -> _tp.Union[str, None]:
    # If the first char in the string is a number, we deem it number-like
    maybe_digits = [word for word in phrase.split(" ") if word[0].isdigit()]

    # If only one number-like string was found and it is actually a number,
    # then we have found what we are looking for.
    if len(maybe_digits) == 1 and maybe_digits[0].isdigit():
        return maybe_digits[0]

    return None


class _ConditionalLRUCache:
    def __init__(self, starting_condition=True):
        self.enabled = starting_condition
        self.f = None

    def __call__(self, f):
        self.f = f

        def wrap(*args, **kwargs):
            if self.enabled:
                return self._cached_call(*args, **kwargs)
            else:
                return f(*args, **kwargs)

        return wrap

    @_lru_cache(maxsize=999)
    def _cached_call(self, *args, **kwargs):
        return self.f(*args, **kwargs)

    def _uncached_call(self, *args, **kwargs):
        return self.f(*args, **kwargs)


_conditional_cache = _ConditionalLRUCache()


@_conditional_cache
def _get_block_result(block: str) -> _tp.Tuple[str, str]:
    num_100 = int(block[0])
    num_10 = int(block[1])
    num_1 = int(block[2])

    words_100, words_10, words_1 = "", "", ""
    glue_100_to_10, glue_10_to_1, block_glue = "", "", ", "

    if num_100:  # This block has a 100 value
        words_100 = f"{_num_to_words_map[num_100]} hundred"
        if num_10 or num_1:  # ... and this block has either a 10 or a 1 value
            glue_100_to_10 = " and "
    elif num_10 or num_1:  # This block has NO 100 value and has either a 10 or a 1 value
        block_glue = " and "

    if num_10 and num_1:  # There is a 10 and a 1 that need to be joined.
        glue_10_to_1 = "-"

    if num_10 == 1:  # Number is in the teens
        words_teen = _num_to_words_map[num_10*10 + num_1]
        block_result = f"{words_100}{glue_100_to_10}{words_teen}"
    else:  # Number is NOT in the teens
        words_10 = _num_to_words_map[num_10*10]
        words_1 = _num_to_words_map[num_1]
        block_result = f"{words_100}{glue_100_to_10}{words_10}{glue_10_to_1}{words_1}"

    return block_result, block_glue


_num_to_words_map = {
    0: "",
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine",
    10: "ten",
    11: "eleven",
    12: "twelve",
    13: "thirteen",
    14: "fourteen",
    15: "fifteen",
    16: "sixteen",
    17: "seventeen",
    18: "eighteen",
    19: "nineteen",
    20: "twenty",
    30: "thirty",
    40: "forty",
    50: "fify",
    60: "sixty",
    70: "seventy",
    80: "eighty",
    90: "ninety"
}

# num_groups_of_three_zeros : word
_block_num_to_thousands_map = {
    1: "thousand",
    2: "million",
    3: "billion",
    4: "trillion",
    5: "quadrillion",
    6: "quintillion",
    7: "sextillion",
    8: "septillion",
    9: "octillion",
    10: "nonillion",
    11: "decillion",
    12: "undecillion",
    13: "duodecillion",
    14: "tredecillion"
}
