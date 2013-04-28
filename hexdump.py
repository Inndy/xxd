#!/usr/bin/env python
# -*- coding: latin-1 -*-
"""
Dump binary data to the following text format:

0000000000: 00 00 00 5B 68 65 78 64  75 6D 70 5D 00 00 00 00  ...[hexdump]....
0000000010: 00 11 22 33 44 55 66 77  88 99 AA BB CC DD EE FF  .."3DUfw........

It is similar to the one used by:
Scapy
00 00 00 5B 68 65 78 64 75 6D 70 5D 00 00 00 00  ...[hexdump]....
00 11 22 33 44 55 66 77 88 99 AA BB CC DD EE FF  .."3DUfw........

Far Manager
000000000: 00 00 00 5B 68 65 78 64 � 75 6D 70 5D 00 00 00 00     [hexdump]
000000010: 00 11 22 33 44 55 66 77 � 88 99 AA BB CC DD EE FF   ?"3DUfw��������

"""

__version__ = '0.1'
__author__  = 'anatoly techtonik <techtonik@gmail.com>'
__license__ = 'Public Domain'

__history__ = \
"""
0.1 (2013-04-28)
 * working hexdump() function for Python 2
"""

import sys

# --- constants
PY3K = sys.version_info >= (3, 0)

# --- helpers
def int2byte(i):
  '''convert int [0..255] to binary byte'''
  if PY3K:
    return i.to_bytes(1, 'little')
  else:
    return chr(i)

def chunks(seq, size): 
  '''Cut sequence into chunks of given size. If `seq` length is 
     not divisible by `size` without reminder, last chunk will 
     have length less than size. 

     >>> list( chunks([1,2,3,4,5,6,7], 3) ) 
     [[1, 2, 3], [4, 5, 6], [7]] 
  ''' 
  d, m = divmod(len(seq), size)
  for i in range(d):
    yield [seq[i*size+n] for n in range(size)] 
  if m: 
    yield seq[d*size:] 

# --- stuff
def hexdump(data):
  # the format is (79 symbols wide)
  # 0000000000: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
  line = ''
  for addr, d in enumerate(chunks(data, 16)):
    # 0000000000:
    line = '%010X: ' % (addr*16)
    # 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 
    for byte in d[:8]:
      line += '%02X ' % ord(byte)
    line += ' '
    for byte in d[8:]:
      line += '%02X ' % ord(byte)
    # ................
    # calculate indentation, which may be different for the last line
    pad = 1
    if len(d) < 16:
      pad += 3*(16 - len(d))
    line += ' '*pad

    for byte in d:
      # printable ASCII range 0x20 to 0x7E
      if 0x20 <= ord(byte) <= 0x7E:
        line += byte
      else:
        line += '.'
    print(line)


if __name__ == '__main__':
  hexdump('zzzz'*12)
  hexdump('o'*17)
  hexdump('p'*24)
  hexdump('q'*26)
  hexdump('line\nfeed\r\ntest')
  hexdump('\x00\x00\x00\x5B\x68\x65\x78\x64\x75\x6D\x70\x5D\x00\x00\x00\x00'
          '\x00\x11\x22\x33\x44\x55\x66\x77\x88\x99\xAA\xBB\xCC\xDD\xEE\xFF')
