#!/usr/bin/env python3
import sys
sys.path.append('..')
from helpers import abort
from block_crypto import pkcs7_pad
  
if __name__ == "__main__":
  if len(sys.argv) == 3:
    padded = pkcs7_pad(sys.argv[1].encode(), int(sys.argv[2]))
    print(padded)
  else: 
    abort(f'{sys.argv[0]}: text pad_length')
