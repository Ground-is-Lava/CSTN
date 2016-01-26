from .parse import CancerScriptTumorNotationParser
from .unparse import unparse_tumor

class HashableList(list):
	'''same as list, but hashable'''

	def __key(self):
		return tuple(self)

	def __hash__(self):
		return hash(self.__key())

	def __eq__(self, other):
		return self.__key() == other.__key()

class HashableDict(dict):
	'''same as dict, but hashable'''

	def __key(self):
		return tuple((k, self[k]) for k in sorted(self, key=str))

	def __hash__(self):
		return hash(self.__key())

	def __eq__(self, other):
		return self.__key() == other.__key()

def loads(text):
	'''Parses CSTN from a string and gives you back a nifty object'''
	return CancerScriptTumorNotationParser(text).parse()

def dump(tumor):
	return unparse_tumor(tumor)
