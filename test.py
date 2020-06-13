from typing import List, Union
import unittest as ut

import numbers_in_words as niw


class TestModuleAPI(ut.TestCase):
    def setUp(self):
        self.public_members = [m for m in dir(niw) if not m[0] == "_"]
        self.expected_members = [
                        "number_in_words",
                        "number_in_words_from_phrase"]

    def test_expected_public_module_members(self):
        for em in self.expected_members:
            self.assertIn(em, self.public_members, msg=f"Expected to find a '{em}' module member, but didn't.")

    def test_no_unexpected_public_module_members(self):
        other_members = [m for m in self.public_members if m not in self.expected_members]
        self.assertFalse(any(other_members), msg=f"Found unexpected public members in module:\n\t{other_members}")


class TestValueMapComplete(ut.TestCase):
    def test_map_members_complete(self):
        expected_keys = [i for i in range(0, 20)]
        expected_keys += [i*10 for i in range(2, 10)]
        mapped_keys = niw._num_to_words_map.keys()
        outcomes = [ek in mapped_keys for ek in expected_keys]
        self.assertTrue(all(outcomes), msg=outcomes)


class Scenario:
    def __init__(self, input_value: str, expected_value: Union[str, None]):
        self.input_value = input_value
        self.expected_value = expected_value


class TestProvidedTestCases(ut.TestCase):
    def setUp(self):
        self.full_scenarios: List[Scenario] = [
            Scenario(
                "The pump is 536 deep underground.",
                "five hundred and thirty-six"),
            Scenario(
                "We processed 9121 records.",
                "nine thousand, one hundred and twenty-one"),
            Scenario(
                "Variables reported as having a number invalid missing type #65678.",
                "number invalid"),
            Scenario(
                "Interactive and printable 10022 ZIP code.",
                "ten thousand and twenty-two"),
            Scenario(
                "The database has 66723107008 records.",
                "sixty-six billion, seven hundred and twenty-three million, one hundred and seven thousand and eight"),
            Scenario(
                "I received 23 456,9 KGs.",
                "number invalid")]

        self.number_scenarios: List[Scenario] = [
            Scenario("The pump is 536 deep underground.", "536"),
            Scenario("We processed 9121 records.", "9121"),
            Scenario("Variables reported as having a number invalid missing type #65678.", None),
            Scenario("Interactive and printable 10022 ZIP code.", "10022"),
            Scenario("The database has 66723107008 records.", "66723107008"),
            Scenario("I received 23 456,9 KGs.", None)]

    def test_number_extraction(self):
        for scenario in self.number_scenarios:
            outcome = niw._get_number_substring(scenario.input_value)
            self.assertEqual(outcome, scenario.expected_value, msg=f"Output incorrect for '{scenario.input_value}'")

    def test_provided_scenarios(self):
        for scenario in self.full_scenarios:
            outcome = niw.number_in_words_from_phrase(scenario.input_value)
            self.assertEqual(outcome, scenario.expected_value, msg=f"Output incorrect for '{scenario.input_value}'")


if __name__ == "__main__":
    ut.main()
