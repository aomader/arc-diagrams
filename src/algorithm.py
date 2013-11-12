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

#find_substrings('assdf43454asdf3465asdasdf324asdfz')

# vim: set expandtab shiftwidth=4 softtabstop=4 textwidth=79:
