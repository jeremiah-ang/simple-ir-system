import sys
import math

def merge_terms (acc, t, tid):
    merged = []
    while (acc and t):
        if acc[0][1] < t[0]:
            merged.append(acc.pop(0))
        else:
            merged.append((tid, t.pop(0)))

    merged.extend((acc if acc else [(tid, x) for x in t]))
    return merged

def smallest_window (s, char_hash):
    def termid (t, i):
        return t[i][0]
    def pos (t, i):
        return t[i][1]

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
                P = (i, j)

            char_hash[termid(s, j)] -= 1
            if char_hash[termid(s, j)] == 0:
                count -= 1
            j += 1

    return float(W), P

def proximity_weight (locations, number_of_terms):
    Ws = {}
    min_w = sys.maxint
    print locations
    for docid in locations:
        acc = []
        for cur_tid in locations[docid]:
            acc = merge_terms(acc, locations[docid][cur_tid], cur_tid)

        W, pos = smallest_window(acc, [0] * number_of_terms)
        Ws[docid] = (W, pos)
        min_w = min(W, min_w)

    return {docid: (min_w / Ws[docid][0] if Ws[docid][1] else 0) for docid in Ws}

def update_score (score, Ws):
    for docid in score:
        score[docid] *= Ws[docid]