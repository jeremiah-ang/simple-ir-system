'''
PROXIMITY.py

Description: Handles functionality to measure 
proximity of query terms in a particular document
measures the smallest window that contains all query term

'''

import sys
import math
import operator

# Accessors 
def termid (t, i):
    return t[i][0]
def pos (t, i):
    return t[i][1]
def gap (window):
    return window[1]
def length (window):
    return window[0]


def merge_terms (acc, t, tid):
    '''
        merge positions of terms
    '''
    merged = []
    while (acc and t):
        if acc[0][1] < t[0]:
            merged.append(acc.pop(0))
        else:
            merged.append((tid, t.pop(0)))

    merged.extend((acc if acc else [(tid, x) for x in t]))
    return merged

def smallest_window (s, char_hash):
    '''
        Calculate smallest window of s contain all 
        values in char_hash
    '''
    char_length = len(char_hash)
    count = 0

    j = 0
    W = sys.maxint
    P = None
    for i in range(len(s)):
        char_hash[termid(s, i)] += 1
        if char_hash[termid(s, i)] == 1:
            count += 1

        while (count == char_length):
            c_W = pos(s, i) - pos(s, j) + 1
            if c_W < W:
                W = c_W
                P = (pos(s, i), pos(s, j))

            char_hash[termid(s, j)] -= 1
            if char_hash[termid(s, j)] == 0:
                count -= 1
            j += 1

    return float(W), P

def proximity_weight (locations, number_of_terms):
    '''
        Calculate smallest window size for each (document, field)
    '''
    Ws = {}
    min_window = sys.maxint
    for docid in locations:
        acc = []
        for cur_tid in locations[docid]:
            acc = merge_terms(acc, locations[docid][cur_tid], cur_tid)

        window = smallest_window(acc, [0] * number_of_terms)
        min_window = min(length(window), min_window)

        Ws[docid] = window

    return Ws, min_window


def calculate_proximity_score (window, min_window, no_of_terms):
    '''
        The score based on the window size.
    '''
    return no_of_terms/length(window) if gap(window) else 0

def update_score (score, Ws, min_window, no_of_terms):
    '''
        returns a new dictionary with same structure as score 
        but updates the score for each (docid, field)
    '''
    return {docid: score[docid] * calculate_proximity_score(Ws[docid], min_window, no_of_terms) 
                for docid in score}

class Proximity:
    def __init__ (self):

        # Locations -- locations of term of a (docid, field)
        self.locations = {}

    def reset (self):
        self.locations = {}

    def add_location (self, term_pos, docid, locations):
        '''
            Add position index of the current termid for a particular docid and field
        '''
        if docid not in self.locations:
            self.locations[docid] = {}

        self.locations[docid][term_pos] = locations

    def get_exact (self, no_of_terms):
        '''
            For exact phrasal search 
            returns docid who contain the exact phrase
        '''
        docids = []
        Ws, min_window = proximity_weight(self.locations, no_of_terms)
        for docid in Ws:
            window, positions = Ws[docid]
            if window == no_of_terms:
                docids.append(docid)
        return docids

    def calculate_proximity_score (self, score, no_of_terms):
        '''
            Return the window which contains all searched terms
            and updates the document score
        '''
        Ws, min_window = proximity_weight(self.locations, no_of_terms)
        proximity_score = update_score(score, Ws, min_window, no_of_terms)
        return proximity_score

    def prepare_query (self, query):
        return [(idx, term) for idx, term in enumerate(query)]
