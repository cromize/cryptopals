#!/usr/bin/env python3
import binascii
import sys
import struct

def abort(msg):
  print(msg)
  sys.exit(1)

def xor(s1, s2):
  output = b''
  if not len(s1) == len(s2):
    raise ValueError("input string lengths doesn't match")

  for i in range(len(s1)):
    output += bytes([s1[i] ^ s2[i]])

  return output

if __name__ == "__main__":
  if len(sys.argv) <= 2:
    abort(f'{sys.argv[0]}: [-h] input1 input2')

  if len(sys.argv) == 3:
    i1 = binascii.unhexlify(sys.argv[1])
    i2 = binascii.unhexlify(sys.argv[2])
    xored = xor(i1, i2)
    print(str(binascii.hexlify(xored), 'ascii'))

  if len(sys.argv) == 4:
    i1 = binascii.unhexlify(sys.argv[2])
    i2 = binascii.unhexlify(sys.argv[3])
    xored = xor(i1, i2)
    if sys.argv[1] == '-h':
      print(str(xored, 'ascii'))
    else:
      abort(f'{sys.argv[0]}: [-h] input1 input2')  


