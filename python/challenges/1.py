#!/usr/bin/env python3
import sys
import binascii
import base64

def b_to_hex(input):
  return base64.b64encode(input)

def hex_to_b(input):
  return binascii.hexlify(base64.b64decode(input))

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print(f'{sys.argv[0]}: [-d] input')
    sys.exit(0)

  if len(sys.argv) < 3:
    print(str(b_to_hex(binascii.unhexlify(sys.argv[1])), 'ascii'))

  if len(sys.argv) < 4:
    if sys.argv[1] == '-d':
      print(str(hex_to_b(sys.argv[2]), 'ascii'))
     
