# -*- coding: utf-8 -*-

from suffix_tree import *

def find_substrings(string, min_length=3):
    retVal = []
    gst = GeneralisedSuffixTree([string])

    for shared in gst.sharedSubstrings(min_length):
        subString = []
        subIndex = []
        subString = string[shared[0][1]:shared[0][2]]
        for seq, start, stop in shared:
            subIndex.append(start)
        subIndex.sort()
        retVal.append((subString, subIndex))
    return retVal

def node_children(node):
    child = node.firstChild
    while child is not None:
        yield child
        child = child.next

def repetition_regions(st):
    def test_node(sub, node):
        child = node.firstChild
        while child is not None:
            if child.edgeLabel.startswith(sub):
                return test_node(sub, child)
            child = child.next
        return node

    for node in st.innerNodes:
        if node.edgeLabel == '':
            continue

        last_rep = test_node(node.pathLabel, node)

        if last_rep != node:
            depth = len(last_rep.parent.pathLabel)
            for end in ([last_rep] if last_rep.isLeaf else
                    node_children(last_rep)):
                right = end.edgeLabel.find(node.pathLabel)
                start = end.start - depth
                stop = end.start + (0 if right == -1 else right + len(node.pathLabel))
                yield (node.pathLabel, start, stop)

# definition 1
def naive_maximal_matching_pairs(string):
    n = len(string)
    s = 0
    candidates = []
    while s < n - 1:
        for l in range((n - s)/2 + 1, 0, -1):
            candidate = string[s:s+l]

            idx = string.find(candidate, s + l)
            if idx != -1:
                candidates.append((candidate, s, idx))
                break
        s += 1

    for candidate in candidates:
        if any(sub != candidate[0] and sub.find(candidate[0]) != -1 and
                candidate[1] >= x and candidate[1] <= x + len(sub) -
                len(candidate[0]) and candidate[2] >= y and
                candidate[2] <= y + len(sub) - len(candidate[0])
                for sub,x,y in candidates):
            continue
        yield candidate

# definition 2
def naive_repetition_regions(string):
    n = len(string)
    s = 0
    while s < n - 1:
        for l in range(1, (n - s)/2 + 1):
            candidate = string[s:s+l]

            end = s + l
            while string.find(candidate, end, end + l) == end:
                end += l

            if end != s + l:
                yield (candidate, s, end)
                s = end - 1
                break
        s += 1

# definition 3
def naive_essential_matching_pairs(string):
    regions = list(naive_repetition_regions(string))
    max_pairs = list(naive_maximal_matching_pairs(string))

    # definition 3.1
    for sub,x,y in max_pairs:
        right = y + len(sub)
        if any(x >= s and right <= e for _,s,e in regions):
            continue
        yield (x, y, len(sub))

    # definition 3.2
    # TODO: thats still missing

    # definition 3.3
    for sub, start, end in regions:
        width = len(sub)
        for arc_start in range(start, end - width, width):
            yield (arc_start, arc_start + width, width)

    

def arc_pairs(string):
    return naive_essential_matching_pairs(unicode(string))

# vim: set expandtab shiftwidth=4 softtabstop=4 textwidth=79:
