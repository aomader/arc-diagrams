from unittest import TestCase

from naive_algorithm import maximal_matching_pairs, repetition_regions, \
                            essential_matching_pairs

class TestMaximalMatchingPairs(TestCase):
    def test_definition_exampe1(self):
        self.verify('123a123', [(0, 4, 3)])

    def test_definition_exampe2(self):
        self.verify('10101010', [(0, 4, 4)])

    def verify(self, string, expected):
        result = sorted(maximal_matching_pairs(string))
        self.assertEqual(result, sorted(expected))


class TestRepetitionRegions(TestCase):
    def test_definition_exampe(self):
        self.verify('ABC010101', [(3, 9, 2)])

    def test_figure1(self):
        self.verify('28746391479735648274639137', [])

    def test_figure2(self):
        self.verify('1234567abcde1234567fghij1234567', [])

    def test_figure3(self):
        self.verify('1010101010101010', [(0, 16, 2)])

    def test_figure4(self):
        self.verify('abcd111110000011111abcd',
                    [(4, 9, 1), (9, 14, 1), (14, 19, 1)])

    def test_figure5(self):
        self.verify('11111000110111001001011110001101110001010',
                    [(0, 5, 1), (5, 8, 1), (8, 10, 1), (11, 14, 1),
                     (14, 16, 1), (17, 19, 1), (21, 25, 1),
                     (25, 28, 1), (28, 30, 1), (31, 34, 1),
                     (34, 37, 1)])

    def verify(self, string, expected):
        result = sorted(repetition_regions(string))
        self.assertEqual(result, sorted(expected))

