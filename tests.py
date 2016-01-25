# coding=UTF-8

# Python 2 compatibility
from __future__ import division, print_function, unicode_literals

import cstn

def test_number_16():
	assert(cstn.loads('0h') == 0)
	assert(cstn.loads('1h') == 1)
	assert(cstn.loads('EFh') == 239)
	assert(cstn.loads('1234h') == 0x1234)
	assert(cstn.loads('    000Fh') == 15)

def test_number_12():
	assert(cstn.loads('0 ') == 0)
	assert(cstn.loads('1\t') == 1)
	assert(cstn.loads('AB\n') == 131)
	assert(cstn.loads('1234 ') == 2056)
	assert(cstn.loads('    000B ') == 11)

def test_number_10():
	assert(cstn.loads('0d') == 0)
	assert(cstn.loads('1d') == 1)
	assert(cstn.loads('89d') == 89)
	assert(cstn.loads('1234d') == 1234)
	assert(cstn.loads('    0009d') == 9)

def test_number_8():
	assert(cstn.loads('0o') == 0)
	assert(cstn.loads('1o') == 1)
	assert(cstn.loads('67o') == 55)
	assert(cstn.loads('1234o') == 0o1234)
	assert(cstn.loads('    0007o') == 7)

def test_number_2():
	assert(cstn.loads('0b') == 0)
	assert(cstn.loads('1b') == 1)
	assert(cstn.loads('11010b') == 0b11010)
	assert(cstn.loads('    0001b') == 1)
	assert(cstn.loads('101010b') == 42)

def test_number_1():
	assert(cstn.loads('0u') == 0)
	assert(cstn.loads('1u') == 1)
	assert(cstn.loads('1111111111u') == 10)
	assert(cstn.loads('    0001u') == 1)
	assert(cstn.loads('101010u') == 3)

def test_string():
	assert(cstn.loads(",hello, world!'") == 'hello, world!')
	assert(cstn.loads('«Je suis Cancer»') == 'Je suis Cancer')
	assert(cstn.loads(",escaped:|t|''") == "escaped:\t'")
	assert(cstn.loads('«escaped:|t|»»') == 'escaped:\t»')

EMPTY_LIST = cstn.HashableList()
EMPTY_DICT = cstn.HashableDict()

def test_list():
	assert(cstn.loads('{}') == EMPTY_LIST)
	assert(cstn.loads('{ }') == EMPTY_LIST)
	assert(cstn.loads('{\t}') == EMPTY_LIST)
	assert(cstn.loads('{\n}') == EMPTY_LIST)
	assert(cstn.loads('{1 2 3d}') == cstn.HashableList([1, 2, 3]))
	assert(cstn.loads("{,1',2',3'}") == cstn.HashableList(['1', '2', '3']))
	assert(cstn.loads("{,1'2d,3'}") == cstn.HashableList(['1', 2, '3']))

def test_tuple():
	assert(cstn.loads('[]') == ())
	assert(cstn.loads('[ ]') == ())
	assert(cstn.loads('[\t]') == ())
	assert(cstn.loads('[\n]') == ())
	assert(cstn.loads('[1 2 3d]') == (1, 2, 3))
	assert(cstn.loads("[,1',2',3']") == ('1', '2', '3'))
	assert(cstn.loads("[,1'2d,3']") == ('1', 2, '3'))

def test_dict():
	assert(cstn.loads('()') == EMPTY_DICT)
	assert(cstn.loads('( )') == EMPTY_DICT)
	assert(cstn.loads('(\t)') == EMPTY_DICT)
	assert(cstn.loads('(\n)') == EMPTY_DICT)
	assert(cstn.loads('(1d2d3d4d)') == cstn.HashableDict({1: 2, 3: 4}))
	assert(cstn.loads("(,1'2d3d«4»)") == cstn.HashableDict({'1': 2, 3: '4'}))
	assert(cstn.loads("({}{})") == cstn.HashableDict({EMPTY_LIST: EMPTY_LIST}))
	assert(cstn.loads("(({}{})3d)") == cstn.HashableDict({ cstn.HashableDict({EMPTY_LIST: EMPTY_LIST}): 3 }))

def test_readme():
	assert(cstn.loads("{,hello',world'}") == cstn.HashableList(['hello', 'world']))
	assert(cstn.loads("[,hello',world']") == ('hello', 'world'))
	assert(cstn.loads("(,hello',world')") == cstn.HashableDict({'hello': 'world'}))
	assert(cstn.loads('''{
    FFhFFh1234d
    (,key',value')
    ({«hello»«world»},the previous list is the key for this value')
}''') == cstn.HashableList([255, 255, 1234, cstn.HashableDict({'key': 'value'}), cstn.HashableDict({cstn.HashableList(['hello', 'world']): 'the previous list is the key for this value'})]))