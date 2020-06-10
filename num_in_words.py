from math import ceil as _ceil
import typing as _tp



_map_to_words = {
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

_exponents_of_ten = {
    1: "thousand",
    2: "million",
    3: "billion",
    4: "trillion"
}


def _get_number_substring(phrase: str) -> _tp.Union[str, None]:
    # if the first char in the string is a number, we deem it number-like
    maybe_digits = [word for word in phrase.split(" ") if word[0].isdigit()]
    
    # if only one number-like string was found, and it is actually a number,
    # then we have found what we are looking for.
    if len(maybe_digits) == 1 and maybe_digits[0].isdigit():
        return maybe_digits[0]
    
    return None


def number_in_words(number_str: str) -> str:
    if not number_str.isdigit():
        raise ValueError("The string is not a valid number")
    
    num_of_thousands = _ceil(len(number_str)/3)
    num_digits = num_of_thousands*3
    number_str = number_str.zfill(num_digits)
    
    result = ""
    for i in range(num_of_thousands):
        block = number_str[i*3:(i+1)*3]
        
        num_100 = int(block[0])
        num_10 = int(block[1])
        num_1 = int(block[2])
        
        words_100, glue_100_to_10, words_10, glue_10_to_1, words_1 = "", "", "", "", ""
        block_glue = ", "
        if num_100 > 0:
            words_100 = f"{_map_to_words[num_100]} hundred"
            if num_1 > 0 and num_10 > 0:
                glue_100_to_10 = " and "
                glue_10_to_1 = "-"
            elif num_1 > 0 or num_10 > 0:
                glue_100_to_10 = " and "
        elif num_1 > 0 and num_10 > 0:
            glue_10_to_1 = "-"
            block_glue = " and "
        elif num_1 > 0 or num_10 > 0:
            block_glue = " and "

        if num_10 == 1:
            words_teen = f"{_map_to_words[num_10*10 + num_1]}"
            block_result = f"{words_100}{glue_100_to_10}{words_teen}"
        else:
            words_10 = f"{_map_to_words[num_10*10]}"
            words_1 = f"{_map_to_words[num_1]}"
            block_result = f"{words_100}{glue_100_to_10}{words_10}{glue_10_to_1}{words_1}"
        
        if block_result:
            if i == (num_of_thousands - 1):
                if i == 0:  # This condition amounts to a single block number
                    result += block_result
                else:  # The last block, but not the only block
                    result += f"{block_glue}{block_result}"
            elif i == 0: #  The first block, but not the only block
                result += f"{block_result} {_exponents_of_ten[num_of_thousands - i - 1]}"
            else:  # Neither the first, nor the last block
                result += f"{block_glue}{block_result} {_exponents_of_ten[num_of_thousands - i - 1]}"
    
    return result


def number_in_words_from_phrase(phrase: str) -> str:
    number_str = _get_number_substring(phrase)
    if number_str is None:
        return "number invalid"
    
    return number_in_words(number_str)

