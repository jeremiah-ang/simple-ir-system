import csv
import sys
import os
import nltk
import itertools
import vector_space as vs
import math

'''

Building dictionary

'''
def read_directory (directory):
	terms = []
	dictionary = {}
	document_length = {}
	N = 0
	for file in os.listdir(directory):
		docid = int(file)
		filename = os.path.join(directory, file)
		with open(filename, 'r') as fdin:
			build_terms(terms, docid, fdin)
		N += 1

	build_dictionary(dictionary, terms)
	calculate_document_length(document_length, terms)

	return N, dictionary, document_length 

def build_terms (terms, docid, line_stream):
	word_n = 0
	for line in line_stream:
		for sent in nltk.sent_tokenize(line):
			for word in nltk.word_tokenize(sent):
				term = proc_word(word)
				terms.append((term, docid, word_n, ))
				word_n += 1

def proc_word (word):
	stemmer = nltk.stem.porter.PorterStemmer()
	return stemmer.stem(word.strip().lower())

def build_dictionary (dictionary, terms):
	terms.sort(key=lambda v:(v[0], v[1]))
	for term_tuple in terms:
		term = term_tuple[0]
		docid = term_tuple[1]
		location = term_tuple[2]
		if term not in dictionary:
			dictionary[term] = {}
		if docid not in dictionary[term]:
			dictionary[term][docid] = []
		dictionary[term][docid].append(location)

def calculate_document_length (document_length, terms):
	terms.sort(key=lambda v:(v[1], v[0]))

	for docid,doc_term in itertools.groupby(terms, key=lambda v:v[1]):
		if docid not in document_length:
			document_length[docid] = {}
		for term,occur in itertools.groupby(doc_term, key=lambda v:v[0]):
			document_length[docid][term] = vs.logtf(len(list(occur))) ** 2

	for docid in document_length:
		document_length[docid] = math.sqrt(sum(document_length[docid].values()))


'''

Posting File

'''

def write_postings (postings_file, dictionary):
	postings = {}
	with open(postings_file, "w") as fdout:
		terms = dictionary.keys()
		terms.sort()
		for term in terms:
			postings[term] = fdout.tell()
			fdout.write(posting_line(dictionary[term]))
	return postings


def posting_line (postings):
	docids = postings.keys()
	docids.sort()
	return "{}\n".format(
		",".join(
			["{}#{}".format(
				docid, "&".join(
					[str(pos) for pos in postings[docid]])) for docid in docids]
			)
		)

def parse_posting_line (postings_line):
	return [(d[0], [int(c.strip()) for c in d[1].split("&")]) for d in [e.split("#") for e in postings_line.split(",")]]

def make_get_posting (posting_fd, dictionary):
    def get_posting (term):
    	if term not in dictionary:
    		return None

        pointer = dictionary[term]
        posting_fd.seek(int(pointer))
        posting_line = posting_fd.readline()
        doc_postings = parse_posting_line(posting_line)
        return doc_postings
    return get_posting

'''

Dictionary File

'''
def write_dictionary (dictionary_file, dictionary, document_length, pointers, N):
	terms = dictionary.keys()
	terms.sort()
	with open(dictionary_file, 'w') as fdout:
		fdout.write("{}\n".format(N))
		docids = document_length.keys()
		docids.sort()
		for docid in docids:
			fdout.write(document_length_line(docid, document_length[docid]))

		for term in terms:
			fdout.write(dictionary_line(term, pointers))

def dictionary_line(term, pointers):
	return "{} {}\n".format(term, pointers[term])
def document_length_line(docid, length):
	return "{} {}\n".format(docid, length)

def read_dictionary (dictionary_file):
	dictionary = {}
	document_length = {}
	with open(dictionary_file, 'r') as fdin:
		N = float(fdin.readline().strip())
		for i in range(int(N)):
			docid, length = parse_document_length_line(fdin.readline())
			document_length[docid] = length

		for line in fdin:
			term, pointer = parse_dictionary_line(line)
			dictionary[term] = pointer

	return N, dictionary, document_length

def parse_dictionary_line(line):
	return (x.strip() for x in line.split(" "))
def parse_document_length_line(line):
	docid, length = line.split(" ")
	return docid, float(length)



'''

Query

'''
def read_query (query_file):
	queries = []
	with open(query_file, 'r') as fdin:
		for query_line in fdin:
			queries.append(parse_query_line(query_line))
	return queries

def parse_query_line (query_line):
	return [proc_word(word) for sent in nltk.sent_tokenize(query_line) 
								for word in nltk.word_tokenize(sent)]












