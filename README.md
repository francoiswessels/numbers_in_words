# numbers_in_words (a code challenge)

A small module that helps with the output of the value of an integer in words. The package makes two functions available to achieve this, namely 'number_in_words' and 'number_in_words_from_phrase'.

The two functions allow for the optional use of an LRU cache, at the expense of a little bit of additional memory consumption.

The range of numbers that can be expressed is any negative or positive number where the whole number component does not exceed 999,999,999,999,999,999,999,999,999,999,999,999,999,999 (14 groups of three 9's). The decimal component is limited only by your machine's memory.

## Dependencies

This package makes use of _formatted string literals_, or F-strings, which was first introduced in Python 3.6, so that or a higher version is the dependency.

## Usage
```
main.py [-h] [-d] [-f FILE] [-t]

a small app that find some integers and converts their value into words

optional arguments:
  -h, --help            show this help message and exit
  -d, --demo            display a list of result that demonstrates what this
                        package does.
  -f FILE, --file FILE  process the contents of FILE, if it exists.
  -t, --timeit          display the results of some timed runs, to get a sense
                        of what the cached functionality achieves.
```
To get started, try:

```
python3 main.py -f example.txt
```

it should give you:

```
Converting contents of example.txt:

Found  : The pump is 536 deep underground.
Outcome: five hundred and thirty-six

Found  : We processed 9121 records.
Outcome: nine thousand, one hundred and twenty-one

Found  : Variables reported as having a number invalid missing type #65678.
Outcome: number invalid

Found  : Interactive and printable 10022 ZIP code.
Outcome: ten thousand and twenty-two

Found  : The database has 66723107008 records.
Outcome: sixty-six billion, seven hundred and twenty-three million, one hundred and seven thousand and eight

Found  : I received 23 456,9 KGs.
Outcome: number invalid

Found  : It doesn't get any colder than -273 degrees Kelvin.
Outcome: negative two hundred and seventy-three

Found  : There is 0 chance of hell freezing over!
Outcome: zero

Found  : Is the sun more than 10,000,000km away from us?
Outcome: ten million

Found  : South Africa's bank balance is at least ZAR -54,343,234.45!
Outcome: negative fify-four million, three hundred and forty-three thousand, two hundred and thirty-four point four five

```

## Remarks on design

### Dependencies and interface
To start with, the aim was to use only standard Python, and not introduce any third party packages. The package needed to run "out of the box", which it does as long as Python 3.6+ is used.

For ease of use, it was important that the package interface is clean i.e. that to the extent possible only functions and variables that are useful to the user are public in the module object after it has been imported. The outcome of that is as follows:
```
>>> import numbers_in_words as niw
>>> dir(niw)
['__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__path__', '__spec__', '_numbers_in_words_modules', 'number_in_words', 'number_in_words_from_phrase']
>>> 
```

### Assumptions

- Numbers can have both whole number and decimal components.
- Negative numbers are indicated by a "-" prefix.
- Suffixes ("km", "kg", "ikko", etc.) can exist and are treated as arbitrary i.e. we don't get involved with the meaning of "ikko".
- Decimal points are "."
- Thousands separators are "," and are optional. However, if they are present in a string they must be used concistently through the string.
- Only phrases with one number in them will be successfully procesed. If it appears that there is more than one number, an invalid response is returned.

### Algorithm

Two approaches were investigated and the faster one selected and then refined and extended. The difference between the approaches lies in whether the numbers are converted to integers, or not.

To help with the discussion, it is useful to set out how number strings are interpreted in the code. Each string is broken up as follows:

    <integer><decimal_point><decimals><suffix>

The integer component, of course, is expressed in groups of three numbers, while decimals are just listed in order. The suffix is just there to help with the interpretation of numbers in the context you may find them.

It turns out that converting the strings to integers and then working through that integers with ```..., integer // 1000```, ```integer // 100```, ```integer // 10```, followed by subtracting the processed value from the number was more expensive, probably because it ultimately involves converting strings to integers, and then back to strings again. The actual arithmetic may also not be trivial as a proportion of total computation, but I stopped short of completely profiling the code.

It was faster to just keep the strings as strings, and working through them in slices of three digits at a time. Breaking the string up into blocks of three and processing it on that basis had the added benefit that the repeating logic required to do that could be broken out into its own function for testing and caching.

This is a brief description of the approach:

```"The number 1345839345 is being used as an example"```

That number is found and then processed as blocks as follows:

```"001" "345" "839" "345"```

Notice the following:
- The leading zeros, which means that each block is complete and we never need to deal with exceptions, making the block interpretation code simpler and easier to understand.
- There are two blocks with the value "345". Those blocks will have the same result, so the option is provided to cache a result in case another block has the same value, giving a bit of a speedup.

It looks like _formatted string literals_, or F-strings, are faster than ```"".join([...])``` and more readable. I did not explore the use of ```array```, because F-strings are just so easy to use and my gut says that any further speedup would be negligible.

#### Optional Caching

Caching is supported at both the block level and the number string level, but not on the phrase level. Caching is on by default on the block level, but off by default on the number level.

This arrangement was chosen because block values are most likely to repeat themselves, there is only 1000 different block values and a block is a known three characters long. Numbers on the other hand are much more varied and can be much longer. Thus the benefit from caching numbers is much less and the memory consumption much higher.

Nevertheless, the feature is there, even if just to demonstrate a certain understanding of the problem.

### run, maintain, evolve

Some care was taken to ensure that utility functions (pretty much all the _internal ones) are pure functions and that they have a single purpose that is decoupled from other methods as much as possible. This, combined with the user tests, has made the inevitable errors arising from extending the code relatively easy to debug. That being said, the tests can be refined to make it clearer where in the code a problem that is causing a test failure is arising.

The introduction of the NumberParts class has helped to organise the handover of results from functions that interpret strings as they are received from user code to functions that interpret these results. It also offers some validation and comparison logic which makes it useful for implementing unit tests. The need for this decoupling only really arose once the functionality was extended to handle numbers with decimal components and thousands separators. Now that it does exist, the opportunity to attach more functionality to that class is there. Is number_in_words a property of a NumberParts class, or is NumberParts class just a d.t.o? At the moment it's just a d.t.o. and significant restructurig will be required to extend it to take on the number-in-words responsibility.

Those questions aside, the NumberParts class makes the code significantly more maintainable.

### A note on linting:

I have used `--max-line-length=120`, because the shorter lines frustrate me.