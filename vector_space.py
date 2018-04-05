import math

def logtf (tf):
	return 1 + math.log10(tf) if tf > 0 else 0
def idf (N, df):
	return math.log10(N / df) if df > 0 else 0
def score (tf, idf):
	return tf * idf
def normalise_score (scores, document_length):
	for docid in scores:
		scores[docid] /= document_length[docid]