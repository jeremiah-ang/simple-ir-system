'''
VECTOR_SPACE.py

Description:
The functions in the file covers topic on vector space representation
of documents and queries, such as logtf, idf, cosine similarity

'''

import math
import itertools
import proximity
import expansion as ex
import inputoutput

NO_OF_RESULTS = 20

def logtf (tf):
    return 1 + math.log10(tf) if tf > 0 else 0
def idf (N, df):
    return math.log10(N / df) if df > 0 else 0
def tfidf_score (tf, idf):
    return tf * idf

class VectorQueryParser:
    def __init__ (self, get_posting, document_length, N):
        self.get_posting = get_posting
        self.document_length = document_length
        self.N = N

        self.idf_threshold = 0.2


    def filter_zero_score (self, scores):
        return {docid: score for docid, score in scores.iteritems() if score > 0}


    def normalise_score (self, scores):
        return {
            docid: scores[docid] / self.document_length[docid]
            for docid in scores
            } 
        
    def process_query (self, query, prox=None, custom_query_vec=None):
        score = {}
        query_vec = {}
        no_of_terms = len(query)
        if prox:
            prox.reset()

        for query_term in query:
            term_pos, term = query_term
            term_doc_freq_pos = self.get_posting(term)

            if custom_query_vec and term in custom_query_vec:
                qw = custom_query_vec[term]
                q_idf = 1
            else:
                df = len(term_doc_freq_pos)
                q_idf = idf(self.N, df)
                qw = q_idf if prox else q_idf * term_pos

            query_vec[term] = qw
            if (q_idf < self.idf_threshold):
                continue 
            for doc_freq_pos in term_doc_freq_pos:
                docid, tf, position = doc_freq_pos
                wf = logtf(tf)
                score[docid] = wf * qw if docid not in score else score[docid] + wf * qw

                if prox:
                    prox.add_location(term_pos, docid, position)


        score = self.normalise_score(score)
        score = prox.calculate_proximity_score(score, no_of_terms) if prox else score 
        score = self.filter_zero_score(score)
        return query_vec, score


