# -*- coding: utf-8 -*-

import naive_algorithm

from collections import defaultdict
from itertools import product, islice

from suffix_tree import SuffixTree

__all__ = [
    'maximal_matching_pairs',
    'repetition_regions',
    'essential_matching_pairs'
]


def maximal_matching_pairs(tree):
    """
    Find all substring pairs fulfilling the properties specified in
    definition 1, namely _identical_, _non-overlapping_, _consecutive_ and
    _maximal_.

    Args:
        tree (SuffixTree): A suffix tree, build from the string to be searched.

    Returns:
        generator. A generator of tuples, each describing one matching pair as
                   composed of the start of the first and the second substring,
                   as well as the length of the substring.
    """
    s = tree.string
    substrings = defaultdict(set)

    # get all substring starts repeated at least once
    for leaf in tree.leaves:
        node = leaf.parent
        end = leaf.start
        while node is not None and \
              (node.pathLabel not in substrings or end - len(node.pathLabel) \
                      not in substrings[node.pathLabel]) and \
              node.edgeLabel != '':
            for i in range(len(node.pathLabel)):
                substrings[node.pathLabel[:i+1]].add(end - len(node.pathLabel))
            end -= len(node.edgeLabel)
            node = node.parent

    def contained(x, y, l, largers):
        for large in largers:
            starts = substrings[large]
            idx = list(find_all(large, sub))
            for i,j in product(idx, idx):
                if (x - i) + len(large) <= (y - j) and (x - i) in starts and \
                   (y - j) in starts:
                    return True
        return False

    # apply constraints and yield legit pairs
    for sub in sorted(substrings, key=len, reverse=True):
        starts = sorted(substrings[sub])
        l = len(sub)
        cs = [k for k in substrings if len(k) > len(sub) and
              k.startswith(sub) and k.endswith(sub)]

        for x, y in zip(starts, islice(starts, 1, None)):
            # overlapping
            if x + l > y:
                continue

            # non maximal: left and right expansion
            if (x > 0 and x + l < y and s[x-1] == s[y-1]) or \
               (y + l < len(s) and x + l < y and s[x+l] == s[y+l]):
                continue

            # not maximal: inner and outer expansion
            if contained(x, y, l, cs):
                continue

            yield x, y, l


def repetition_regions(tree):
    """
    Find all repetition regions as specified in definition 2 and the following
    further limiting rules:
    
    2.1) _Minimal_: There does not exist any other repetition region R'
         containing R, with the fundamental substring P' containing P.
    2.2) _Leftmost_: There doesn't exist another repetition region R',
         originating from R shifted one character to the left, with equal
         length of the region and of the fundamental substring.

    Args:
        tree (SuffixTree): A suffix tree, build from the string to be searched.

    Returns:
        list. A list of tuples, each describing one repetition region build
              from multiple matching pairs. The tuples contain the start of
              the region, the end of the region not inclusive and the length
              of the fundamental substring, respectively.
    """
    return naive_algorithm.repetition_regions(tree.string)

    s = tree.string
    substrings = defaultdict(set)

    for leaf in tree.leaves:
        node = leaf.parent
        end = leaf.start
        while node is not None and \
              (node.pathLabel not in substrings or end - len(node.pathLabel) \
                      not in substrings[node.pathLabel]) and \
              node.edgeLabel != '':
            for i in range(len(node.pathLabel)):
                substrings[node.pathLabel[:i+1]].add(end - len(node.pathLabel))
            end -= len(node.edgeLabel)
            node = node.parent

    regions = []

    for sub in sorted(substrings, key=len):
        starts = sorted(substrings[sub])
        l = len(sub)

        a = 0
        while a < len(starts) - 1:
            f = starts[a]
            e = f + l
            b = a + 1
            while b < len(starts) and starts[b] - starts[b - 1] == l:
                e += l
                b += 1

            if b - a > 1:
                regions.append((f, e, l))

            a = b

    return regions


def essential_matching_pairs(string):
    """
    Find all essential matching pairs as specified in definition 3. These
    pairs might be used to build arc diagrams from.

    Args:
        string (str): The string to be searched.

    Returns:
        generator. Yields tuples, each describing one matching pair as composed
                   of the start of the first and the second substring, as well
                   as the length of the substring.
    """
    tree = SuffixTree(string)

    regions = repetition_regions(tree)

    # definition 3.1 and 3.2
    for x,y,l in maximal_matching_pairs(tree):
        if not any(x >= r and y + l <= e for r,e,_ in regions) or \
           any(int((x - r)/f) == int((y + l - r - 1)/f) for r,_,f in regions):
            yield x, y, l

    # definition 3.3
    for r,e,l in regions:
        for x in range(r, e - l, l):
            yield x, x + l, l


def children(node):
    """ Returns a generator to iterate all direct node children. """
    c = node.firstChild
    while c is not None:
        yield c
        c = c.next


def find_all(a_str, sub):
    """ Yield all occurences of a substring. """
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += 1

# vim: set expandtab shiftwidth=4 softtabstop=4 textwidth=79:
