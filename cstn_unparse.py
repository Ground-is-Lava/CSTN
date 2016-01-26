#!/usr/bin/env python3
# coding=UTF-8
'''
functions for converting objects to CSTN
'''

# Python 2 compatibility
from __future__ import division, print_function, unicode_literals

import cstn

def unparse_tumor(tumor):
	'''
	Returns the CSTN representation of a Python object
	Chucks an error if the object type has no CSTN conversion
	'''

	if isinstance(tumor, str):
		return unparse_string(tumor)
	if isinstance(tumor, list):
		return unparse_list(tumor, '{', '}')
	if isinstance(tumor, tuple):
		return unparse_list(tumor, '[', ']')
	if isinstance(tumor, dict):
		return unparse_dict(tumor)
	if isinstance(tumor, int):
		return unparse_int(tumor)

	raise ValueError('i donut kno hoa 2 unparse {}'.format(type(tumor)))

def unparse_string(tumor_string):
	'''
	Returns the pseudoGerman CSTN representation of a string
	'''

	string = ','
	for char in tumor_string:
		if char in cstn.ESCAPES_INVERSE:
			string += cstn.ESCAPE_CHAR
			char = cstn.ESCAPES_INVERSE[char]
		string += char
	string += "'"
	return string

def unparse_list(tumor_list, startchar, endchar):
	'''
	Returns the CSTN representation of a list or a tuple
	(note startchar and endchar params)
	'''

	return startchar + ''.join(unparse_tumor(item) for item in tumor_list) + endchar

def unparse_dict(tumor_dict):
	'''
	Returns the CSTN representation of a dictionary
	'''

	pairs = zip(tumor_dict.keys(), tumor_dict.values())
	return unparse_list([item for pair in pairs for item in pair], '(', ')')

def unparse_int(tumor_int):
	'''
	Returns a CSTN equivalent of the given integer
	'''

	# TODO: use base 12
	string = int_to_base(tumor_int, 10)
	if string[0] == '-':
		string = cstn.SIGN_NEGATIVE + string[1:]
	elif string[0] == '+': # not going to happen, but check anyway just in case
		string = cstn.SIGN_POSITIVE + string[1:]
	string += 'd'
	return string

def int_to_base(i, base):
	if base == 10:
		return str(i)
	pass
