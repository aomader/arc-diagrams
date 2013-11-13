# -*- coding: utf-8 -*-

# definition 1
def maximal_matching_pairs(string):
    n = len(string)
    s = 0
    candidates = []
    while s < n - 1:
        for l in range((n - s)/2 + 1, 0, -1):
            candidate = string[s:s+l]

            idx = string.find(candidate, s + l)
            if idx != -1 and string.find(candidate, s + 1) == idx:
                candidates.append((candidate, s, idx))
        s += 1

    for candidate in candidates:
        #if any(sub != candidate[0] and sub.find(candidate[0]) != -1
        #        for sub,x,y in candidates):
        if any(sub != candidate[0] and sub.find(candidate[0]) != -1 and
                candidate[1] >= x and candidate[1] <= x + len(sub) -
                len(candidate[0]) and candidate[2] >= y and
                candidate[2] <= y + len(sub) - len(candidate[0])
                for sub,x,y in candidates):
            continue
        yield (candidate[1], candidate[2], len(candidate[0]))

# definition 2
def repetition_regions(string):
    n = len(string)
    s = 0
    while s < n - 1:
        for l in range(1, (n - s)/2 + 1):
            candidate = string[s:s+l]

            end = s + l
            while string.find(candidate, end, end + l) == end:
                end += l

            if end != s + l:
                yield (s, end, len(candidate))
                s = end - 1
                break
        s += 1

# definition 3
def essential_matching_pairs(string):
    regions = list(repetition_regions(string))
    max_pairs = list(maximal_matching_pairs(string))

    print('rep regions %s' % regions)

    # definition 3.1
    for x,y,l in max_pairs:
        right = y + l
        #if any(x >= s and x + len(sub) <= e for _,s,e in regions) or \
        #   any(y >= s and y + len(sub) <= e for _,s,e in regions):
        if any(x >= s and y + l <= e for _,s,e in regions):
            continue
        yield (x, y, l)

    # definition 3.2
    # TODO: thats still missing

    # definition 3.3
    for start, end, l in regions:
        for arc_start in range(start, end - l, l):
            yield (arc_start, arc_start + l, l)

# vim: set expandtab shiftwidth=4 softtabstop=4 textwidth=79:
