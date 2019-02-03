#!/usr/bin/env python3
import sys
import random
sys.path.append('..')
from block_crypto import aes_ecb_encrypt, get_random_bytes, aes_ecb_detect
from helpers import abort
from collections import Counter

to_append = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"

key = get_random_bytes(16)

def find_block(target, ciphertext):
  cipher_blocks = [ciphertext[i:i+16] for i in range(0, len(ciphertext), 16)]
  counter = Counter(cipher_blocks)
  sentinel = counter.most_common()[0][0]
  target = sentinel
  print("here")
  print(sentinel)
  for idx, block in enumerate(cipher_blocks):
    if block == target:
      print("FOUND")
      print("idx:", idx)
      print(target)
  
def oracle(plaintext, append, key):
  random_prefix = get_random_bytes(random.randrange(1, 48))
  to_cipher = random_prefix + plaintext.encode() + append.encode()
  cipher = aes_ecb_encrypt(to_cipher, key)
  return cipher

if __name__ == "__main__":
  if len(sys.argv) == 1:
    target = oracle(4*16*"a", to_append, key)
    print("duplicate count:", aes_ecb_detect(target))
    find_block(16*"a", target)
    fake = aes_ecb_encrypt(16*b"a", key)
    print("fake:", fake)
    

  else:
    abort(f'{sys.argv[0]}: filename')
