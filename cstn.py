#!/usr/bin/env python3
'''This is the amazing CancerScript Tumor Notation module'''

from enum import Enum

def loads(text: str):
	'''Parses CSTN from a string and gives you back a nifty object'''
	return CancerousTumorParser(text).parse()

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
		return tuple((k, self[k]) for k in sorted(self))

	def __hash__(self):
		return hash(self.__key())

	def __eq__(self, other):
		return self.__key() == other.__key()

WHITESPACE = ' \n\t'
DIGITS = '0123456789ABCDEF'
class CancerousTumorParser:
	'''this crap parses Cancerous Tumer Notation'''

	def __init__(self, text):
		self.text = text

	def parse(self):
		'''parse self.text pls'''
		return self.parse_tumor(0)[0]

	def consume_whitespace(self, i):
		'''skippin' whitespace, man'''
		char = self.text[i]
		while char in WHITESPACE:
			i += 1
			char = self.text[i]
		return char, i

	def parse_tumor(self, i):
		'''parses a tumor, starting at self.text[i]'''

		reading = TumorType.none
		tumor = None
		text_len = len(self.text)
		while i < text_len:
			char = self.text[i]

			if reading == TumorType.none:
				char, i = self.consume_whitespace(i)

			if (reading == TumorType.string) or (reading == TumorType.le_string):
				while True:
					if char == '|':
						i += 1
						char = self.text[i]
						if char == 'n':
							char = '\n'
						elif char == 't':
							char = '\t'
					elif (char == '\'' and reading == TumorType.string) or (char == '»' and reading == TumorType.le_string):
						i += 1
						return (tumor, i)
					tumor += char
					i += 1
					char = self.text[i]
			elif (reading == TumorType.list) or (reading == TumorType.tuple):
				while True:
					char, i = self.consume_whitespace(i)
					if (char == '}') and (reading == TumorType.list):
						return (tumor, i + 1)
					elif (char == ']') and (reading == TumorType.tuple):
						return (tuple(tumor), i + 1)
					tumor2, i = self.parse_tumor(i)
					tumor.append(tumor2)
			elif reading == TumorType.dict:
				while True:
					char, i = self.consume_whitespace(i)
					if char == ')':
						return (tumor, i + 1)
					key, i = self.parse_tumor(i)
					char, i = self.consume_whitespace(i)
					value, i = self.parse_tumor(i)
					tumor[key] = value
			elif reading == TumorType.number:
				while char in DIGITS:
					tumor += char
					i += 1
					char = self.text[i]
				tumor += char
				i += 1
				number = self.parse_number(tumor)
				return number, i
			else:
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
			i += 1
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
