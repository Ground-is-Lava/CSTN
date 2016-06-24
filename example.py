#!/usr/bin/env python3
# coding=UTF-8
'''An example of how to use the cstn module'''

# Python 2 compatibility
from __future__ import division, print_function, unicode_literals

import sys
from pprint import pprint

import cstn

def warn(message):
	'''Prints a message in red (hopefully)'''
	print('\x1B[91m{}\x1B[0m'.format(message))

def fail(message, code=1):
	'''Prints a message in red (hopefully) and exits'''
	warn(message)
	exit(code)

def main(args):
	'''it's just me, Main Newell'''

	if len(args) <= 1:
		fail('filename needed')

	with open(args[1], 'r') as f:
		text = f.read()

	try:
		tumor = cstn.loads(text)
	except ValueError as e:
		fail('failed to parse tumor: {}'.format(e))

	pprint(tumor)

if __name__ == '__main__':
	main(sys.argv)
