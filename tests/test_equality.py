from pytest import mark
from suffix_tree import SuffixTree

import arc_diagrams.algorithm
import arc_diagrams.naive_algorithm


class TestAlgorithmResults:
    @mark.randomize(s=str, str_attrs=('digits',), max_length=50, ncalls=100)
    def test_maximal_matching_pairs(self, s):
        a = arc_diagrams.algorithm.maximal_matching_pairs(SuffixTree(s))
        b = arc_diagrams.naive_algorithm.maximal_matching_pairs(s)
        assert sorted(a) == sorted(b)

    @mark.randomize(s=str, str_attrs=('digits',), max_length=50, ncalls=100)
    def test_repetition_regions(self, s):
        a = arc_diagrams.algorithm.repetition_regions(SuffixTree(s))
        b = arc_diagrams.naive_algorithm.repetition_regions(s)
        assert sorted(a) == sorted(b)

    @mark.randomize(s=str, str_attrs=('digits',), max_length=50, ncalls=100)
    def test_essential_matching_pairs(self, s):
        a = arc_diagrams.algorithm.essential_matching_pairs(s)
        b = arc_diagrams.naive_algorithm.essential_matching_pairs(s)
        assert sorted(a) == sorted(b)

# vim: set expandtab shiftwidth=4 softtabstop=4 textwidth=79:
