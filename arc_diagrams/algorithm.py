# -*- coding: utf-8 -*-

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
    string = tree.string
    substrings = defaultdict(set)

    # get all substring starts repeated at least once
    for leaf in tree.leaves:
        node = leaf.parent
        end = leaf.start
        while node is not None and \
              end - len(node.pathLabel) not in substrings[node.pathLabel] and \
              node.edgeLabel != '':
            for i in range(len(node.pathLabel)):
                substrings[node.pathLabel[:i+1]].add(end - len(node.pathLabel))
            end -= len(node.edgeLabel)
            node = node.parent

    def contained(i, j, l, cs):
        for c in cs:
            xs = []
            ys = []

            for s in sorted(substrings[c]):
                if s <= i and s + len(c) >= i + l:
                    xs.append(s)
                if s <= j and s + len(c) >= j + l:
                    ys.append(s)

            for a,b in product(xs, ys):
                if a + len(c) <= b:
                    return True
        return False

    # apply constraints and yield legit pairs
    for sub, starts in substrings.iteritems():
        starts = sorted(starts)
        cs = [k for k in substrings if len(k) > len(sub) and
              k.startswith(sub) and k.endswith(sub)]
        l = len(sub)
        for x, y in zip(starts, islice(starts, 1, None)):
            # overlapping
            if x + l > y:
                continue

            # non maximum: left expansion
            if x > 0 and x + l < y and string[x-1] == string[y-1]:
                continue

            # non maximum: right expansion
            if y + l < len(string) and x + l < y and string[x+l] == string[y+l]:
                continue

            # not maximum: inner/outer expansion
            # TODO: There has to be a better way!
            if contained(x, y, l, cs):
                continue

            yield x, y, l


def repetition_regions(string):
    """
    Find all repetition regions as specified in definition 2 and the following
    further limiting rules:
    
    2.1) _Minimal_: There do not exist other repetition regions R'
         containing R, with the fundamental substring P' containing P.

    Args:
        tree (SuffixTree): A suffix tree, build from the string to be searched.

    Returns:
        list. A list of tuples, each describing one repetition region build
              from multiple matching pairs. The tuples contain the start of
              the region, the end of the region not inclusive and the length
              of the fundamental substring, respectively.
    """
    return []


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
            yield (x, y, l)

    # definition 3.3
    for r,e,l in regions:
        for x in range(r, e - l, l):
            yield (x, x + l, l)


def children(node):
    """ Returns a generator to iterate all direct node children. """
    c = node.firstChild
    while c is not None:
        yield c
        c = c.next

# vim: set expandtab shiftwidth=4 softtabstop=4 textwidth=79:
