
import timeit


setup = """
from typing import List,Union
import num_in_words as niw

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
            Scenario("I received 23 456,9 KGs.", None)]"""

s1 = """for i in range(1,10000000,1):    
    (niw.number_in_words_from_phrase(str(i)))"""

s2 = """for i in range(1,10000000,1):    
    (niw.number_in_words_from_phrase_2(str(i)))"""


print(timeit.timeit(stmt=s1, setup=setup, number=1))
print(timeit.timeit(stmt=s2, setup=setup, number=1))




    