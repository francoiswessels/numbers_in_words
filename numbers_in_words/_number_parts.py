"""Help on package _number_parts:

NAME
    _number_parts

DESCRIPTION
    A private module belonging to numbers_in_words package.

AUTHOR:
    Francois Wessels
    https://github.com/francoiswessels/numbers_in_words
"""

from typing import Optional, Union


class NumberParts:
    def __init__(
            self,
            integer: str = "",
            decimals: str = "",
            suffix: str = "",
            negative: bool = False):

        self.negative = negative
        self.integer = integer
        self.decimals = decimals
        self.suffix = suffix

    @property
    def is_valid(self) -> bool:
        return True if self.integer else False
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, NumberParts):
            return False
        return self.integer == other.integer and self.decimals == other.decimals \
            and self.suffix == other.suffix and self.negative == other.negative

    def __repr__(self):
        neg = "-" if self.negative else ""
        return f"<NumberParts negative={neg} integer={self.integer} decimals={self.decimals} suffix={self.suffix}/>"
