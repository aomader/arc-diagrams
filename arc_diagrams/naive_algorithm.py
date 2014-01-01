# -*- coding: utf-8 -*-

def maximal_matching_pairs(string):
    """
    Find all substring pairs fulfilling the properties specified in
    definition 1, namely _identical_, _non-overlapping_, _consecutive_ and
    _maximal_.

    Args:
        string (str): The string to be searched.

    Returns:
        generator. A generator of tuples, each describing one matching pair as
                   composed of the start of the first and the second substring,
                   as well as the length of the substring.
    """
    n = len(string)
    for x in range(0, n - 1):
        for l in range(int((n - x)/2) + 1, 0, -1):
            c = string[x:x+l]
            y = string.find(c, x + 1)

            # not found or not consecutive
            if y == -1 or y < x + l:
                continue

            # not maximal: left or right expansion
            if (y + l < n and x + l < y and string[x+l] == string[y+l]) or \
               (x - 1 >= 0 and x + l < y and string[x-1] == string[y-1]):
                continue

            # not maximal: inner expansion
            if any(string[x:x+l+i] == string[y-i:y+l]
                   for i in range(1, (y - x - l)/2 + 1)):
                continue

            # not maximal: outer expansion
            if any(string[x-i:x+l] == string[y:y+l+i]
                   for i in range(1, max(x, n - y - l) + 1)):
                continue

            yield x, y, l


def repetition_regions(string):
    """
    Find all repetition regions as specified in definition 2 and the following
    further limiting rules:
    
    2.1) _Minimal_: There do not exist other repetition regions R'
         containing R, with the fundamental substring P' containing P.

    Args:
        string (str): The string to be searched.

    Returns:
        list. A list of tuples, each describing one repetition region build
              from multiple matching pairs. The tuples contain the start of
              the region, the end of the region not inclusive and the length
              of the fundamental substring, respectively.
    """
    n = len(string)
    s = 0
    regions = []
    while s < n - 1:
        for l in range(1, (n - s)/2 + 1):
            candidate = string[s:s+l]

            end = s + l
            while string.find(candidate, end, end + l) == end:
                end += l

            if end != s + l:
                regions.append((s, end, len(candidate)))
                s = end - 1
                break
        s += 1
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
    regions = repetition_regions(string)

    # definition 3.1 and 3.2
    for x,y,l in maximal_matching_pairs(string):
        if not any(x >= r and y + l <= e for r,e,_ in regions) or \
           any(int((x - r)/f) == int((y + l - r - 1)/f) for r,_,f in regions):
            yield (x, y, l)

    # definition 3.3
    for r,e,l in regions:
        for x in range(r, e - l, l):
            yield (x, x + l, l)

# vim: set expandtab shiftwidth=4 softtabstop=4 textwidth=79:
