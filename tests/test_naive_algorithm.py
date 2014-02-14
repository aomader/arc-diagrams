from itertools import product, islice

from pytest import mark

from arc_diagrams.naive_algorithm import *

class TestMaximalMatchingPairs:
    @mark.randomize(s=str, str_attrs=('digits',), max_length=50, ncalls=100)
    def test_identical(self, s):
        for x,y,l in self.generate(s):
            assert s[x:x+l] == s[y:y+l]

    @mark.randomize(s=str, str_attrs=('digits',), max_length=50, ncalls=100)
    def test_nonoverlapping(self, s):
        for x,y,l in self.generate(s):
            assert x + l <= y

    @mark.randomize(s=str, str_attrs=('digits',), max_length=50, ncalls=100)
    def test_consecutive(self, s):
        for x,y,l in self.generate(s):
            assert s.find(s[x:x+l], x + 1, y + l - 1) == -1

    @mark.randomize(s=str, str_attrs=('digits',), max_length=50, ncalls=100)
    def test_maximal(self, s):
        for x,y,l in self.generate(s):
            for i,j in islice(product(range(x + 1), range(y - x - l + 1)), 1,
                              None):
                sub = s[x-i:x+l+j]
                idx = s.find(sub, x-i+1)
                assert idx == -1 or idx > y or idx + j + i < y or idx < x + l + j

    def test_example1(self):
        self.verify('123ab456', [])

    def test_example2(self):
        self.verify('123a123', [(0, 4, 3)])

    def test_example3(self):
        self.verify('10101010', [(0, 2, 2), (4, 6, 2), (1, 3, 2), (3, 5, 2)])

    def test_example4(self):
        self.verify('28746391479735648274639137',
                    [(0, 17, 1), (1, 16, 1), (2, 18, 6), (2, 9, 1), (3, 8, 1),
                     (4, 14, 1), (5, 12, 1), (6, 10, 1), (8, 15, 1), (9, 11, 1),
                     (10, 22, 1), (11, 18, 1), (12, 21, 1), (14, 20, 1),
                     (15, 19, 1), (18, 25, 1), (21, 24, 1)])

    def test_example5(self):
        self.verify('1234567abcde1234567fghij1234567',
                    [(0, 12, 7), (12, 24, 7)])

    def test_example6(self):
        self.verify('abcd111110000011111abcd',
                    [(0, 19, 4), (4, 14, 5), (4, 5, 1), (7, 8, 1), (9, 10, 1),
                     (12, 13, 1), (14, 15, 1), (17, 18, 1)])

    def verify(self, string, expected):
        result = sorted(self.generate(string))
        assert result == sorted(expected)
        self.test_identical(string)
        self.test_nonoverlapping(string)
        self.test_consecutive(string)
        self.test_maximal(string)

    def generate(self, string):
        return maximal_matching_pairs(string)


class TestRepetitionRegions:
    @mark.randomize(s=str, str_attrs=('digits',), max_length=50, ncalls=100)
    def test_successive(self, s):
        for r,n,l in self.generate(s):
            assert (n - r) % l == 0 and n <= len(s)
            assert len(set(s[x:x+l] for x in range(r, n, l))) == 1

    @mark.randomize(s=str, str_attrs=('digits',), max_length=50, ncalls=100)
    def test_minimal(self, s):
        for r,n,l in self.generate(s):
            for d in range(l):
                for l1 in range(l-d, 0, -1):
                    if d == 0 and l1 == l:
                        continue

                    p = s[r+d:r+d+l1]

                    a = r+d
                    while a - l1 >= 0 and s[a-l1:a] == p:
                        a -= l1

                    b = r+d
                    while b + l1 <= len(s) and s[b+l1:b+l1+l1] == p:
                        b += l1

                    assert r < a or n > b

    @mark.randomize(s=str, str_attrs=('digits',), max_length=50, ncalls=100)
    def test_leftmost(self, s):
        for r,n,l in self.generate(s):
            key = s[r-1:r-1+l]
            assert not all(key == s[i:i+l] for i in range(r-1, n-1, l))

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
                    [(0, 5, 1), (5, 8, 1), (7, 13, 3), (8, 10, 1), (11, 14, 1),
                     (14, 16, 1), (17, 19, 1), (21, 25, 1),
                     (25, 28, 1), (27, 33, 3), (28, 30, 1), (31, 34, 1),
                     (34, 37, 1), (36, 40, 2)])

    def verify(self, string, expected):
        result = sorted(self.generate(string))
        assert result == sorted(expected)
        self.test_successive(string)
        self.test_minimal(string)
        self.test_leftmost(string)

    def generate(self, string):
        return repetition_regions(string)


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
