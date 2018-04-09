'''
INPUTOUTPUT.py

Description: A quick and dirty input and output handler

'''

import itertools
import vector_space as vs
import math
import nltk
import os
import string
import random

stemmer = nltk.stem.porter.PorterStemmer()

def build_direct_index (terms, fields):
	direct_index = {}
	for field, field_terms in enumerate(terms):
		direct_index[field] = {}
		for docid, group in itertools.groupby(field_terms, key=lambda x: x[1]):
			direct_index[field][docid] = {}
			group = list(group)
			group.sort(key=lambda x: x[0])
			for term, pos in itertools.groupby(list(group), key=lambda x: x[0]):
				direct_index[field][docid][term] = len(list(pos))

	return direct_index

def top_n_terms (direct_index, inverted_index, n):
	top_n = {}
	for field, field_docs in direct_index.iteritems():
		N = len(field_docs)
		for docid, terms in field_docs.iteritems():
			if docid not in top_n:
				top_n[docid] = {}
			if field not in top_n[docid]:
				top_n[docid][field] = {}
			top_n[docid][field] = [term for term in list(sorted(terms.iteritems(), 
				key=lambda x:vs.tfidf_score(x[1], vs.idf(N, len(inverted_index[x[0]])))))[:n]]

	return top_n

def build_inverted_index (terms):
	dictionary = [[]]
	document_length = [[]]

	dictionary[0], document_length[0] = build_dictionary_doc_length(terms[0])

	dictionary = merge_dictionary_fields(dictionary)
	document_length = merge_document_length_fields(document_length)

	return dictionary, document_length

def build_dictionary_doc_length (terms):
	dictionary = {}
	document_length = {}
	build_dictionary(dictionary, terms)
	calculate_document_length(document_length, terms)
	return dictionary, document_length

def build_dictionary (dictionary, terms):
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
	for docid,doc_term in itertools.groupby(terms, key=lambda v:v[1]):
		if docid not in document_length:
			document_length[docid] = {}
		for term,occur in itertools.groupby(doc_term, key=lambda v:v[0]):
			document_length[docid][term] = vs.logtf(len(list(occur))) ** 2

	for docid in document_length:
		document_length[docid] = math.sqrt(sum(document_length[docid].values()))


def merge_dictionary_fields (dictionary):
	merged_dict = {}
	for field,dict_field in enumerate(dictionary):
		for term in dict_field:
			if term not in merged_dict:
				merged_dict[term] = {}
			doc_pos = dict_field[term]
			for docid in doc_pos:
				if docid not in merged_dict[term]:
					merged_dict[term][docid] = {}
				merged_dict[term][docid][field] = doc_pos[docid]

	return merged_dict

def merge_document_length_fields (document_length):
	merged_doc_len = {}
	for field,doc_len_field in enumerate(document_length):
		for docid in doc_len_field:
			if docid not in merged_doc_len:
				merged_doc_len[docid] = {field: []}
			merged_doc_len[docid][field] = document_length[field][docid]
	return merged_doc_len

def build_terms_csv (csv_reader, row_id = lambda x:x[0], row_content = lambda x:x[2], required=[]):
	nolimit = True
	terms = [[build_terms (row_id(row), row_content(row).splitlines())] 
					for row in csv_reader 
						if nolimit 
							or row[0] in required 
								or random.randint(0,99) < 1]
	return proc_terms (terms)

def build_terms_dir (directory, fields):
	terms = list(itertools.chain.from_iterable([build_terms (file, open(os.path.join(directory, file), 'r'))
					for file in os.listdir(directory)]))
	return proc_terms(terms)

def proc_terms (terms):
	N = len(terms)
	terms = [list(itertools.chain.from_iterable(field)) for field in zip(*terms)]
	return terms, N

def build_terms (docid, line_stream):
	print "Adding: ", docid
	return [(word[0], word[1], idx) for idx, word in enumerate([(proc_word(word), docid) 
			for line in line_stream 
					for word in nltk.word_tokenize(line.decode('utf-8'))]) if word[0]]
				

def proc_word (word):
	return stemmer.stem(word.strip().decode('utf-8')) if word.strip() not in string.punctuation else ""