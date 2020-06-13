
from typing import List, Dict, Union
import timeit
import numbers_in_words as niw


class Scenario:
    def __init__(self, input_value: str, expected_value: Union[str, None]):
        self.input_value = input_value
        self.expected_value = expected_value


number_scenarios: List[Scenario] = [
    Scenario("The pump is 536 deep underground.", "536"),
    Scenario("We processed 9121 records.", "9121"),
    Scenario("Variables reported as having a number invalid missing type #65678.", None),
    Scenario("Interactive and printable 10022 ZIP code.", "10022"),
    Scenario("The database has 66723107008 records.", "66723107008"),
    Scenario("I received 23 456,9 KGs.", None)]


# for s in number_scenarios:
#     print(s.expected_value, niw.number_in_words_from_phrase(s.input_value))

statement1 = "niw.number_in_words_from_phrase('999', cached=False)"
statement2 = "niw.number_in_words_from_phrase('99999999999999999999', cached=True)"

setup = "import numbers_in_words as niw"

print(timeit.timeit(stmt=statement1, setup=setup, number=100000))
print(timeit.timeit(stmt=statement2, setup=setup, number=100000))
