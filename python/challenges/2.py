#!/usr/bin/env python3
import sys
import binascii
sys.path.append('..')
from helpers import abort, xor

if __name__ == "__main__":
  if len(sys.argv) == 3:
    i1 = binascii.unhexlify(sys.argv[1])
    i2 = binascii.unhexlify(sys.argv[2])
    xored = xor(i1, i2)
    print(str(binascii.hexlify(xored), 'ascii'))
  elif len(sys.argv) == 4 and sys.argv[1] == '-h':
    i1 = binascii.unhexlify(sys.argv[2])
    i2 = binascii.unhexlify(sys.argv[3])
    xored = xor(i1, i2)
    print(str(xored, 'ascii'))
  else:
    abort(f'{sys.argv[0]}: [-h] input1 input2')

