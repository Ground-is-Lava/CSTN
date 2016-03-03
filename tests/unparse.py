# coding=UTF-8

# Python 2 compatibility
from __future__ import division, print_function, unicode_literals

import cstn
from cstn.things import HashableList, HashableDict
from collections import OrderedDict

def test_number_dump():
	assert(cstn.dump(0) == '0d')
	assert(cstn.dump(1) == '1d')
	assert(cstn.dump(89) == '89d')
	assert(cstn.dump(1234) == '1234d')
	assert(cstn.dump(-9) == '+9d')

def test_string_dump():
	assert(cstn.dump('hello, world!') == ",hello, world!'")
	assert(cstn.dump("escaped:\t'") == ",escaped:|t|''")

def test_list_dump():
	assert(cstn.dump([]) == '{}')
	assert(cstn.dump([1, 2, 3]) == '{1d2d3d}')
	assert(cstn.dump(['1', '2', '3']) == "{,1',2',3'}")
	assert(cstn.dump(['1', 2, '3']) == "{,1'2d,3'}")

def test_tuple_dump():
	assert(cstn.dump(()) == '[]')
	assert(cstn.dump((1, 2, 3)) == '[1d2d3d]')
	assert(cstn.dump(('1', '2', '3')) == "[,1',2',3']")
	assert(cstn.dump(('1', 2, '3')) == "[,1'2d,3']")

EMPTY_LIST = HashableList()
EMPTY_DICT = HashableDict()

def test_dict_dump():
	assert(cstn.dump({}) == '()')
	assert(cstn.dump(OrderedDict([(1, 2), (3, 4)])) == '(1d2d3d4d)')
	assert(cstn.dump(OrderedDict([('1', 2), (3, '4')]) == "(,1'2d3d«4»)"))
	assert(cstn.dump({HashableList(): HashableList()}) == '({}{})')
	assert(cstn.dump({HashableDict({EMPTY_LIST: EMPTY_LIST}): 3}) == '(({}{})3d)')

def test_readme():
	assert(cstn.loads("{,hello',world'}") == HashableList(['hello', 'world']))
	assert(cstn.loads("[,hello',world']") == ('hello', 'world'))
	assert(cstn.loads("(,hello',world')") == HashableDict({'hello': 'world'}))
	assert(cstn.loads('''{
    FFhFFh1234d
    (,key',value')
    ({«hello»«world»},the previous list is the key for this value')
}''') == HashableList([255, 255, 1234, HashableDict({'key': 'value'}), HashableDict({HashableList(['hello', 'world']): 'the previous list is the key for this value'})]))
