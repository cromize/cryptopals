#!/usr/bin/env python3
import sys
import binascii
sys.path.append('..')
from helpers import abort, xor
from base64 import b64encode, b64decode

if __name__ == "__main__":
  if len(sys.argv) == 2:
    i1 = binascii.unhexlify(sys.argv[1])
    print(str(b64encode(i1), 'ascii'))
  elif len(sys.argv) == 3 and sys.argv[1] == '-d':
    o1 = b64decode(sys.argv[2])
    print(str(binascii.hexlify(o1), 'ascii'))
  else:
    abort(f'{sys.argv[0]}: [-d] input')
     
