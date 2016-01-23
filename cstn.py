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

		reading = TumorType.none
		tumor = None

		char = self.skip_whitespace()

		if char == ',':
			reading = TumorType.string
			tumor = ''
		elif char == '«':
			reading = TumorType.le_string
			tumor = ''
		elif char == '{':
			reading = TumorType.list
			tumor = HashableList()
		elif char == '[':
			reading = TumorType.tuple
			tumor = []
		elif char == '(':
			reading = TumorType.dict
			tumor = HashableDict()
		elif char in DIGITS:
			reading = TumorType.number
			tumor = char
		else:
			raise ValueError('CSTN syntax is invalid, or the parser is bugged (probably both)')

		if (reading == TumorType.string) or (reading == TumorType.le_string):
			while True:
				char = self.stream.read()
				if char == '|':
					char = self.stream.read()
					if char == 'n':
						char = '\n'
					elif char == 't':
						char = '\t'
				elif (char == '\'' and reading == TumorType.string) or (char == '»' and reading == TumorType.le_string):
					return tumor
				tumor += char
		elif (reading == TumorType.list) or (reading == TumorType.tuple):
			while True:
				char = self.skip_whitespace_peek()
				if (char == '}') and (reading == TumorType.list):
					self.stream.skip(1)
					return tumor
				elif (char == ']') and (reading == TumorType.tuple):
					self.stream.skip(1)
					return tuple(tumor)
				tumor2 = self.parse_tumor()
				tumor.append(tumor2)
		elif reading == TumorType.dict:
			while True:
				char = self.skip_whitespace_peek()
				if char == ')':
					self.stream.skip(1)
					return tumor
				key = self.parse_tumor()
				self.skip_whitespace_peek()
				value = self.parse_tumor()
				tumor[key] = value
		elif reading == TumorType.number:
			while char in DIGITS:
				char = self.stream.read()
				tumor += char
			number = self.parse_number(tumor)
			return number

		raise ValueError('CSTN is truncated in {}'.format(reading))

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
