#!/usr/bin/python
import re
import nltk
import sys
import getopt

import inputoutput
import vector_space as vs
import time
import heapq
import boolean as bq
import relevance_feedback as rf
import query_parser as qp

'''
python search.py -d dictionary.txt -p postings.txt -q query.txt -o output.txt
python search.py -d dictionary_sample.txt -p postings_sample.txt -q query.txt -o output_sample.txt

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


start = time.time()

N, dictionary, document_length, topTerms = inputoutput.read_dictionary (dictionary_file)
queries = inputoutput.read_query (file_of_queries)
results = []
with open (postings_file) as posting_fd:
    get_posting = inputoutput.make_get_posting(posting_fd, dictionary)
    query_parser = qp.QueryParser(dictionary, document_length, N, topTerms, get_posting)
    for query in queries:
        print query
        query_parser.parse(query)
        # results.append(parse_query (query, get_posting, N, document_length, topTerms))

end = time.time()
print "Time Taken: ", end - start, "s"




