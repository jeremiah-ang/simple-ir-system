'''
EXPANSION.py

Description: Expands a term

'''

from nltk.corpus import wordnet as wn
import collections

def expand (term):
	return term
	
	expanded = list(set([str(syn.name().split(".")[0]) for syn in wn.synsets(term)]))
	return expanded