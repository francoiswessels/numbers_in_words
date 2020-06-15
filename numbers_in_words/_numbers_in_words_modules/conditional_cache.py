"""Help on module conditional_cache:

NAME
    conditional_cache

DESCRIPTION
    A private module belonging to numbers_in_words package.

AUTHOR:
    Francois Wessels
    https://github.com/francoiswessels/numbers_in_words
"""

from functools import lru_cache


class ConditionalLRUCache:
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

    @lru_cache(maxsize=1000)
    def _cached_call(self, *args, **kwargs):
        return self.f(*args, **kwargs)

    def _uncached_call(self, *args, **kwargs):
        return self.f(*args, **kwargs)
