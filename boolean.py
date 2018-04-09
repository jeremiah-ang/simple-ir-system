'''
BOOLEAN.py

Description:
The functions in the file covers topic on boolean retrieval

'''

import proximity
import inputoutput
import vector_space as vs

class BooleanQueryParser:
	def __init__ (self, get_posting):
		self.get_posting = get_posting
		self.prox = proximity.Proximity()

	def is_phrasal_query (self, query):
		return len(query) > 1

	def process_query (self, boolean_query):
		docids = set()

		for query in boolean_query:
			if self.is_phrasal_query(query):
				result = self.process_phrasal (query)
			else:
				result = self.process_individual (query)

			if docids:
				docids &= result
			else:
				docids = result
			
		return docids

	def process_phrasal (self, query, get_posting=None):
		if get_posting is None:
			get_posting = self.get_posting
		self.prox.reset()
		query = self.prox.prepare_query(query)

		for term_pos, term in query:
			doc_postings = get_posting(term)
			if not doc_postings:
				continue
			for doc_posting in doc_postings:
				docid, tf, locations = doc_posting 
				self.prox.add_location(term_pos, docid, locations)
		return set(self.prox.get_exact(len(query)))

	def process_individual (self, query, get_posting=None):
		if get_posting is None:
			get_posting = self.get_posting
			
		term = query[0]
		doc_postings = get_posting(term)
		if not doc_postings:
			return set()
		term_docids = set([doc_posting[0] for doc_posting in doc_postings])
		return term_docids
