#!/usr/bin/env python3
import sys
import binascii
sys.path.append('..')
from helpers import abort, xor
from xor import crack_singlebyte_xor

if __name__ == "__main__":
  if len(sys.argv) == 2:
    plaintext = crack_singlebyte_xor(binascii.unhexlify(sys.argv[1]))[0].decode()
    print(plaintext)
  else: 
    abort(f'{sys.argv[0]}: input')
    
