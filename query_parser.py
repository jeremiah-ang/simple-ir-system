'''
QUERY_PARSER.py

Description: Parse the query and do whatever is neccesary
if it is boolean, pass it to boolean query parser 
else do proximity search, collect the scores and do a pseudo
relevance feedback 

'''

import inputoutput
import boolean
import proximity
import vector_space
import nltk
import itertools
import heapq
import relevance_feedback as rf

class QueryParser:
	def __init__ (self, dictionary, document_length, N, topN, get_posting):
		self.dictionary = dictionary
		self.document_length = document_length
		self.N = N
		self.topN = topN
		self.get_posting = get_posting

		self.bParser = boolean.BooleanQueryParser(get_posting)
		self.vParser = vector_space.VectorQueryParser(get_posting, document_length, N)

		self.PROXIMITY = True
		self.NO_OF_RESULTS = 10
		self.prox = proximity.Proximity()
		self.rf = rf.RelevanceFeedback(self.get_posting, self.topN, self.document_length, self.N)

	def parse (self, query):
		if self.is_boolean_query(query):
			boolean_query = self.parse_boolean_query(query)
			result = self.process_boolean_query(boolean_query)
			return self.process_boolean_result(result, boolean_query)
		else:
			vector_query = self.parse_vector_query(query)
			if self.PROXIMITY:
				query_vector, result = self.process_vector_proximity_query(vector_query)
			else:
				query_vector, result = self.process_vector_query(vector_query)
			return self.process_vector_result(result, query_vector)

	def is_boolean_query(self, query):
		return "AND" in query

	def parse_boolean_query (self, query):
		query = query.split("AND")
		terms = []
		for term in query:
			term = term.strip().strip('"')
			terms.append([word for word in nltk.word_tokenize(term)])
		return terms

	def process_boolean_query(self, boolean_query):
		docids = self.bParser.process_query(boolean_query)
		return docids
	def process_boolean_result(self, result, boolean_query):
		print "=" * 100
		print boolean_query
		for docid in result:
			print "\t", docid
		print "=" * 100



	def parse_vector_query (self, query):
		return nltk.word_tokenize(query)
	def process_vector_query (self, query, prox=None, custom_query_vec=None):
		return self.vParser.process_query(query, prox=prox, custom_query_vec=custom_query_vec)
	def get_prox_weights (self, query_length):
		weight = [0.05, 0.15, 0.3, 0.5]
		if query_length == 3:
			return [0.1, 0.3, 0.6]
		elif query_length == 2:
			return [0.3, 0.7]
		elif query_length == 1:
			return [1]
		return weight
	def process_vector_proximity_query(self, query):
		def update_result (result, score, weight, length):
			length = length - 1
			for docid in score:
				value = weight[length] * score[docid]
				result[docid] = result[docid] + value if docid in result else value

		def process (query, results, weight, prox=None, length=None):
			query = query if not prox else prox.prepare_query(query)
			query_vec, score = self.process_vector_query(query, prox=prox)
			length = length if length else min(4, len(query))
			update_result(results, score, weight, length)
			return query_vec


		results = {}
		weight = self.get_prox_weights(len(query))
		length = min(3, len(query))

		if len(query) > 3:
			process (query, results, weight, self.prox)

		while len(results) < self.NO_OF_RESULTS and length > 1:
			query_step = [query[i:i+length] for i in range(len(query) - length + 1)]
			for smaller_query in query_step:
				process (smaller_query, results, weight, self.prox)
				length -= 1


		query = [(len(list(group)), term) for term, group in itertools.groupby(query)]
		query_vec = process (query, results, weight, length=1)

		return query_vec, results

	def process_vector_result (self, result, query_vector):
		sorted_results = self.heapify_result(result)
		print "\nBefore Relevance Feedback"
		self.print_score(sorted_results, query_vector)

		rf_query = self.rf.pseudo_feedback(sorted_results, query_vector)
		query = [(len(list(group)), term) for term, group in itertools.groupby(rf_query.keys())]
		query_vec, rf_score = self.process_vector_query(query, custom_query_vec=rf_query)

		sorted_rf_results = self.heapify_result(rf_score)
		print "\nAfter Relevance Feedback"
		self.print_score(sorted_rf_results, query_vec)

		return None

	def heapify_result(self, result):
		sorted_results = []
		for docid in result:
			heapq.heappush(sorted_results, (-result[docid], docid))
		return sorted_results

	def print_score (self, result, query_vector):
		print "=" * 100
		print "Query:", query_vector, "\n"
		for score in heapq.nsmallest(self.NO_OF_RESULTS, result):
			print "\t", score[1], -score[0], "\n"
		print "=" * 100, "\n"


