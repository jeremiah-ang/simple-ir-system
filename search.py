#!/usr/bin/python
import re
import nltk
import sys
import getopt

import inputoutput
import proximity
import vector_space as vs
import heapq
import itertools

'''
python search.py -d dictionary.txt -p postings.txt -q query.txt -o output.txt

'''
def usage():
    print "usage: " + sys.argv[0] + " -d dictionary-file -p postings-file -q file-of-queries -o output-file-of-results"

dictionary_file = postings_file = file_of_queries = output_file_of_results = None
posting_fd = None
DEBUG = False

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'd:p:q:o:')
    except getopt.GetoptError, err:
        usage()
        sys.exit(2)

    for o, a in opts:
        if o == '-d':
            dictionary_file  = a
        elif o == '-p':
            postings_file = a
        elif o == '-q':
            file_of_queries = a
        elif o == '-o':
            file_of_output = a
        else:
            assert False, "unhandled option"

    if dictionary_file == None or postings_file == None or file_of_queries == None or file_of_output == None :
        usage()
        sys.exit(2)



PROXIMITY = True

def add_location (locations, docid, tid, posting):
    if docid not in locations:
        locations[docid] = {}
    locations[docid][tid] = posting

def add_score (score, docid, tf, idf):
    if docid not in score:
        score[docid] = 0
    score[docid] += vs.score(tf, idf)

def update_score (score, step_score, weight=1):
    for docid in step_score:
        if docid not in score:
            score[docid] = 0
        score[docid] = max(score[docid], weight * step_score[docid])


def parse_query (query, get_posting, N, document_length):
    score = {}
    length = len(query)
    weight = 1
    while len(score) < 10 and length > 0:
        query_step = list(itertools.combinations(query, length))
        for smaller_query in query_step:
            step_score = process_query(smaller_query, get_posting, N, document_length)
            print smaller_query, step_score
            update_score (score, step_score, weight)

        length -= 1
        weight /= 2.0

    results = []
    for key in score:
        if score[key] > 0:
            heapq.heappush(results, (-score[key], key))
    return results

def process_query (query, get_posting, N, document_length):
    locations = {}
    score = {}

    # tid to give term unique identifier
    tid = 0 
    print query
    for term in query:

        doc_postings = get_posting(term)
        if not doc_postings:
            continue

        df = len(doc_postings)
        # Inverse Document Frequency
        idf = vs.idf(N, df)

        print idf
        if (idf < 0.2):
            continue

        for doc_posting in doc_postings:
            docid, posting = doc_posting

            # Term Frequency
            tf = len(posting)

            # Store term location in a document
            add_location(locations, docid, tid, posting)

            # Store score of a document
            add_score(score, docid, tf, idf)


        tid += 1
    

    vs.normalise_score(score, document_length)
    
    if (PROXIMITY):
        Ws = proximity.proximity_weight(locations, tid)
        proximity.update_score(score, Ws)

    nonzero_score = {docid: value for docid, value in score.iteritems() if value > 0}

    return nonzero_score


N, dictionary, document_length = inputoutput.read_dictionary (dictionary_file)
queries = inputoutput.read_query (file_of_queries)
results = []
with open (postings_file) as posting_fd:
    get_posting = inputoutput.make_get_posting(posting_fd, dictionary)
    for query in queries:
        # results.append(process_query(query, get_posting, N, document_length))
        results.append(parse_query (query, get_posting, N, document_length))

q = 0
for result in results:
    i = 0   
    print "=" * 10, q, "=" * 10
    q += 1
    while (result and i < 10):
        print '\t', heapq.heappop(result), '\n'
        i += 1



