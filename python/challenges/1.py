#!/usr/bin/env python3
import sys
import binascii
from base64 import b64encode, b64decode

if __name__ == "__main__":
  if len(sys.argv) <= 1:
    print(f'{sys.argv[0]}: [-d] input')
    sys.exit(0)

  if len(sys.argv) == 2:
    i1 = binascii.unhexlify(sys.argv[1])
    print(str(b64encode(i1), 'ascii'))

  if len(sys.argv) == 3:
    if sys.argv[1] == '-d':
      o1 = b64decode(sys.argv[2])
      print(str(binascii.hexlify(o1), 'ascii'))
     
