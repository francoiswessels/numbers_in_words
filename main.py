import argparse as ap
from typing import List
import timeit

import numbers_in_words as niw


def demo():
    test_cases: List[str] = [
        "The pump is 536.5m deep underground.",
        "We processed 9121 records.",
        "Variables reported as having a number invalid missing type #65678.",
        "Interactive and printable 10022 ZIP code.",
        "The database has 66723107008 records.",
        "I received 23 456,9 KGs.",
        "It doesn't get any colder than -273 degrees Kelvin.",
        "There is 0 chance of hell freezing over!",
        "Is the sun more than 10,000,000km away from us?",
        "South Africa's bank balance is at least ZAR -54,343,234.45!"
        ]

    print("These are the results of some test cases:\n")
    for tc in test_cases:
        print(tc, "\n>> ", niw.number_in_words_from_phrase(tc))
        print("")


def run_file(file_name):
    print(f"Converting contents of {file_name}:\n")

    with open(file_name, "r") as fread:
        for line in fread:
            print(f"Found  : {line}", end="")
            print(f"Outcome: {niw.number_in_words_from_phrase(line)}\n")


def time():
    setup = "import numbers_in_words as niw"

    statement1 = "niw.number_in_words_from_phrase('99', cached_blocks=False)"
    statement2 = "niw.number_in_words_from_phrase('99')"
    statement3 = "niw.number_in_words_from_phrase('99', cached_numbers=True)"
    statement4 = "niw.number_in_words_from_phrase('99999999999999999999', cached_blocks=False)"
    statement5 = "niw.number_in_words_from_phrase('99999999999999999999')"
    statement6 = "niw.number_in_words_from_phrase('99999999999999999999', cached_numbers=False)"

    t1 = round(timeit.timeit(stmt=statement1, setup=setup, number=100000), 5)
    print(f"Convert 99 to words, without caching, 100 000 times                                 : {t1}s")
    t2 = round(timeit.timeit(stmt=statement2, setup=setup, number=100000), 5)
    print(f"Convert 99 to words, with block caching, 100 000 times                              : {t2}s")
    t3 = round(timeit.timeit(stmt=statement3, setup=setup, number=100000), 5)
    print(f"Convert 99 to words, with block and number caching, 100 000 times                   : {t3}s")

    t4 = round(timeit.timeit(stmt=statement4, setup=setup, number=100000), 5)
    print(f"Convert 99999999999999999999 to words, without caching, 100 000 times               : {t4}s")
    t5 = round(timeit.timeit(stmt=statement5, setup=setup, number=100000), 5)
    print(f"Convert 99999999999999999999 to words, with block caching, 100 000 times            : {t5}s")
    t6 = round(timeit.timeit(stmt=statement6, setup=setup, number=100000), 5)
    print(f"Convert 99999999999999999999 to words, with block and number caching, 100 000 times : {t6}s")


if __name__ == "__main__":
    file = ""
    parser = ap.ArgumentParser(
        description="a small app that find some integers and converts their value into words")

    parser.add_argument(
        "-d", "--demo",
        action="store_true",
        help="display a list of result that demonstrates what this package does.")

    parser.add_argument(
        "-f", "--file",
        type=str,
        help="process the contents of FILE, if it exists.")

    parser.add_argument(
        "-t", "--timeit",
        action="store_true",
        help="display the results of some timed runs, to get a sense of what the cached functionality achieves.")

    args = parser.parse_args()

    if args.demo:
        demo()

    if args.file:
        run_file(args.file)

    if args.timeit:
        time()
