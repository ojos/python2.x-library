# -*- coding: utf-8 -*-
"""
source : http://emptypage.jp/gadgets/codepoint-py.ja.html
"""


import re
from __builtin__ import unichr as _unichr


__all__ = ['codepoint', 'unichr', 'characters']


rx_characters = re.compile(u'[\ud800-\udbff][\udc00-\udfff]|.', re.DOTALL)


def codepoint(c):
    r"""Return the code point of the Unicode character `c`

    Notice that some Unicode characters may be expressed with a couple 
    of other code points ("surrogate pair"). This function treats 
    surrogate pairs as representations of original code points; e.g. 
    codepoint(u'\ud842\udf9f') returns 134047 (0x20b9f).  
    u'\ud842\udf9f' is a surrogate pair expression which means  
    u'\U00020b9f'.

    >>> codepoint(u'a')
    97
    >>> codepoint(u'\u3042')
    12354
    >>> codepoint(u'\U00020b9f')
    134047
    >>> codepoint(u'\ud842\udf9f')
    134047
    >>> codepoint('a')
    Traceback (most recent call last):
      ...
    TypeError: must be unicode, not str
    >>> codepoint(u'abc')
    Traceback (most recent call last):
      ...
    TypeError: need a single Unicode character as parameter

    """

    if not isinstance(c, unicode):
        raise TypeError('must be unicode, not %s' % type(c).__name__)

    len_s = len(c)
    if len_s == 1:
        return ord(c)
    if len_s == 2:
        hi = ord(c[0])
        lo = ord(c[1])
        if 0xd800 <= hi < 0xdc00 and 0xdc00 <= lo < 0xe000:
            return (hi - 0xd800) * 0x400 + (lo - 0xdc00) + 0x10000
    raise TypeError('need a single Unicode character as parameter')


def unichr(cp):
    r"""Return the Unicode character for the code point integer, `cp`

    Notice that some Unicode characters may be expressed with a 
    couple of other code points ("surrogate pair"). This function may 
    return a unicode object of which length is more than two; e.g. 
    unichr(0x20b9f) returns u'\U00020b9f' while built-in unichr() may 
    raise ValueError.

    >>> unichr(0x20b9f)
    u'\U00020b9f'

    """

    if not isinstance(cp, int):
        raise TypeError('must be int, not %s' % type(c).__name__)

    if cp < 0x10000:
        return _unichr(cp)
    hi, lo = divmod(cp - 0x10000, 0x400)
    hi += 0xd800
    lo += 0xdc00
    if 0xd800 <= hi < 0xdc00 and 0xdc00 <= lo < 0xe000:
        return _unichr(hi) + _unichr(lo)
    raise ValueError('invalid code point')


def characters(s):
    """Return the list of Unicode characters in the unicode string `s`

    The number of iteration may differ from the len(s), because some 
    characters may be represented as a couple of other code points 
    ("surrogate pair").

    >>> s = u'abc\U00020b9f\u3042'
    >>> characters(s)
    [u'a', u'b', u'c', u'\U00020b9f', u'\u3042']

    """

    return rx_characters.findall(s)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
