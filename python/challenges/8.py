#!/usr/bin/env python3
import sys
sys.path.append('..')
from helpers import abort
from block_crypto import aes_ecb_detect

if __name__ == "__main__":
  if len(sys.argv) == 2:
    with open(sys.argv[1], 'rb') as f:
      cipher_lines = f.readlines()
      best_duplicate_count = 0
      best_idx = 0
      for idx, line in enumerate(cipher_lines):
        duplicate_count = aes_ecb_detect(line)
        if duplicate_count  > best_duplicate_count:
          best_duplicate_count  = duplicate_count
          best_idx = idx 
      print("index:", best_idx, "(starting from index 0)")
  else: 
    abort(f'{sys.argv[0]}: filename')
