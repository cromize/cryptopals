#!/usr/bin/env python3
import sys
import binascii
sys.path.append('..')
from helpers import abort
from base64 import b64decode
from xor import crack_multibyte_xor

if __name__ == "__main__":
  if len(sys.argv) == 2:
    with open(sys.argv[1]) as input_file:
      cipher = input_file.read().rstrip() 
      cipher = b64decode(cipher)
      plaintext, key = crack_multibyte_xor(cipher)
      print(plaintext.decode())
      print("key: ", key[:-1]) 
  else: 
    abort(f'{sys.argv[0]}: filename')
