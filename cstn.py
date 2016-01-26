#!/usr/bin/env python3
# coding=UTF-8
'''This is the amazing CancerScript Tumor Notation module'''

# Python 2 compatibility
from __future__ import division, print_function, unicode_literals

from cstn_unparse import unparse_tumor

def loads(text):
	'''Parses CSTN from a string and gives you back a nifty object'''
	return CancerScriptTumorNotationParser(text).parse()

def dump(tumor):
	return unparse_tumor(tumor)

def parse_cstn_number(text):
	'''
	Parses a string as a suffixed CSTN number
	'''

	base = text[-1]
	text = text[:-1]
	if base == 'h':
		return int(text, 16)
	if base == 'd':
		return int(text, 10)
	if base == 'o':
		return int(text, 8)
	if base == 'b':
		return int(text, 2)
	if base == 'u':
		return parse_base_1(text)
	return int(text, 12)

def parse_base_1(text):
	'''
	Parses a string as a unary number
	'''

	number = 0
	for char in text:
		number += int(char, 2)
	return number

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

class CharStream:
	def __init__(self, text, i=0):
		self.text = text
		self.i = i

	def peek(self):
		'''
		Reads a character without changing the cursor position
		'''

		char = self.text[self.i]
		return char

	def read(self):
		'''
		Reads a character and increments the cursor position
		'''

		char = self.peek()
		self.seek_relative(1)
		return char

	def peek_past_whitespace(self):
		'''
		Skips whitespace characters and returns the first non-whitespace character found
		The stream's cursor is set to read this character again
		'''

		char = self.read_past_whitespace()
		self.seek_relative(-1)
		return char

	def read_past_whitespace(self):
		'''
		Skips whitespace characters and returns the first non-whitespace character found
		The stream's cursor is set to right after this character
		'''

		char = self.read()
		while char in WHITESPACE:
			char = self.read()
		return char

	def read_while(self, condition):
		char = self.peek()
		string = ''
		while True:
			char = self.read()
			if condition(char):
				string += char
			else:
				self.seek_relative(-1)
				break
		return string


	def seek_relative(self, i):
		'''
		Moves the cursor relative to its current position
		'''

		self.i += i

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

class CancerScriptTumorNotationParser:
	'''this crap parses CancerScript Tumer Notation'''

	def __init__(self, text):
		self.stream = CharStream(text)

	def parse(self):
		'''parse self.text pls'''
		return self.parse_tumor()

	def parse_tumor(self):
		'''
		Parses the next CSTN tumor in the CharStream and returns its object equivalent
		'''

		char = self.stream.read_past_whitespace()

		if char == ',':
			return self.parse_tumor_string("'")
		elif char == '«':
			return self.parse_tumor_string('»')
		elif char == '{':
			return self.parse_tumor_list('}')
		elif char == '[':
			return tuple(self.parse_tumor_list(']'))
		elif char == '(':
			return self.parse_tumor_dictionary(')')
		elif char == SIGN_POSITIVE or char == SIGN_NEGATIVE:
			sign = -1 if char == SIGN_NEGATIVE else 1
			char = self.stream.read()
			if char in DIGITS:
				return sign * self.parse_tumor_number(char)
		elif char in DIGITS:
			return self.parse_tumor_number(char)

		raise ValueError('CSTN syntax is invalid (unexpected character: {})'.format(repr(char)))

	def parse_tumor_string(self, endchar):
		'''
		Reads a string, stopping when endchar is encountered (unless escaped)
		'''

		tumor = ''
		while True:
			char = self.stream.read()
			if char == endchar:
				return tumor
			if char == ESCAPE_CHAR:
				char = self.stream.read()
				if char in ESCAPES:
					char = ESCAPES[char]
			tumor += char

	def parse_tumor_list(self, endchar):
		'''
		Reads consecutive tumors (stopping at endchar) and returns them in a list
		This is also used to parse tuples, since they are effectively the same thing
		'''

		tumor = HashableList()
		while self.stream.peek_past_whitespace() != endchar:
			tumor2 = self.parse_tumor()
			tumor.append(tumor2)
		self.stream.seek_relative(1)
		return tumor

	def parse_tumor_dictionary(self, endchar):
		'''
		Reads consecutive tumors (stopping at endchar) and returns them in a dictionary
		This is the same as list parsing, but every 2 tumors read are used as a key and value pair
		'''

		tumor = HashableDict()
		while self.stream.peek_past_whitespace() != endchar:
			key = self.parse_tumor()
			self.stream.peek_past_whitespace()
			value = self.parse_tumor()
			tumor[key] = value
		self.stream.seek_relative(1)
		return tumor

	def parse_tumor_number(self, firstchar):
		'''
		Reads and parses a number
		A CSTN number is a series of digits (0-9, A-F) and a suffix (to indicate the base)
		'''

		tumor = firstchar
		tumor += self.stream.read_while(lambda c: c in DIGITS)
		tumor += self.stream.read()
		return parse_cstn_number(tumor)
