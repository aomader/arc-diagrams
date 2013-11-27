# -*- coding: utf-8 -*-

from suffix_tree import SuffixTree

def maximal_matching_pairs(tree):
    """
    Find all substring pairs fulfilling the properties specified in
    definition 1, namely _identical_, _non-overlapping_, _consecutive_ and
    _maximal_.

    Args:
        tree (SuffixTree): A suffix tree, build from the string to be searched.

    Returns:
        list. A list of tuples, each describing one matching pair as composed
              of the start of the first and the second substring, as well as
              the length of the substring.
    """
    return []


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

# vim: set expandtab shiftwidth=4 softtabstop=4 textwidth=79:
