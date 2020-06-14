# numbers_in_words (a code challenge)

A small module that helps with the output of the value of an integer in words. The package makes two functions available to achieve this, namely 'number_in_words' and 'number_in_words_from_phrase'.

The two functions allow for the optional use of an LRU cached, at the expense of a little bit of additional memory consumption.

The range of numbers that can be expressed is negative to positive 999999999999999999999999999999999999999999 (14 groups of three 9's).

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

```

## Remarks on design

### Dependencies and interface
To start with, the aim was to use only standard Python, and not introduce any third party packages. The package needed to run out "out of the box", which it does as long as Python 3.6+ is used.

It is was important to me that the package interface is clean i.e. that only functions and variables that are useful to the user are public in the module object after it has been imported. The outcome of that is as follows:
```
>>> import numbers_in_words as niw
>>> dir(niw)
['__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__path__', '__spec__', '_conditional_cache', '_string_processing', 'number_in_words', 'number_in_words_from_phrase']
>>> 
```

### Algorithm

Broadly, two approaches were investigated and the faster one selected and then refined a little bit. The difference between the approaches lies in whether the numbers are converted to integers, or not.

It turns out that converting the strings to integers and then working my way through that string with ..., ```integer // 1000```, ```integer // 100```, ```integer // 10```, followed by subtracting the processed value from the number was simply expensive, probably because ultimately it involves converting strings to integers, and then back to strings again. The actualy arithmetic may also not be trivial in, but I stopped short of completely profiling the code.

It was faster to just keep the strings as strings, and working them in slices of three digits at a time. Breaking the string up into blocks of three and proceessing it on that basis had the added benefit that the repeating logic required to do that could be broken out into its own function for testing and caching.

This is a brief description of the approach:

```"The number 1345839345 is being used as an example"```

That number is found and then processed as blocks as follows:

```"001" "345" "839" "345"```

Notice the following:
- The leading zeros, which means that each block is complete and we never need to deal with exceptions.
- There two blocks with the value "345". Those blocks will have the same result, so the option is provided to cache a result in case another block has the same value, giving a bit of a speedup.

It looks like _formatted string literals_, or F-strings, are faster than ```"".join([...])``` and more readable. I did not explore the use of ```array```, because F-strings are just so easy to use and my gut says that any further speedup would be negligible.

#### Optional Caching

I've made caching optional because it gives me the opportunity to demonstrate the use of a custom _decorator class_. This is certainly more complex than it perhaps needs to be, but I thought it was a little bit clever.

If it wasn't for the want to demonstrate this, I would make the caching a permament feature, not least because it seems to always result in faster run times.

#### To investigate

Why does the runtime decrease when caching is switched on even for the "99" example, which would not result in the cache being used?

### A note on linting:

I have used `--max-line-length=120`, because the shorter lines frustrate me.