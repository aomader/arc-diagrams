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

def arc_pairs(string):
    suffix_tree = SuffixTree(unicode(string))

    for sub, start, end in repetition_regions(suffix_tree):
        width = len(sub)
        for arc_start in range(start, end - width, width):
            yield (arc_start, arc_start + width, width)

# vim: set expandtab shiftwidth=4 softtabstop=4 textwidth=79:
