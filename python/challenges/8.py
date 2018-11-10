#!/usr/bin/env python3
import sys
sys.path.append('..')
from helpers import abort
from block_crypto import detect_aes_ecb

if __name__ == "__main__":
  if len(sys.argv) == 2:
    with open(sys.argv[1], 'rb') as f:
      cipher_lines = f.readlines()
      idx = detect_aes_ecb(cipher_lines)
      print("index:", idx, "(starting from index 0)")
  else: 
    abort(f'{sys.argv[0]}: filename')
