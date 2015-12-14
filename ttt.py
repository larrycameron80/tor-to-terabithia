#!/usr/bin/env python3

from collections import namedtuple
import csv

WordList = namedtuple("WordList", ['nouns', 'verbs', 'conjunctions', 'others'])

def load_wordlist(filename):
    wordlist = WordList([], [], [], []) # A totally empty list.
    with open(filename) as wordlist_file:
        for line in wordlist_file:
            # Check that the line is valid; if not, skip it.
            split_line = line.strip('\n').split(',')
            if len(split_line) != 2:
                continue
            else:
                # Line was valid; get the part of speech and put it in the right bin
                if split_line[1] == 'n':
                    wordlist.nouns.append(split_line[0])
                elif split_line[1] == 'v':
                    wordlist.verbs.append(split_line[0])
                elif split_line[1] == 'c':
                    wordlist.conjunctions.append(split_line[0])
                else:
                    wordlist.others.append(split_line[0])
    return wordlist


