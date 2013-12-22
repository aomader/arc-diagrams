# arc-diagrams

A Python powered implementation of [arc diagrams], a visualization method
proposed by Martin Wattenberg, that is capable of representing complex patterns
of repetition in string data. It's not using the exact specification due to
some problems with these, which I explain in a more detailed fashion in the
chapter titled _Mistakes_ found below.

![snapshot of the GUI](http://reaktor42.de/~b52/public/arc-diagrams.png)

## Requirements

The software has been run and tested with the following versions. It might work
with older or newer ones, but we can't say that for sure.

* Python >= 2.7
* PyQt4 == 4.10.3
* [suffix_tree] == 2.1

## Installation

In order to install the software, you have to ensure that you got a proper
version of Python and PyQt4 installed. If that is ensured you install the
package by running the following command:

    # python setup.py install

Once you installed the software you can simply startup the GUI by running
`arc-diagrams`.

## Tests

If you are eager and want to run the tests you can do so by executing the
`setup.py`'s test command. That might also install `pytest` and
`pytest-quickcheck`, since these packages are required in order to run the
tests.

    # python setup.py test

## Mistakes

During the development I encountered a few mistakes within the examples and
definitions given by Wattenberg in his [paper](docs/arc-diagrams.pdf). Using
the original definition I wasn't able to reproduce the examples images
shown in the paper.

### Page 2: Second example of Definition 1 ("10101010")

The author states, that the string "10101010" contains only one maximal
matching pair, namely the substring "1010" located at index 0 and 4.
That is incorrect, since this particular pair is _not_ a maximal matching one
due to definition 1.3: There exists an identical substring lying at index 2
between the beginning of the first and the beginning of the second substring.

It's also incorrect to say, that there is only one maximal matching
pair. By looking at the specification we can find four pairs satisfying all
properties:

Substring | Index First | Index Second
--- | --- | ---
"10" | 0 | 2
"10" | 4 | 6
"01" | 1 | 3
"01" | 3 | 5

Although the substring "1010" at index 0 and 4 is not a maximal matching pair,
it effectively blocks the definition of substring "10" at index 2 and 4 being
a maximal matching pair. That's because of the maximality property
(definition 1.4), which doesn't specify that the superior subsequences have to
be _consecutive_.

That leads to two conclusions: Either the property _consecutive_ is incorrectly
specified and it should instead be limited to an exclusive area:

> 1.3: _Consecutive_: _X_ occurs before _Y_, and there is no substring Z,
> identical to X and Y, **whose beginning is located after the end of X and
> its ending is located before the beginning of Y.**

Or the _maximality_ property should include the _consecutive_ property:

> 1.4: _Maximal_: There do not exist longer identical non-overlapping
> **consecutive** subsequences _X'_ and _Y'_ with _X'_ containing _X_ and
> _Y'_ containing **_Y_**.

One has to note, that both adaptations lead to different results and it's not
clear which one is superior (the adapted parts are marked bold).

### Page 2: Definition 2 and Definition 3.3

The definition of a _repetition region_ is problematic in combination with the
definition 3.3 of a _essential matching pair_. The definition 3.3 basically
lifts all successive pairs of fundamental substrings with a repetition region
into the class of _essential matching pairs_. That by itself is not a problem,
but once we look at the definition 2 for a _repetition region_ one might see
that it misses some sort of _minimality_ property, because the definition
basically says that _all_ substrings repeated two or more times in immediate
succession define a repetition region.

Looking again at the string "10101010" one might see a lot of repetition
regions and each successive pair within in each region is going to be an
_essential matching pair_. But that obviously doesn't make any sense and we can
also approve that by looking at the example images shown in the paper.
Therefore the author implicitly used some sort of _minimality_ property, but
didn't mention it in the specification.

It's also not clear how repetition regions are handled that are somewhat equal
but off by a small amount. For example the string "01010" would contain two
region, "01" repeated 2 times starting at 0 and "10" also repeated 2 times
starting at index 1. Nevertheless it doesn't make any sense to use both,
describe nearly the same repeating area with nearly the same _fundamental
substring_.

So you see there are at least two more properties missing, which further
define a _repetition region_.

[arc diagrams]: http://innovis.cpsc.ucalgary.ca/innovis/uploads/Courses/InformationVisualizationDetails2009/Wattenberg2002.pdf
[suffix_tree]: http://cs.au.dk/~mailund/suffix_tree.html
