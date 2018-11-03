#!/usr/bin/env python3
import sys
import binascii
sys.path.append('..')
from helpers import abort
from xor import crack_singlebyte_xor

def detect_xored_cipher(filename):
  with open(sys.argv[1]) as cipher_file:
    best_score = 0
    best_line = ""
    for line in cipher_file:
      plaintext, score = crack_singlebyte_xor(binascii.unhexlify(line.rstrip()))
      if score > best_score:
        best_score = score
        best_line = plaintext 
  return best_line.rstrip()

if __name__ == "__main__":
  if len(sys.argv) == 2:
    print(detect_xored_cipher(sys.argv[1]))
  else: 
    abort(f'{sys.argv[0]}: filename')

