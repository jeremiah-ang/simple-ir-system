#!/usr/bin/python
import re
import nltk
import sys
import getopt

from os import listdir, path
import math
from random import randint

import inputoutput

'''
python index.py -i queries/basic/data -d queries/basic/dictionary.txt -p queries/basic/postings.txt
python index.py -i /Users/jeremiahang/nltk_data/corpora/reuters/training -d queries/forum/dictionary.txt -p queries/forum/postings.txt


python index.py -i data -d dictionary.txt -p postings.txt
python index.py -i /Users/jeremiahang/nltk_data/corpora/reuters/training -d dictionary.txt -p postings.txt

'''

def usage():
    print "usage: " + sys.argv[0] + " -i directory-of-documents -d dictionary-file -p postings-file [-x]"

input_directory = output_file_dictionary = output_file_postings = None
phrasal_queries = False

try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:d:p:x')
except getopt.GetoptError, err:
    usage()
    sys.exit(2)
    
for o, a in opts:
    if o == '-i': # input directory
        input_directory = a
    elif o == '-d': # dictionary file
        output_file_dictionary = a
    elif o == '-p': # postings file
        output_file_postings = a
    elif o == '-x':
        phrasal_queries = True
    else:
        assert False, "unhandled option"

if input_directory == None or output_file_postings == None or output_file_dictionary == None:
    usage()
    sys.exit(2)

N, dictionary, document_length = inputoutput.read_directory(input_directory)
pointers = inputoutput.write_postings(output_file_postings, dictionary)
inputoutput.write_dictionary(output_file_dictionary, dictionary, document_length, pointers, N)
