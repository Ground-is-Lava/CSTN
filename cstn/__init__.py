from .parse import CancerScriptTumorNotationParser
from .unparse import unparse_tumor

def loads(text):
	'''Parses CSTN from a string and gives you back a nifty object'''
	return CancerScriptTumorNotationParser(text).parse()

def dump(tumor):
	return unparse_tumor(tumor)
