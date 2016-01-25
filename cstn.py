#!/usr/bin/env python3
# coding=UTF-8
'''This is the amazing CancerScript Tumor Notation module'''

# Python 2 compatibility
from __future__ import division, print_function, unicode_literals

def loads(text):
	'''Parses CSTN from a string and gives you back a nifty object'''
	return CancerScriptTumorNotationParser(text).parse()

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

		char = self.text[self.i]
		self.i += 1
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

	def seek_relative(self, i):
		'''
		Moves the cursor relative to its current position
		'''

		self.i += i

WHITESPACE = ' \n\t'
DIGITS = '0123456789ABCDEF'
ESCAPE_CHAR = '|'

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
				if char == 'n':
					char = '\n'
				elif char == 't':
					char = '\t'
			tumor += char

	def parse_tumor_list(self, endchar):
		'''
		Reads consecutive tumors (stopping at endchar) and returns them in a list
		This is also used to parse tuples, since they are effectively the same thing
		'''

		tumor = HashableList()
		while True:
			char = self.stream.peek_past_whitespace()
			if char == endchar:
				self.stream.seek_relative(1)
				return tumor
			tumor2 = self.parse_tumor()
			tumor.append(tumor2)

	def parse_tumor_dictionary(self, endchar):
		'''
		Reads consecutive tumors (stopping at endchar) and returns them in a dictionary
		This is the same as list parsing, but every 2 tumors read are used as a key and value pair
		'''

		tumor = HashableDict()
		while True:
			char = self.stream.peek_past_whitespace()
			if char == endchar:
				self.stream.seek_relative(1)
				return tumor
			key = self.parse_tumor()
			self.stream.peek_past_whitespace()
			value = self.parse_tumor()
			tumor[key] = value

	def parse_tumor_number(self, char):
		'''
		Reads and parses a number
		A CSTN number is a series of digits (0-9, A-F) and a suffix (to indicate the base)
		'''

		tumor = char
		while char in DIGITS:
			char = self.stream.read()
			tumor += char
		number = parse_cstn_number(tumor)
		return number
