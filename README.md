# CSTN [![Build Status](https://travis-ci.org/Ground-is-Lava/CSTN.svg?branch=master)](https://travis-ci.org/Ground-is-Lava/CSTN) 
CancerScript Tumor Notation is a lightweight data-interchange format. It is annoying for humans to read and write.

A CancerScript Tumor Notation file contains a tumor, which may or may not contain additional tumors. There are 2 tumor types:

 * a benign tumor is a comment (not yet implemented)
 * a malignant tumor is an object, such as a list or a string

Malignant tumors can identify as any of the following types (but only 1 at once):

 * string
 * integer (floats are not yet implemented)
 * list
 * tuple, for compatibility with Python
 * dict

Strings can be written in 2 ways:

 * ,pseudoGerman'
 * «French»

There are several number suffixes available:

 * any whitespace char: base 12
 * h: base 16
 * d: base 10
 * o: base 8
 * b: base 2
 * u: base 1

Lists are written like this:

	{
		item1
		item2
		item3
	}

Tuples are the same, but with square brackets instead.

Dictionaries are almost the same; there must be an even amount of items, since they are interpreted this way:

	(
		key1 value1
		key2 value2
		key3 value3
	)

As you can (not) see in the examples above, there are no commas (except to start strings). Whitespace is optional, too. Any object may be written adjacent to any other object. These are all valid:

	{,hello',world'}
<!-- -->
	[,hello',world']
<!-- -->
	(,hello',world')
<!-- -->
	{
		FFhFFh1234d
		(,key',value')
		({«hello»«world»},the previous list is the key for this value')
	}