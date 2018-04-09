'''
RELEVANCE_FEEDBACK.py

Description:
The functions in the file covers topic on relevance feedback,
fetching top k document, 
fetching the top n terms of each k document
adding those n terms into the query vector
returning the updated vector

'''

import vector_space as vs
import heapq

class RelevanceFeedback:
	def __init__ (self, get_posting, topTerms, document_length, N):
		self.get_posting = get_posting
		self.topTerms = topTerms
		self.document_length = document_length
		self.N = N

	def pseudo_feedback (self, score, query_vec, k=3):
		k = min(k, len(score))
		topK_docid = [heapq.heappop(score)[1] for i in range(k)]
		rel = {}
		for docid in topK_docid:
			for term_tf in self.topTerms[docid][0]:
				term, tf = term_tf
				wf = vs.logtf(int(tf))
				rel[term] = rel[term] + wf if term in rel else wf

		for term in rel:
			df = len(self.get_posting(term))
			idf = vs.idf(self.N, df)
			add = rel[term] / 3 * idf
			query_vec[term] = query_vec[term] + add if term in query_vec else add

		return query_vec












