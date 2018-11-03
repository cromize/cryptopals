#!/usr/bin/env python3
import sys
import binascii
sys.path.append('..')
from helpers import abort, xor
from xor import crack_cipher

if __name__ == "__main__":
  if len(sys.argv) == 2:
    plaintext = crack_cipher(binascii.unhexlify(sys.argv[1]))
    print(plaintext)
  else: 
    abort(f'{sys.argv[0]}: input')
    
