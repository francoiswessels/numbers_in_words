from typing import List, Union, Tuple
import unittest as ut

import numbers_in_words as niw
import numbers_in_words._numbers_in_words_modules.string_processing as sp
import numbers_in_words._numbers_in_words_modules.number_parts as np


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
                "It doesn't get any colder than -273 degrees Kelvin.",
                "negative two hundred and seventy-three"),
            Scenario(
                "I received 23 456,9 KGs.",
                "number invalid"),
            Scenario(
                "There is 0 chance of fell freezing over!",
                "zero")]

        self.number_extraction_cases: List[Tuple[str, np.NumberParts]] = [
            ("The pump is 536 deep underground.", np.NumberParts("536")),
            ("We processed 9121 records.", np.NumberParts("9121")),
            ("Variables reported as having a number invalid missing type #65678.", np.NumberParts()),
            ("Interactive and printable 10022 ZIP code.", np.NumberParts("10022")),
            ("The database has 66723107008 records.", np.NumberParts("66723107008")),
            ("It doesn't get any colder than -273", np.NumberParts("273", negative=True)),
            ("I received 23 456,9 KGs.", np.NumberParts())]

    def test_provided_scenarios(self):
        for scenario in self.full_scenarios:
            outcome = niw.number_in_words_from_phrase(scenario.input_value)
            self.assertEqual(outcome, scenario.expected_value, msg=f"Output incorrect for '{scenario.input_value}'")

    def test_number_extraction(self):
        for case in self.number_extraction_cases:
            outcome = sp._get_number_parts_from_phrase(case[0])
            self.assertEqual(outcome, case[1], msg=f"Output incorrect for '{case[0]}'")


class TestAdditionalTestCases(ut.TestCase):
    def setUp(self):
        self.full_scenarios: List[Scenario] = [
            Scenario(
                "The pump is 536.5m underground.",
                "five hundred and thirty-six point five"),
            Scenario(
                "Is the sun more than 10,000,000.5km away from us?.",
                "ten million point five"
            )]

        self.number_extraction_cases: List[Tuple[str, np.NumberParts]] = [
            ("The car travels at 65.38kph.", np.NumberParts("65", "38", "kph.")),
            ("The rocket travels at 1,965.38kph.", np.NumberParts("1965", "38", "kph.")),
            ("The rocket travels at 19,65.38kph.", np.NumberParts()),
            ("The rocket travels at 1,965.38kph.", np.NumberParts("1965", "38", "kph.")),
            ("Is the sun more than 10,000,000km away from us?.", np.NumberParts("10000000", suffix="km")),
            ("The pump is 536 deep underground.", np.NumberParts("536")),
            ("There is 0 chance of fell freezing over!", np.NumberParts("0"))]

    def test_additional_scenarios(self):
        for scenario in self.full_scenarios:
            outcome = niw.number_in_words_from_phrase(scenario.input_value)
            self.assertEqual(outcome, scenario.expected_value, msg=f"Output incorrect for '{scenario.input_value}'")

    def test_additional_number_extraction(self):
        for case in self.number_extraction_cases:
            outcome = sp._get_number_parts_from_phrase(case[0])
            self.assertEqual(outcome, case[1], msg=f"Output incorrect for '{case[0]}'")


if __name__ == "__main__":
    ut.main()
