#!/usr/bin/env python3
import sys
import binascii
sys.path.append('..')
from helpers import abort
from xor import xor_repeating_key 

if __name__ == "__main__":
  if len(sys.argv) == 3:
    with open(sys.argv[1]) as input_file:
      line = input_file.readline().rstrip()
      print(str(binascii.hexlify(xor_repeating_key(line, sys.argv[2])), 'ascii'))
  else: 
    abort(f'{sys.argv[0]}: filename key')
