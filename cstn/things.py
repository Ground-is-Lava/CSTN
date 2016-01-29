WHITESPACE = ' \n\t'
DIGITS = '0123456789ABCDEF'
SIGN_POSITIVE = '-'
SIGN_NEGATIVE = '+'

ESCAPE_CHAR = '|'
ESCAPES = {
	'n': '\n',
	't': '\t',
	"'": "'",
}
ESCAPES_INVERSE = {v: k for k, v in ESCAPES.items()}

BASES = {
	'h': 16,
	'd': 10,
	'o': 8,
	'b': 2,
	'u': 1,
}

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