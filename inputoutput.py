import csv
import sys
import os
import nltk
import itertools
import vector_space as vs
import math
import io
import cStringIO
import random
import expansion as ex
import dictionary_builder as db

'''
	Reading Corpus
'''
last = 0
count = 0

def case_id (case):
	return case[0]
def case_title (case):
	return case[1]
def case_content (case):
	return case[2]
def case_date (case):
	return case[3]
def case_court (case):
	return case[4]
def case_field (case, field):
	return case[int(field) + 1]

def read_cases_csv (csv_file, required=[]):

	fields = 4

	csv.field_size_limit(sys.maxsize)
	with open(csv_file, 'r') as fdin:
		cases_reader = csv.reader(fdin, quotechar='"')
		headers = cases_reader.next()

		terms, N = db.build_terms_csv(cases_reader, required=required)
		direct_index = db.build_direct_index (terms, fields)
		inverted_index, document_length = db.build_inverted_index (terms)

	return N, inverted_index, document_length, direct_index

def read_directory (directory):
	terms = []
	fields = 1

	terms, N = db.build_terms_dir(directory, fields)
	direct_index = db.build_direct_index (terms, fields)
	inverted_index, document_length = db.build_inverted_index (terms, fields)

	return N, inverted_index, document_length, direct_index



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

	return "{}\n".format(",".join(["{}+{}".format(
		docid, 
		"$".join(
			["{}".format(
				"&".join([str(pos) 
					for pos in postings[docid][zone]])) 
			for zone in postings[docid]])) 
		for docid in docids]))

def parse_posting_line (postings_line):
	# return [(doc_posting[0], # DocId
	# 		{field: [int(p) for p in pos.split("&")] # {Field: Posting list}
	# 				for field_posting in doc_posting[1].split("$") 
	# 					for field,pos in (field_posting.split("#"), )}) 
	# 			for doc_posting in [posting.split("+") 
	# 				for posting in postings_line.split(",")]]

	return [(docid.strip(), len(posting.split("&")), [int(x.strip()) for x in posting.split("&")]) for docid, posting in [postings.split("+") for postings in postings_line.split(",")]]
	

def make_get_posting (posting_fd, dictionary):

    def get_posting (word):
    	term = db.proc_word(word)
    	if term not in dictionary:
    		return []

        pointer = dictionary[term]
        posting_fd.seek(int(pointer))
        posting_line = posting_fd.readline()
        doc_postings = parse_posting_line(posting_line)
        return doc_postings

    def get_expanded_posting (term):
    	terms = ex.expand(term)
    	doc_postings = list(itertools.chain.from_iterable([get_posting(t) for t in terms]))
    	return doc_postings

    return get_posting

'''

Dictionary File

'''
def write_dictionary (dictionary_file, dictionary, document_length, direct_index, pointers, N):
	terms = dictionary.keys()
	terms.sort()
	topNterms = db.top_n_terms(direct_index, dictionary, 8)
	with open(dictionary_file, 'w') as fdout:
		fdout.write("{}\n".format(N))
		docids = document_length.keys()
		docids.sort()
		for docid in docids:
			fdout.write(document_length_line(docid, document_length[docid], topNterms[docid]))

		for term in terms:
			fdout.write(dictionary_line(term, pointers))

def dictionary_line(term, pointers):
	return "{} {}\n".format(term.encode('utf-8'), pointers[term])
def document_length_line(docid, length, topNterms):
	return "{} {}\n".format(docid, 
		";".join(["[{} ({})]".format(str(length[field]), 
			" @@ ".join(["{} {}".format(term[0].encode('utf-8'), term[1]) for term in topNterms[field]])) for field in length]))

def read_dictionary (dictionary_file):
	dictionary = {}
	document_length = {}
	topTerms = {}
	with open(dictionary_file, 'r') as fdin:
		N = float(fdin.readline().strip())
		for i in range(int(N)):
			docid, length, topTerm = parse_document_length_line(fdin.readline())
			document_length[docid] = length
			topTerms[docid] = topTerm

		for line in fdin:
			term, pointer = parse_dictionary_line(line)
			dictionary[term] = pointer

	return N, dictionary, document_length, topTerms

def parse_dictionary_line(line):
	term, pointer = line.split(" ")
	return term.strip().decode('utf-8'), pointer.strip()

def parse_document_length_line(line):
	docid, lengths = line.split(" ", 1)

	length = []
	topTerms = []
	for length_topN in lengths.strip().split(";"):
		l, topN = length_topN.strip("[]").split(" ", 1)
		length = float(l.strip())
		topTerms.append([N.strip().split(" ") for N in topN.strip("()").split("@@")])

	return docid, length, topTerms



'''

Query

'''
def read_query (query_file):
	queries = []
	with open(query_file, 'r') as fdin:
		for query_line in fdin:
			queries.append(parse_query_line(query_line))

	return queries

def is_boolean_query (query):
    return "AND" in query

def parse_query_line (query_line):
	return query_line 
	
	if is_boolean_query(query_line):
		query = query_line.split("AND")
		terms = []
		for term in query:
			term = term.strip().strip('"')
			terms.append([word for word in nltk.word_tokenize(term)])
		return terms
	return nltk.word_tokenize(query_line)












