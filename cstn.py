#!/usr/bin/env python3
# coding=UTF-8
'''This is the amazing CancerScript Tumor Notation module'''

# Python 2 compatibility
from __future__ import division, print_function, unicode_literals

from enum import Enum

def loads(text):
	'''Parses CSTN from a string and gives you back a nifty object'''
	return CancerScriptTumorNotationParser(text).parse()

class TumorType(Enum):
	'''tumor types, duh'''

	none = 0
	string = 1
	le_string = 2
	integer = 3
	floating = 4
	list = 5
	tuple = 6
	dict = 7
	number = 8

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
		char = self.text[self.i]
		return char

	def read(self):
		char = self.text[self.i]
		self.i += 1
		return char

	def skip(self, i):
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

	def skip_whitespace(self):
		'''skippin' whitespace, man'''
		char = self.stream.read()
		while char in WHITESPACE:
			char = self.stream.read()
		return char

	def skip_whitespace_peek(self):
		char = self.skip_whitespace()
		self.stream.i -= 1
		return char

	def parse_tumor(self):
		'''parses a tumor (recursive)'''

		char = self.skip_whitespace()

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
		tumor = HashableList()
		while True:
			char = self.skip_whitespace_peek()
			if char == endchar:
				self.stream.skip(1)
				return tumor
			tumor2 = self.parse_tumor()
			tumor.append(tumor2)

	def parse_tumor_dictionary(self, endchar):
		tumor = HashableDict()
		while True:
			char = self.skip_whitespace_peek()
			if char == endchar:
				self.stream.skip(1)
				return tumor
			key = self.parse_tumor()
			self.skip_whitespace_peek()
			value = self.parse_tumor()
			tumor[key] = value

	def parse_tumor_number(self, char):
		tumor = char
		while char in DIGITS:
			char = self.stream.read()
			tumor += char
		number = self.parse_number(tumor)
		return number

	def parse_number(self, text):
		'''Parses a string as a suffixed CSTN number'''

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
			return self.parse_base_1(text)
		return int(text, 12)

	def parse_base_1(self, text):
		'''Parses a string as a unary number'''

		number = 0
		for char in text:
			number += int(char, 2)
		return number
