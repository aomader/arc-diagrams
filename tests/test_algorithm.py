from itertools import product, islice

from pytest import mark
from suffix_tree import SuffixTree

from arc_diagrams.algorithm import *

import test_naive_algorithm


class TestMaximalMatchingPairs(test_naive_algorithm.TestMaximalMatchingPairs):
    def verify(self, string, expected):
        result = sorted(maximal_matching_pairs(SuffixTree(string)))
        assert result == sorted(expected)


class TestRepetitionRegions(test_naive_algorithm.TestRepetitionRegions):
    def verify(self, string, expected):
        result = sorted(repetition_regions(SuffixTree(string)))
        assert result == sorted(expected)


class TestEssentialMatchingPairs(test_naive_algorithm.TestEssentialMatchingPairs):
    pass

# vim: set expandtab shiftwidth=4 softtabstop=4 textwidth=79:
