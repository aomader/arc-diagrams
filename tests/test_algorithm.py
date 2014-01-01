from suffix_tree import SuffixTree

from arc_diagrams.algorithm import *

import test_naive_algorithm


class TestMaximalMatchingPairs(test_naive_algorithm.TestMaximalMatchingPairs):
    def generate(self, string):
        return maximal_matching_pairs(SuffixTree(string))


class TestRepetitionRegions(test_naive_algorithm.TestRepetitionRegions):
    def generate(self, string):
        return repetition_regions(SuffixTree(string))


class TestEssentialMatchingPairs(test_naive_algorithm.TestEssentialMatchingPairs):
    def verify(self, string, expected):
        result = sorted(list(essential_matching_pairs(string)))
        assert result == sorted(expected)

# vim: set expandtab shiftwidth=4 softtabstop=4 textwidth=79:
