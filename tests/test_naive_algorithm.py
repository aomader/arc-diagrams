from itertools import product, islice

from pytest import mark

from arc_diagrams.naive_algorithm import *

class TestMaximalMatchingPairs:
    @mark.randomize(s=str, str_attrs=('digits',), max_length=50, ncalls=100)
    def test_identical(self, s):
        for x,y,l in maximal_matching_pairs(s):
            assert s[x:x+l] == s[y:y+l]

    @mark.randomize(s=str, str_attrs=('digits',), max_length=50, ncalls=100)
    def test_nonoverlapping(self, s):
        for x,y,l in maximal_matching_pairs(s):
            assert x + l <= y

    @mark.randomize(s=str, str_attrs=('digits',), max_length=50, ncalls=100)
    def test_consecutive(self, s):
        for x,y,l in maximal_matching_pairs(s):
            assert s.find(s[x:x+l], x+1, y) == -1

    @mark.randomize(s=str, str_attrs=('digits',), max_length=50, ncalls=100)
    def test_maximal(self, s):
        n = len(s)
        for x,y,l in maximal_matching_pairs(s):
            for i,j in islice(product(range(x + 1), range(y - x - l + 1)), 1, None):
                sub = s[x-i:x+l+j]
                idx = s.find(sub, x+l+j)
                assert idx == -1 or idx > y or idx + l + i + j < y + l

    def test_example1(self):
        self.verify('123ab456', [])

    def test_example2(self):
        self.verify('123a123', [(0, 4, 3)])

    def test_example2(self):
        self.verify('10101010', [(0, 4, 4), (0, 2, 2), (4, 6, 2), (1, 3, 2),
                                 (3, 5, 2)])

    def test_example3(self):
        self.verify('28746391479735648274639137',
                    [(0, 17, 1), (1, 16, 1), (2, 18, 6), (2, 9, 1), (3, 8, 1),
                     (4, 14, 1), (5, 12, 1), (6, 10, 1), (8, 15, 1), (9, 11, 1),
                     (10, 22, 1), (11, 18, 1), (12, 21, 1), (14, 20, 1),
                     (15, 19, 1), (18, 25, 1), (21, 24, 1)])

    def test_example4(self):
        self.verify('1234567abcde1234567fghij1234567',
                    [(0, 12, 7), (12, 24, 7)])

    def test_example5(self):
        self.verify('abcd111110000011111abcd',
                    [(0, 19, 4), (4, 14, 5), (4, 6, 2), (4, 5, 1), (7, 8, 1),
                     (5, 7, 2), (9, 11, 2), (9, 10, 1), (12, 13, 1),
                     (10, 12, 2), (14, 16, 2), (15, 17, 2), (14, 15, 1),
                     (17, 18, 1)])

    def verify(self, string, expected):
        result = sorted(list(maximal_matching_pairs(string)))
        assert result == sorted(expected)


class TestRepetitionRegions:
    @mark.randomize(s=str, str_attrs=('digits',), max_length=50, ncalls=100)
    def test_successive(self, s):
        for r,n,l in repetition_regions(s):
            assert (n - r) % l == 0 and n <= len(s)
            assert len(set(s[x:x+l] for x in range(r, n, l))) == 1

    @mark.randomize(s=str, str_attrs=('digits',), max_length=50, ncalls=100)
    def test_minimal(self, s):
        for r,n,l in repetition_regions(s):
            assert (n - r) % l == 0 and n <= len(s)
            assert len(set(s[x:x+l] for x in range(r, n, l))) == 1

    def test_example1(self):
        self.verify('ABC010101', [(3, 9, 2)])

    def test_example2(self):
        self.verify('28746391479735648274639137', [])

    def test_example3(self):
        self.verify('1010101010101010', [(0, 16, 2)])

    def test_exampel4(self):
        self.verify('abcd111110000011111abcd',
                    [(4, 9, 1), (9, 14, 1), (14, 19, 1)])

    def test_example5(self):
        self.verify('11111000110111001001011110001101110001010',
                    [(0, 5, 1), (5, 8, 1), (8, 10, 1), (11, 14, 1),
                     (14, 16, 1), (17, 19, 1), (21, 25, 1),
                     (25, 28, 1), (28, 30, 1), (31, 34, 1),
                     (34, 37, 1)])

    def verify(self, string, expected):
        result = sorted(repetition_regions(string))
        assert result == sorted(expected)


class TestEssentialMatchingPairs:
    def test_example1(self):
        self.verify('123ab456', [])

    def test_example2(self):
        self.verify('10101010', [(0, 2, 2), (2, 4, 2), (4, 6, 2)])

    def test_example3(self):
        self.verify('abcd111110000011111abcd',
                    [(0, 19, 4), (4, 14, 5), (4, 5, 1), (5, 6, 1), (6, 7, 1),
                     (7, 8, 1), (9, 10, 1), (10, 11, 1), (11, 12, 1),
                     (12, 13, 1), (14, 15, 1), (15, 16, 1), (16, 17, 1),
                     (17, 18, 1)])

    def verify(self, string, expected):
        result = sorted(list(essential_matching_pairs(string)))
        assert result == sorted(expected)

# vim: set expandtab shiftwidth=4 softtabstop=4 textwidth=79:
